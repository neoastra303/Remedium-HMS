import secrets

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required as perm_decorator
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from .forms import StaffForm, StaffWithUserForm
from .models import Staff, Shift


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shifts'] = self.object.shifts.all()
        return context


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


class ShiftCreateView(LoginRequiredMixin, generic.CreateView):
    model = Shift
    fields = ['day_of_week', 'start_time', 'end_time']
    template_name = 'staff/shift_form.html'

    def form_valid(self, form):
        form.instance.staff = get_object_or_404(Staff, pk=self.kwargs['staff_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.kwargs['staff_pk']})


class ShiftDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Shift
    template_name = 'staff/shift_confirm_delete.html'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.staff.pk})

# User Management Views

class UserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Staff
    template_name = 'staff/user_list.html'
    context_object_name = 'users_list'
    permission_required = 'auth.view_user' # Needs appropriate permission
    raise_exception = True

    def get_queryset(self):
        # Only show staff that have a linked user account
        return Staff.objects.filter(user__isnull=False).select_related('user').order_by('user__username')


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    form_class = StaffWithUserForm
    template_name = 'staff/user_form.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'auth.add_user'
    raise_exception = True

@login_required
@perm_decorator('auth.change_user')
def toggle_user_status(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if staff.user:
        user = staff.user
        user.is_active = not user.is_active
        user.save()
        
        staff.is_active = user.is_active
        staff.save()
        
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.username} has been {status}.")
    
    return redirect('user_list')

@login_required
@perm_decorator('auth.change_user')
def admin_reset_password(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if staff.user:
        user = staff.user
        temp_password = secrets.token_urlsafe(12)
        user.set_password(temp_password)
        user.save()
        messages.success(request, f"Password for {user.username} has been reset. New password: {temp_password}")

    return redirect('user_list')
