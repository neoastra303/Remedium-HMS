from django.db import models
from patients.models import Patient
from staff.models import Staff


class Appointment(models.Model):
    class Meta:
        app_label = 'appointments'
        permissions = [
            ('appointments_view_appointment', 'Can view appointment'),
            ('appointments_add_appointment', 'Can add appointment'),
            ('appointments_change_appointment', 'Can change appointment'),
            ('appointments_delete_appointment', 'Can delete appointment'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['patient', 'doctor', 'appointment_date'], name='unique_appointment')
        ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey("staff.Staff", on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Scheduled", "Scheduled"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Scheduled",
    )

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date}"