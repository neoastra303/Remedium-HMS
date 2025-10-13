from django.shortcuts import render
from django.views import generic
from .models import Staff


class StaffListView(generic.ListView):
    model = Staff
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff'


class StaffCreateView(generic.CreateView):
    model = Staff
    fields = '__all__'  # Use all fields from the model
    template_name = 'staff/staff_form.html'
    success_url = '/staff/'  # Redirect to the list view after success


class StaffUpdateView(generic.UpdateView):
    model = Staff
    fields = '__all__'  # Use all fields from the model
    template_name = 'staff/staff_form.html'
    success_url = '/staff/'  # Redirect to the list view after success


class StaffDeleteView(generic.DeleteView):
    model = Staff
    template_name = 'staff/staff_confirm_delete.html'
    success_url = '/staff/'  # Redirect to the list view after success

# Create your views here.
