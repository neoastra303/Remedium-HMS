from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .forms import SurgeryForm
from .models import Surgery

class SurgeryListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Surgery
    template_name = 'surgery/surgery_list.html'
    context_object_name = 'surgeries'
    paginate_by = 10  # Add pagination
    permission_required = 'surgery.surgery_view_surgery'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'scheduled_date') # Default sort by scheduled_date
        return queryset.order_by(order_by)

class SurgeryDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Surgery
    template_name = 'surgery/surgery_detail.html'
    context_object_name = 'surgery'
    permission_required = 'surgery.surgery_view_surgery'
    raise_exception = True


class SurgeryCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Surgery
    form_class = SurgeryForm
    template_name = 'surgery/surgery_form.html'
    success_url = reverse_lazy('surgery_list')
    permission_required = 'surgery.surgery_add_surgery'
    raise_exception = True


class SurgeryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Surgery
    form_class = SurgeryForm
    template_name = 'surgery/surgery_form.html'
    success_url = reverse_lazy('surgery_list')
    permission_required = 'surgery.surgery_change_surgery'
    raise_exception = True


class SurgeryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Surgery
    success_url = reverse_lazy('surgery_list')
    permission_required = 'surgery.surgery_delete_surgery'
    raise_exception = True

# Create your views here.
