from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Invoice, Payment
from .forms import InvoiceForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class InvoiceListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10  # Add pagination
    permission_required = 'billing.billing_view_invoice'
    raise_exception = True

    ALLOWED_ORDER_BY = ['issue_date', 'due_date', 'total_amount', '-issue_date', '-due_date', '-total_amount']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient')
        order_by = self.request.GET.get('order_by', 'issue_date')
        if order_by not in self.ALLOWED_ORDER_BY:
            order_by = 'issue_date'
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

    def get_queryset(self):
        return Invoice.objects.select_related('patient').prefetch_related('payments').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payments.all()
        return context


class PaymentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Payment
    fields = ['amount', 'payment_method', 'transaction_id']
    template_name = 'billing/payment_form.html'

    def form_valid(self, form):
        form.instance.invoice = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('invoice_detail', kwargs={'pk': self.kwargs['invoice_pk']})


# Create your views here.