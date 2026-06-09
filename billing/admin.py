from django.contrib import admin
from .models import Invoice, Payment, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ('service', 'description', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'issue_date', 'due_date', 'total_amount', 'paid')
    list_filter = ('paid', 'insurance_claimed', 'issue_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'invoice_number')
    inlines = [InvoiceItemInline, PaymentInline]
    readonly_fields = ('total_amount', 'invoice_number')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
