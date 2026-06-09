from django.db import models
from django.db.models import Sum
from patients.models import Patient
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords


class InvoiceCounter(models.Model):
    """Per-year atomic sequence counter for invoice numbers."""
    year = models.PositiveIntegerField(primary_key=True)
    last_seq = models.PositiveIntegerField(default=0)

    @classmethod
    def next_seq(cls, year):
        """Atomically increment and return the next sequence number for the given year."""
        from django.db import transaction
        with transaction.atomic():
            counter, _ = cls.objects.select_for_update().get_or_create(year=year)
            counter.last_seq += 1
            counter.save(update_fields=['last_seq'])
            return counter.last_seq


class Invoice(models.Model):
    class Meta:
        app_label = 'billing'
        permissions = [
            ('billing_view_invoice', 'Can view invoice'),
            ('billing_add_invoice', 'Can add invoice'),
            ('billing_change_invoice', 'Can change invoice'),
            ('billing_delete_invoice', 'Can delete invoice'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_amount__gte=0),
                name='invoice_total_amount_non_negative'
            ),
            models.CheckConstraint(
                condition=models.Q(due_date__gte=models.F('issue_date')),
                name='invoice_due_after_issue'
            ),
        ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False, db_index=True)
    insurance_claimed = models.BooleanField(default=False, db_index=True)
    details = models.TextField(blank=True, null=True)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        """Auto-generate invoice number if not set."""
        if not self.invoice_number:
            year = timezone.now().year
            seq = InvoiceCounter.next_seq(year)
            self.invoice_number = f'INV-{year}-{seq:05d}'
        return super().save(*args, **kwargs)

    def update_total(self):
        """Recalculate total amount from items."""
        total = self.items.aggregate(total=Sum('total_price'))['total'] or 0
        self.total_amount = total
        self.save(update_fields=['total_amount'])

    def clean(self):
        super().clean()
        if self.total_amount and self.total_amount < 0:
            raise ValidationError({'total_amount': "Total amount cannot be negative."})
        if self.issue_date and self.due_date and self.due_date < self.issue_date:
            raise ValidationError({'due_date': "Due date cannot be before the issue date."})

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.patient}"


class InvoiceItem(models.Model):
    """Individual line items on an invoice."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey('hospital.HospitalService', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, help_text="Specific description for this item")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.description and self.service:
            self.description = self.service.name
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        # Update parent invoice total
        self.invoice.update_total()

    def __str__(self):
        return f"{self.description} (x{self.quantity}) on {self.invoice.invoice_number}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('INSURANCE', 'Insurance'),
        ('ONLINE', 'Online Payment'),
    ]
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name='payment_amount_positive'
            ),
        ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, db_index=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    status = models.CharField(max_length=20, default='COMPLETED', db_index=True)

    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.amount} for Invoice #{self.invoice.invoice_number}"


@receiver(post_save, sender=Payment)
def update_invoice_paid(sender, instance, created, **kwargs):
    """Signal to update invoice paid status when a payment is created."""
    if created:
        total_paid = instance.invoice.payments.aggregate(total=Sum('amount'))['total'] or 0
        if total_paid >= instance.invoice.total_amount:
            instance.invoice.paid = True
            instance.invoice.save(update_fields=['paid'])
