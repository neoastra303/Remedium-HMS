from django.shortcuts import render
from django.views import generic
from .models import Invoice


class InvoiceListView(generic.ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'invoices'


class InvoiceCreateView(generic.CreateView):
    model = Invoice
    fields = '__all__'
    template_name = 'billing/invoice_form.html'
    success_url = '/invoices/'


class InvoiceUpdateView(generic.UpdateView):
    model = Invoice
    fields = '__all__'
    template_name = 'billing/invoice_form.html'
    success_url = '/invoices/'


class InvoiceDeleteView(generic.DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = '/invoices/'

# Create your views here.
