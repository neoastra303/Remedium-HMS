from django.db import models
from .models import Invoice
from django.utils import timezone

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('INSURANCE', 'Insurance'),
        ('ONLINE', 'Online Payment'),
    ]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='COMPLETED')
    
    def __str__(self):
        return f"{self.amount} for Invoice #{self.invoice.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update invoice status
        total_paid = sum(p.amount for p in self.invoice.payments.all())
        if total_paid >= self.invoice.total_amount:
            self.invoice.paid = True
            self.invoice.save()
