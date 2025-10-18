from django.db import models
from patients.models import Patient
from django.utils import timezone
from django.core.exceptions import ValidationError


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
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    insurance_claimed = models.BooleanField(default=False)
    details = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        if self.total_amount and self.total_amount < 0:
            raise ValidationError({'total_amount': "Total amount cannot be negative."})
        if self.issue_date and self.due_date and self.due_date < self.issue_date:
            raise ValidationError({'due_date': "Due date cannot be before the issue date."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.id} for {self.patient}"