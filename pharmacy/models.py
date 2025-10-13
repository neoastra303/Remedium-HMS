from django.db import models
from patients.models import Patient


class Prescription(models.Model):
    class Meta:
        app_label = 'pharmacy'

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    prescribed_date = models.DateTimeField(auto_now_add=True)
    prescribed_by = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.drug_name} for {self.patient}"
