from django.db import models
from patients.models import Patient


class PatientCare(models.Model):
    class Meta:
        app_label = 'care_monitoring'

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    monitoring_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Care for {self.patient} on {self.monitoring_date}"
