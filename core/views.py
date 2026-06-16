from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, F
from django.db import models, connections
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from appointments.models import Appointment
from patients.models import Patient
from billing.models import Invoice
from staff.models import Staff
from care_monitoring.models import PatientCare
from pharmacy.models import Prescription
from laboratory.models import LabTest
from surgery.models import Surgery
from inventory.models import InventoryItem
from hospital.models import HospitalService


def get_role(request):
    """Determine user role from staff profile, falling back to groups."""
    staff_profile = getattr(request.user, "staff_profile", None)
    if staff_profile:
        return staff_profile.role
    if request.user.is_superuser:
        return "ADMIN"
    return "OTHER"


def get_role_template(role):
    """Map role to dashboard template."""
    mapping = {
        "ADMIN": "dashboards/admin_dashboard.html",
        "DOCTOR": "dashboards/doctor_dashboard.html",
        "NURSE": "dashboards/nurse_dashboard.html",
        "RECEPTIONIST": "dashboards/receptionist_dashboard.html",
        "PHARMACIST": "dashboards/pharmacist_dashboard.html",
        "LAB_TECH": "dashboards/labtech_dashboard.html",
        "SURGEON": "dashboards/surgeon_dashboard.html",
        "ANESTHESIOLOGIST": "dashboards/surgeon_dashboard.html",
    }
    return mapping.get(role, "dashboards/default_dashboard.html")


def get_role_display(role):
    mapping = {
        "ADMIN": "Administrator",
        "DOCTOR": "Physician",
        "NURSE": "Nursing Staff",
        "RECEPTIONIST": "Receptionist",
        "PHARMACIST": "Pharmacist",
        "LAB_TECH": "Lab Technician",
        "SURGEON": "Surgeon",
        "ANESTHESIOLOGIST": "Anesthesiologist",
        "RADIOLOGIST": "Radiologist",
        "TECH": "Technician",
        "SECURITY": "Security",
        "MAINTENANCE": "Maintenance",
        "OTHER": "Staff",
    }
    return mapping.get(role, "Staff")


