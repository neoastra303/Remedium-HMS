from django.shortcuts import render
from django.views import generic
from .models import Surgery

class SurgeryListView(generic.ListView):
    model = Surgery
    template_name = 'surgery/surgery_list.html'
    context_object_name = 'surgeries'

class SurgeryCreateView(generic.CreateView):
    model = Surgery
    fields = '__all__'
    template_name = 'surgery/surgery_form.html'
    success_url = '/surgeries/'


class SurgeryUpdateView(generic.UpdateView):
    model = Surgery
    fields = '__all__'
    template_name = 'surgery/surgery_form.html'
    success_url = '/surgeries/'


class SurgeryDeleteView(generic.DeleteView):
    model = Surgery
    template_name = 'surgery/surgery_confirm_delete.html'
    success_url = '/surgeries/'

# Create your views here.
