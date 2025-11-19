from django.shortcuts import render
from django.views import generic
from .models import Invoice
from .forms import InvoiceForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class InvoiceListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10  # Add pagination
    permission_required = 'billing.billing_view_invoice'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'issue_date') # Default sort by issue_date
        return queryset.order_by(order_by)


class InvoiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'billing.billing_add_invoice'
    raise_exception = True


class InvoiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'billing.billing_change_invoice'
    raise_exception = True


class InvoiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'billing.billing_delete_invoice'
    raise_exception = True


class InvoiceDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Invoice
    template_name = 'billing/invoice_detail.html'
    context_object_name = 'invoice'
    permission_required = 'billing.billing_view_invoice'
    raise_exception = True


# Create your views here.