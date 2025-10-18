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
    permission_required = 'surgery_view_surgery'

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'scheduled_date') # Default sort by scheduled_date
        return queryset.order_by(order_by)

class SurgeryDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Surgery
    template_name = 'surgery/surgery_detail.html'
    context_object_name = 'surgery'
    permission_required = 'surgery_view_surgery'


class SurgeryCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Surgery
    form_class = SurgeryForm
    template_name = 'surgery/surgery_form.html'
    success_url = reverse_lazy('surgery_list')
    permission_required = 'surgery_add_surgery'


class SurgeryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Surgery
    form_class = SurgeryForm
    template_name = 'surgery/surgery_form.html'
    success_url = reverse_lazy('surgery_list')


class SurgeryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Surgery
    success_url = reverse_lazy('surgery_list')
    permission_required = 'surgery_delete_surgery'

# Create your views here.
