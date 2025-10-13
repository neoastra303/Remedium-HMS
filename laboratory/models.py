from django.db import models
from patients.models import Patient


class LabTest(models.Model):
    class Meta:
        app_label = 'laboratory'

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    requested_date = models.DateTimeField(auto_now_add=True)
    result_date = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Requested", "Requested"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Requested",
    )

    def __str__(self):
        return f"{self.test_name} for {self.patient}"
