from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.db import connections
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from appointments.models import Appointment
from patients.models import Patient
from billing.models import Invoice
from staff.models import Staff


def homepage(request):
    context = {}
    if request.user.is_authenticated:
        context["total_patients"] = Patient.objects.count()
        context["admitted_patients"] = Patient.objects.filter(
            admission_date__isnull=False, discharge_date__isnull=True
        ).count()
        context["recent_patients"] = Patient.objects.order_by("-admission_date")[:5]
        context["now"] = timezone.now()

        today = timezone.now().date()
        context["today_appointments"] = Appointment.objects.filter(
            appointment_date__date=today, status="Scheduled"
        ).count()
        context["upcoming_appointments"] = (
            Appointment.objects.filter(
                appointment_date__gte=timezone.now(), status="Scheduled"
            )
            .select_related("patient", "doctor")
            .order_by("appointment_date")[:5]
        )

        staff_profile = getattr(request.user, "staff_profile", None)
        if staff_profile and staff_profile.role == "DOCTOR":
            context["my_appointments"] = (
                Appointment.objects.filter(
                    doctor=staff_profile,
                    appointment_date__date=today,
                    status="Scheduled",
                )
                .select_related("patient")
                .order_by("appointment_date")[:5]
            )

        if request.user.is_superuser or (
            staff_profile and staff_profile.role == "ADMIN"
        ):
            context["unpaid_invoices"] = Invoice.objects.filter(paid=False).count()
            revenue_agg = Invoice.objects.filter(paid=True).aggregate(
                total=Sum("total_amount")
            )
            context["total_revenue"] = revenue_agg["total"] or 0
            context["active_staff"] = Staff.objects.filter(is_active=True).count()

            dept_stats = list(
                Staff.objects.values("department")
                .annotate(count=Count("id"))
                .order_by("-count")[:5]
            )
            if dept_stats:
                max_count = dept_stats[0]["count"]
                for d in dept_stats:
                    d["pct"] = int(d["count"] / max_count * 100) if max_count else 0
            context["dept_stats"] = dept_stats

    return render(request, "index.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def health_check(request):
    health = {"status": "healthy", "database": "connected"}
    status_code = 200
    try:
        conn = connections["default"]
        conn.ensure_connection()
    except Exception as e:
        health["database"] = f"error: {str(e)}"
        health["status"] = "unhealthy"
        status_code = 503
    return JsonResponse(health, status=status_code)


@login_required
@user_passes_test(
    lambda u: u.is_superuser
    or (hasattr(u, "staff_profile") and u.staff_profile.role == "ADMIN")
)
def audit_log(request):
    from patients.models import Patient
    from staff.models import Staff
    from appointments.models import Appointment
    from billing.models import Invoice
    from django.contrib.auth.models import User

    all_history = sorted(
        list(Patient.history.all()[:20])
        + list(Staff.history.all()[:20])
        + list(Appointment.history.all()[:20])
        + list(Invoice.history.all()[:20]),
        key=lambda x: x.history_date,
        reverse=True,
    )[:50]
    # Annotate each entry with model name (can't access _meta in templates)
    for entry in all_history:
        try:
            entry.model_name = entry.instance._meta.verbose_name.title()
        except Exception:
            entry.model_name = type(entry).__name__.replace("Historical", "")
    return render(request, "core/audit_logs.html", {"history": all_history})


class DeleteSuccessMixin:
    """Appends ?deleted=1 to the success URL so the list page shows a toast."""

    def get_success_url(self):
        url = super().get_success_url()
        return f"{url}?deleted=1"
