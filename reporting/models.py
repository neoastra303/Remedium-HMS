from django.db import models


class Report(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50)
    data = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.report_type})"


# Create your models here.
