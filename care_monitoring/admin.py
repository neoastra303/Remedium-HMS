from django.contrib import admin
from .models import PatientCare


@admin.register(PatientCare)
class PatientCareAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "status",
        "monitoring_date",
        "heart_rate",
        "temperature",
        "oxygen_saturation",
    )
    list_filter = ("status", "monitoring_date")
    search_fields = ("patient__first_name", "patient__last_name")
    date_hierarchy = "monitoring_date"
