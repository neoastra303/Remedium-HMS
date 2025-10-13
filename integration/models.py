from django.db import models


class ExternalIntegration(models.Model):
    system_name = models.CharField(max_length=100)
    api_endpoint = models.URLField()
    last_sync = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Integration with {self.system_name}"


# Create your models here.
