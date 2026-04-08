from django.db import models
from patients.models import Patient
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# 10 MB file size limit
MAX_FILE_SIZE = 10 * 1024 * 1024


class PatientDocument(models.Model):
    DOCUMENT_TYPES = [
        ('LAB_REPORT', 'Lab Report'),
        ('XRAY', 'X-Ray'),
        ('MRI', 'MRI Scan'),
        ('PRESCRIPTION', 'Prescription'),
        ('INSURANCE', 'Insurance Document'),
        ('OTHER', 'Other'),
    ]

    class Meta:
        app_label = 'medical_records'
        permissions = [
            ('medical_records_view_document', 'Can view document'),
            ('medical_records_add_document', 'Can add document'),
            ('medical_records_change_document', 'Can change document'),
            ('medical_records_delete_document', 'Can delete document'),
        ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='patient_documents/%Y/%m/%d/',
        # Removed .doc/.docx - potential macro security risk
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    # Generic foreign key to link to related entities (LabTest, Prescription, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    history = HistoricalRecords()

    def clean(self):
        super().clean()
        # Validate file size (10 MB limit)
        if self.file and hasattr(self.file, 'size') and self.file.size > MAX_FILE_SIZE:
            raise ValidationError({
                'file': f'File size must be under {MAX_FILE_SIZE / (1024 * 1024)} MB. Current size: {self.file.size / (1024 * 1024):.1f} MB'
            })

    def __str__(self):
        return f"{self.title} - {self.patient.full_name}"
