from django.db import models


class InventoryItem(models.Model):
    class Meta:
        app_label = 'inventory'

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    reorder_level = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
