from django.db import models
from django.db.models import Sum
from patients.models import Patient
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords


class Invoice(models.Model):
    class Meta:
        app_label = 'billing'
        permissions = [
            ('billing_view_invoice', 'Can view invoice'),
            ('billing_add_invoice', 'Can add invoice'),
            ('billing_change_invoice', 'Can change invoice'),
            ('billing_delete_invoice', 'Can delete invoice'),
        ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    insurance_claimed = models.BooleanField(default=False)
    details = models.TextField(blank=True, null=True)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        """Auto-generate invoice number if not set."""
        if not self.invoice_number:
            year = timezone.now().year
            # Get the next sequence number for this year
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=f'INV-{year}-'
            ).order_by('-invoice_number').first()
            if last_invoice:
                seq = int(last_invoice.invoice_number.split('-')[-1]) + 1
            else:
                seq = 1
            self.invoice_number = f'INV-{year}-{seq:05d}'
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.total_amount and self.total_amount < 0:
            raise ValidationError({'total_amount': "Total amount cannot be negative."})
        if self.issue_date and self.due_date and self.due_date < self.issue_date:
            raise ValidationError({'due_date': "Due date cannot be before the issue date."})

    def __str__(self):
        return f"Invoice #{self.id} for {self.patient}"


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

    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.amount} for Invoice #{self.invoice.id}"


@receiver(post_save, sender=Payment)
def update_invoice_paid(sender, instance, created, **kwargs):
    """Signal to update invoice paid status when a payment is created."""
    if created:
        total_paid = instance.invoice.payments.aggregate(total=Sum('amount'))['total'] or 0
        if total_paid >= instance.invoice.total_amount:
            instance.invoice.paid = True
            instance.invoice.save(update_fields=['paid'])