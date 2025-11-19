from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .forms import PrescriptionForm
from .models import Prescription


class PrescriptionListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Prescription
    template_name = 'pharmacy/prescription_list.html'
    context_object_name = 'prescriptions'
    paginate_by = 10  # Add pagination
    permission_required = 'pharmacy.pharmacy_view_prescription'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'prescribed_date') # Default sort by prescribed_date
        return queryset.order_by(order_by)


class PrescriptionDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Prescription
    template_name = 'pharmacy/prescription_detail.html'
    context_object_name = 'prescription'
    permission_required = 'pharmacy.pharmacy_view_prescription'
    raise_exception = True


class PrescriptionCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'pharmacy/prescription_form.html'
    success_url = reverse_lazy('prescription_list')
    permission_required = 'pharmacy.pharmacy_add_prescription'
    raise_exception = True


class PrescriptionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'pharmacy/prescription_form.html'
    success_url = reverse_lazy('prescription_list')
    permission_required = 'pharmacy.pharmacy_change_prescription'
    raise_exception = True


class PrescriptionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Prescription
    template_name = 'pharmacy/prescription_confirm_delete.html'
    success_url = reverse_lazy('prescription_list')
    permission_required = 'pharmacy.pharmacy_delete_prescription'
    raise_exception = True

# Create your views here.
