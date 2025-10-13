from django.db import models


class Patient(models.Model):
    class Meta:
        app_label = 'patients'

    unique_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    admission_date = models.DateTimeField(blank=True, null=True)
    discharge_date = models.DateTimeField(blank=True, null=True)
    ward = models.ForeignKey("hospital.Ward", on_delete=models.SET_NULL, blank=True, null=True)
    room = models.ForeignKey("hospital.Room", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.unique_id} - {self.first_name} {self.last_name}"
