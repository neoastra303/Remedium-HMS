from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .models import PatientCare
from django.urls import reverse_lazy

class PatientCareListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = PatientCare
    template_name = 'care_monitoring/patientcare_list.html'
    context_object_name = 'patientcares'
    paginate_by = 10  # Add pagination
    permission_required = 'care_monitoring.care_monitoring_view_patientcare'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'monitoring_date') # Default sort by monitoring_date
        return queryset.order_by(order_by)

class PatientCareDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = PatientCare
    template_name = 'care_monitoring/patientcare_detail.html'
    context_object_name = 'patientcare'
    permission_required = 'care_monitoring.care_monitoring_view_patientcare'
    raise_exception = True

class PatientCareCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = PatientCare
    fields = '__all__'
    template_name = 'care_monitoring/patientcare_form.html'
    success_url = reverse_lazy('care_monitoring:patientcare_list')
    permission_required = 'care_monitoring.care_monitoring_add_patientcare'
    raise_exception = True


class PatientCareUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = PatientCare
    fields = '__all__'
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
