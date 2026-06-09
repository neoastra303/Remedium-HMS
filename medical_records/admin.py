from django.contrib import admin
from .models import PatientDocument, Encounter


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ("patient", "encounter_type", "doctor", "start_time", "end_time")
    list_filter = ("encounter_type", "start_time", "doctor")
    search_fields = ("patient__first_name", "patient__last_name", "reason_for_visit")


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "patient", "document_type", "uploaded_at")
    list_filter = ("document_type", "uploaded_at")
    search_fields = ("title", "patient__first_name", "patient__last_name")
