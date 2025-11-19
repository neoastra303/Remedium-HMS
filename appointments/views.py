from django.shortcuts import render
from django.views import generic
from .models import Appointment
from .forms import AppointmentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class AppointmentListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10  # Add pagination
    permission_required = 'appointments.appointments_view_appointment'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'appointment_date') # Default sort by appointment_date
        return queryset.order_by(order_by)


class AppointmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')  # Redirect to the list view after success
    permission_required = 'appointments.appointments_add_appointment'
    raise_exception = True


class AppointmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')  # Redirect to the list view after success
    permission_required = 'appointments.appointments_change_appointment'
    raise_exception = True


class AppointmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')  # Redirect to the list view after success
    permission_required = 'appointments.appointments_delete_appointment'
    raise_exception = True


class AppointmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'
    permission_required = 'appointments.appointments_view_appointment'
    raise_exception = True


# Create your views here.