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

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'staff_profile') and user.staff_profile.role == 'ADMIN')

def homepage(request):
    context = {}
    if request.user.is_authenticated:
        # Global context stats
        context['total_patients'] = Patient.objects.count()
        context['recent_patients'] = Patient.objects.order_by('-admission_date')[:5]
        
        today = timezone.now().date()
        context['today_appointments'] = Appointment.objects.filter(
            appointment_date__date=today,
            status='Scheduled'
        ).count()
        
        context['upcoming_appointments'] = Appointment.objects.filter(
            appointment_date__gte=timezone.now(),
            status='Scheduled'
        ).order_by('appointment_date')[:5]

        # Doctor-specific data
        staff_profile = getattr(request.user, 'staff_profile', None)
        if staff_profile and staff_profile.role == 'DOCTOR':
            context['my_appointments'] = Appointment.objects.filter(
                doctor=staff_profile,
                appointment_date__date=today,
                status='Scheduled'
            ).order_by('appointment_date')[:5]

        # Admin/Management data
        if request.user.is_superuser or (staff_profile and staff_profile.role == 'ADMIN'):
            context['unpaid_invoices'] = Invoice.objects.filter(paid=False).count()
            revenue_agg = Invoice.objects.filter(paid=True).aggregate(total=Sum('total_amount'))
            context['total_revenue'] = revenue_agg['total'] or 0
            context['active_staff'] = Staff.objects.filter(is_active=True).count()

            # Simple department stats
            dept_stats = Staff.objects.values('department').annotate(count=Count('id')).order_by('-count')[:5]
            context['dept_stats'] = dept_stats

    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


def health_check(request):
    """Lightweight health check endpoint for Docker and load balancers.

    Returns 200 with database connectivity check.
    No authentication required.
    """
    health = {
        'status': 'healthy',
        'database': 'connected',
    }
    status_code = 200

    # Check database connectivity
    try:
        conn = connections['default']
        conn.ensure_connection()
    except Exception as e:
        health['database'] = f'error: {str(e)}'
        health['status'] = 'unhealthy'
        status_code = 503

    return JsonResponse(health, status=status_code)

@login_required
@user_passes_test(is_admin)
def audit_log(request):
    # Fetch historical records from various models
    from patients.models import Patient
    from staff.models import Staff
    from appointments.models import Appointment
    from billing.models import Invoice
    from django.contrib.auth.models import User
    
    # Get latest 50 changes across main models
    patient_history = Patient.history.all()[:20]
    staff_history = Staff.history.all()[:20]
    appointment_history = Appointment.history.all()[:20]
    invoice_history = Invoice.history.all()[:20]
    user_history = User.history.all()[:20]
    
    # Combine and sort by history_date
    all_history = sorted(
        list(patient_history) + list(staff_history) + list(appointment_history) + list(invoice_history) + list(user_history),
        key=lambda x: x.history_date,
        reverse=True
    )[:50]
    
    return render(request, 'core/audit_logs.html', {'history': all_history})

# Create your views here.