from django.shortcuts import render
from django.views import generic
from .models import Patient
from .forms import PatientForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10  # Add pagination
    permission_required = 'patients_view_patient'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        order_by = self.request.GET.get('order_by', 'last_name') # Default sort by last_name

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(unique_id__icontains=query)
            )
        
        return queryset.order_by(order_by)

class PatientDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'
    permission_required = 'patients_view_patient'


from .forms import PatientForm

class PatientCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = '/patients/'  # Redirect to the list view after success
    permission_required = 'patients_add_patient'


class PatientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = '/patients/'  # Redirect to the list view after success
    permission_required = 'patients_change_patient'


class PatientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = '/patients/'  # Redirect to the list view after success
    permission_required = 'patients_delete_patient'

# Create your views here.