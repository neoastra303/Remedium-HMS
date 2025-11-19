from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .forms import StaffForm
from .models import Staff


class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Staff
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_list' # Changed to staff_list to avoid conflict with template variable
    paginate_by = 10  # Add pagination
    permission_required = 'staff.staff_view_staff'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'last_name') # Default sort by last_name
        return queryset.order_by(order_by)


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'
    permission_required = 'staff.staff_view_staff'
    raise_exception = True


class StaffCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Staff
    form_class = StaffForm  # Use the custom form class
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')  # Redirect to the list view after success
    permission_required = 'staff.staff_add_staff'
    raise_exception = True


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Staff
    form_class = StaffForm  # Use the custom form class
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')  # Redirect to the list view after success
    permission_required = 'staff.staff_change_staff'
    raise_exception = True


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Staff
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')  # Redirect to the list view after success
    permission_required = 'staff.staff_delete_staff'
    raise_exception = True

# Create your views here.
