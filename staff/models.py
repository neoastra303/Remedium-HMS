from django.db import models


class Staff(models.Model):
    class Meta:
        app_label = 'staff'

    staff_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    department = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.staff_id} - {self.first_name} {self.last_name} ({self.role})"
