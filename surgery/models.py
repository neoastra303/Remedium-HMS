from django.db import models
from patients.models import Patient
from staff.models import Staff


class Surgery(models.Model):
    class Meta:
        app_label = 'surgery'

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    surgeon = models.ForeignKey('staff.Staff', on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    operating_room = models.CharField(max_length=50)
    procedure = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Scheduled", "Scheduled"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Scheduled",
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Surgery for {self.patient} by {self.surgeon} on {self.scheduled_date}"
