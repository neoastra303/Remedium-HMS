from django.db import models
from django.core.exceptions import ValidationError

class Ward(models.Model):
    class Meta:
        app_label = 'hospital'
        permissions = [
            ('hospital_view_ward', 'Can view ward'),
            ('hospital_add_ward', 'Can add ward'),
            ('hospital_change_ward', 'Can change ward'),
            ('hospital_delete_ward', 'Can delete ward'),
        ]

    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()

    def clean(self):
        super().clean()
        if self.capacity and self.capacity <= 0:
            raise ValidationError("Capacity must be a positive number.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Room(models.Model):
    class Meta:
        app_label = 'hospital'
        permissions = [
            ('hospital_view_room', 'Can view room'),
            ('hospital_add_room', 'Can add room'),
            ('hospital_change_room', 'Can change room'),
            ('hospital_delete_room', 'Can delete room'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['ward', 'room_number'], name='unique_room_per_ward')
        ]

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()

    def clean(self):
        super().clean()
        if self.capacity and self.capacity <= 0:
            raise ValidationError("Capacity must be a positive number.")
        if not self.room_number or not self.room_number.strip():
            raise ValidationError("Room number cannot be empty.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ward.name} - Room {self.room_number}'


class HospitalService(models.Model):
    """
    Centralized catalog of all billable services, tests, and procedures.
    Allows for flexible pricing and categorization.
    """
    SERVICE_CATEGORIES = [
        ('CONSULTATION', 'Consultation'),
        ('LABORATORY', 'Laboratory Test'),
        ('RADIOLOGY', 'Radiology/Imaging'),
        ('SURGERY', 'Surgical Procedure'),
        ('ACCOMMODATION', 'Ward/Room Charge'),
        ('PHARMACY', 'Medication/Pharmacy'),
        ('OTHER', 'Other Services'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hospital Service"
        verbose_name_plural = "Hospital Services"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"