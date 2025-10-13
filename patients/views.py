from django.shortcuts import render
from django.views import generic
from .models import Patient
from django.db.models import Q

class PatientListView(generic.ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Patient.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(unique_id__icontains=query)
            )
        else:
            return Patient.objects.all()

class PatientDetailView(generic.DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'


class PatientCreateView(generic.CreateView):
    model = Patient
    fields = '__all__'  # Use all fields from the model
    template_name = 'patients/patient_form.html'
    success_url = '/patients/'  # Redirect to the list view after success


class PatientUpdateView(generic.UpdateView):
    model = Patient
    fields = '__all__'  # Use all fields from the model
    template_name = 'patients/patient_form.html'
    success_url = '/patients/'  # Redirect to the list view after success


class PatientDeleteView(generic.DeleteView):
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = '/patients/'  # Redirect to the list view after success

# Create your views here.
