from django.shortcuts import render
from django.views import generic
from .models import LabTest


class LabTestListView(generic.ListView):
    model = LabTest
    template_name = 'laboratory/labtest_list.html'
    context_object_name = 'lab_tests'


class LabTestCreateView(generic.CreateView):
    model = LabTest
    fields = '__all__'
    template_name = 'laboratory/labtest_form.html'
    success_url = '/labtests/'


class LabTestUpdateView(generic.UpdateView):
    model = LabTest
    fields = '__all__'
    template_name = 'laboratory/labtest_form.html'
    success_url = '/labtests/'


class LabTestDeleteView(generic.DeleteView):
    model = LabTest
    template_name = 'laboratory/labtest_confirm_delete.html'
    success_url = '/labtests/'

# Create your views here.
