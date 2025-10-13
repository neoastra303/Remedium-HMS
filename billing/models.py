from django.db import models
from patients.models import Patient


class Invoice(models.Model):
    class Meta:
        app_label = 'billing'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    insurance_claimed = models.BooleanField(default=False)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.id} for {self.patient}"
