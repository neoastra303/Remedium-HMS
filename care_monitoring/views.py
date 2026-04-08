from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import PatientCare
from patients.models import Patient
import json


class PatientCareForm(forms.ModelForm):
    """Form for PatientCare that excludes auto-managed fields."""
    class Meta:
        model = PatientCare
        fields = [
            'patient', 'status', 'temperature', 'heart_rate',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'respiratory_rate', 'oxygen_saturation', 'weight', 'height',
            'notes', 'monitored_by',
        ]


class PatientCareListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = PatientCare
    template_name = 'care_monitoring/patientcare_list.html'
    context_object_name = 'patientcares'
    paginate_by = 10
    permission_required = 'care_monitoring.care_monitoring_view_patientcare'
    raise_exception = True

    ALLOWED_ORDER_BY = ['monitoring_date', 'status', '-monitoring_date', '-status']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient', 'monitored_by')
        order_by = self.request.GET.get('order_by', 'monitoring_date')
        if order_by not in self.ALLOWED_ORDER_BY:
            order_by = 'monitoring_date'
        return queryset.order_by(order_by)


class PatientCareDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = PatientCare
    template_name = 'care_monitoring/patientcare_detail.html'
    context_object_name = 'patientcare'
    permission_required = 'care_monitoring.care_monitoring_view_patientcare'
    raise_exception = True

    def get_queryset(self):
        return PatientCare.objects.select_related('patient', 'monitored_by').all()


class PatientCareCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = PatientCare
    form_class = PatientCareForm
    template_name = 'care_monitoring/patientcare_form.html'
    success_url = reverse_lazy('care_monitoring:patientcare_list')
    permission_required = 'care_monitoring.care_monitoring_add_patientcare'
    raise_exception = True


class PatientCareUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = PatientCare
    form_class = PatientCareForm
    template_name = 'care_monitoring/patientcare_form.html'
    success_url = reverse_lazy('care_monitoring:patientcare_list')
    permission_required = 'care_monitoring.care_monitoring_change_patientcare'
    raise_exception = True


class PatientCareDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = PatientCare
    template_name = 'care_monitoring/patientcare_confirm_delete.html'
    success_url = reverse_lazy('care_monitoring:patientcare_list')
    permission_required = 'care_monitoring.care_monitoring_delete_patientcare'
    raise_exception = True


class PatientVitalTrendsView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Patient
    template_name = 'care_monitoring/vital_trends.html'
    context_object_name = 'patient'
    permission_required = 'care_monitoring.care_monitoring_view_patientcare'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        care_records = PatientCare.objects.filter(patient=self.object).order_by('monitoring_date')

        dates = []
        heart_rates = []
        temperatures = []
        systolic = []
        diastolic = []
        oxygen = []

        for record in care_records:
            dates.append(record.monitoring_date.strftime("%Y-%m-%d %H:%M"))
            heart_rates.append(record.heart_rate if record.heart_rate else 0)
            temperatures.append(float(record.temperature) if record.temperature else 0)
            systolic.append(record.blood_pressure_systolic if record.blood_pressure_systolic else 0)
            diastolic.append(record.blood_pressure_diastolic if record.blood_pressure_diastolic else 0)
            oxygen.append(float(record.oxygen_saturation) if record.oxygen_saturation else 0)

        context['chart_data'] = json.dumps({
            'dates': dates,
            'heart_rates': heart_rates,
            'temperatures': temperatures,
            'systolic': systolic,
            'diastolic': diastolic,
            'oxygen': oxygen,
        })

        context['latest_care'] = care_records.last()

        return context