def homepage(request):
    context = {}
    if not request.user.is_authenticated:
        return render(request, "index.html", context)

    staff_profile = getattr(request.user, "staff_profile", None)
    role = get_role(request)
    today = timezone.now().date()

    # ── Common context for all roles ──
    context["total_patients"] = Patient.objects.count()
    context["admitted_patients"] = Patient.objects.filter(
        admission_date__isnull=False, discharge_date__isnull=True
    ).count()
    context["recent_patients"] = Patient.objects.select_related("ward", "room").order_by("-admission_date")[:5]
    context["now"] = timezone.now()
    context["role_display"] = get_role_display(role)

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

    # ── Admin context ──
    if role == "ADMIN" or request.user.is_superuser:
        context["unpaid_invoices"] = Invoice.objects.filter(paid=False).count()
        context["paid_invoices"] = Invoice.objects.filter(paid=True).count()
        revenue_agg = Invoice.objects.filter(paid=True).aggregate(total=Sum("total_amount"))
        context["total_revenue"] = revenue_agg["total"] or 0
        context["active_staff"] = Staff.objects.filter(is_active=True).count()
        context["discharged_patients"] = Patient.objects.filter(discharge_date__isnull=False).count()
        context["completed_today"] = Appointment.objects.filter(
            appointment_date__date=today, status="Completed"
        ).count()
        context["on_duty_today"] = Staff.objects.filter(is_active=True).count()
        context["recent_invoices"] = Invoice.objects.select_related("patient").order_by("-issue_date")[:5]

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

    # ── Doctor context ──
    if role == "DOCTOR" and staff_profile:
        context["my_appointments"] = (
            Appointment.objects.filter(
                doctor=staff_profile,
                appointment_date__date=today,
                status="Scheduled",
            )
            .select_related("patient")
            .order_by("appointment_date")[:5]
        )
        context["my_pending_appointments"] = Appointment.objects.filter(
            doctor=staff_profile,
            appointment_date__date=today,
            status="Scheduled",
        ).count()
        context["my_patient_count"] = Appointment.objects.filter(
            doctor=staff_profile
        ).values("patient").distinct().count()
        context["active_care_count"] = PatientCare.objects.filter(
            status="STABLE"
        ).count() + PatientCare.objects.filter(status="CRITICAL").count()
        context["my_prescriptions_count"] = Prescription.objects.filter(
            prescribed_by=staff_profile
        ).count()
        context["recent_vitals"] = PatientCare.objects.select_related("patient").order_by("-monitoring_date")[:5]
        context["upcoming_surgeries"] = Surgery.objects.filter(
            scheduled_date__gte=timezone.now()
        ).select_related("patient").order_by("scheduled_date")[:5]

    # ── Nurse context ──
    if role == "NURSE":
        context["active_care_count"] = PatientCare.objects.filter(
            status__in=["STABLE", "CRITICAL"]
        ).count()
        context["critical_count"] = PatientCare.objects.filter(status="CRITICAL").count()
        context["stable_count"] = PatientCare.objects.filter(status="STABLE").count()
        context["recent_vitals"] = PatientCare.objects.select_related("patient").order_by("-monitoring_date")[:5]
        context["critical_care"] = PatientCare.objects.filter(
            status="CRITICAL"
        ).select_related("patient").order_by("-monitoring_date")[:5]
        context["recent_admissions_count"] = Patient.objects.filter(
            admission_date__gte=today - timedelta(days=7)
        ).count()

    # ── Receptionist context ──
    if role == "RECEPTIONIST":
        context["available_doctors"] = Staff.objects.filter(
            role="DOCTOR", is_active=True
        ).count()
        context["new_patients_7days"] = Patient.objects.filter(
            admission_date__gte=today - timedelta(days=7)
        ).count()
        context["checked_in_count"] = Appointment.objects.filter(
            appointment_date__date=today, status="Scheduled"
        ).count()

    # ── Pharmacist context ──
    if role == "PHARMACIST":
        context["active_prescriptions"] = Prescription.objects.filter(status="Active").count()
        context["pending_dispense"] = Prescription.objects.filter(status="Active").count()
        context["new_prescriptions_today"] = Prescription.objects.filter(
            prescribed_date__date=today
        ).count()
        context["dispensed_today"] = Prescription.objects.filter(
            prescribed_date__date=today
        ).count()
        context["low_stock_count"] = InventoryItem.objects.filter(
            quantity__lte=F("reorder_level")
        ).count()
        context["low_stock_items"] = list(InventoryItem.objects.filter(
            quantity__lte=F("reorder_level")
        )[:5])
        context["pending_prescriptions"] = Prescription.objects.filter(
            status="Active"
        ).select_related("patient", "prescribed_by").order_by("-prescribed_date")[:10]

    # ── Lab Tech context ──
    if role == "LAB_TECH":
        context["pending_tests"] = LabTest.objects.filter(status="Requested").count()
        context["completed_today"] = LabTest.objects.filter(
            requested_date__date=today, status="Completed"
        ).count()
        context["in_progress_tests"] = LabTest.objects.filter(status="In Progress").count()
        context["requests_today"] = LabTest.objects.filter(
            requested_date__date=today
        ).count()
        context["pending_lab_tests"] = LabTest.objects.filter(
            status="Requested"
        ).select_related("patient").order_by("-requested_date")[:10]
        context["recent_completed"] = LabTest.objects.filter(
            status="Completed"
        ).select_related("patient").order_by("-requested_date")[:5]

    # ── Surgeon / Anesthesiologist context ──
    if role in ("SURGEON", "ANESTHESIOLOGIST") and staff_profile:
        surgeon_filter = {"surgeon": staff_profile} if role == "SURGEON" else {}
        context["upcoming_surgeries_count"] = Surgery.objects.filter(
            scheduled_date__gte=timezone.now(), **surgeon_filter
        ).count()
        context["surgeries_today"] = Surgery.objects.filter(
            scheduled_date__date=today, **surgeon_filter
        ).count()
        context["completed_surgeries_7days"] = Surgery.objects.filter(
            scheduled_date__gte=today - timedelta(days=7),
            status="Completed", **surgeon_filter
        ).count()
        context["my_patient_count"] = Surgery.objects.filter(
            **surgeon_filter
        ).values("patient").distinct().count()
        context["pre_op_count"] = Surgery.objects.filter(
            status="Scheduled", **surgeon_filter
        ).count()
        context["consult_count"] = 0
        context["today_surgeries"] = Surgery.objects.filter(
            scheduled_date__date=today, **surgeon_filter
        ).select_related("patient").order_by("scheduled_date")[:5]
        context["upcoming_surgeries"] = Surgery.objects.filter(
            scheduled_date__gte=timezone.now(), **surgeon_filter
        ).select_related("patient").order_by("scheduled_date")[:5]

    template = get_role_template(role)
    return render(request, template, context)


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
