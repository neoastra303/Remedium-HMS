from django.shortcuts import render
from django.views import generic
from .models import Appointment


class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    fields = '__all__'  # Use all fields from the model
    template_name = 'appointments/appointment_form.html'
    success_url = '/appointments/'  # Redirect to the list view after success


class AppointmentUpdateView(generic.UpdateView):
    model = Appointment
    fields = '__all__'  # Use all fields from the model
    template_name = 'appointments/appointment_form.html'
    success_url = '/appointments/'  # Redirect to the list view after success


class AppointmentDeleteView(generic.DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = '/appointments/'  # Redirect to the list view after success

# Create your views here.
