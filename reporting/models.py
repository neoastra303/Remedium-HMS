from django.db import models


class Report(models.Model):
    class Meta:
        permissions = [
            ('reporting_view_report', 'Can view report'),
            ('reporting_add_report', 'Can add report'),
            ('reporting_change_report', 'Can change report'),
            ('reporting_delete_report', 'Can delete report'),
        ]

    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50)
    data = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.report_type})"


# Create your models here.
