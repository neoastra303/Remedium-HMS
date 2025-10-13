from django.shortcuts import render
from django.views import generic
from .models import Prescription


class PrescriptionListView(generic.ListView):
    model = Prescription
    template_name = 'pharmacy/prescription_list.html'
    context_object_name = 'prescriptions'


class PrescriptionCreateView(generic.CreateView):
    model = Prescription
    fields = '__all__'
    template_name = 'pharmacy/prescription_form.html'
    success_url = '/prescriptions/'


class PrescriptionUpdateView(generic.UpdateView):
    model = Prescription
    fields = '__all__'
    template_name = 'pharmacy/prescription_form.html'
    success_url = '/prescriptions/'


class PrescriptionDeleteView(generic.DeleteView):
    model = Prescription
    template_name = 'pharmacy/prescription_confirm_delete.html'
    success_url = '/prescriptions/'

# Create your views here.
