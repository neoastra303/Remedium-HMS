from django.db import models
from patients.models import Patient


class Prescription(models.Model):
    class Meta:
        app_label = 'pharmacy'
        permissions = [
            ('pharmacy_view_prescription', 'Can view prescription'),
            ('pharmacy_add_prescription', 'Can add prescription'),
            ('pharmacy_change_prescription', 'Can change prescription'),
            ('pharmacy_delete_prescription', 'Can delete prescription'),
        ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    prescribed_date = models.DateTimeField(auto_now_add=True)
    prescribed_by = models.ForeignKey('staff.Staff', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.drug_name} for {self.patient}"
