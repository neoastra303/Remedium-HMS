from django.contrib import admin
from .models import Surgery


@admin.register(Surgery)
class SurgeryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'surgeon', 'scheduled_date', 'status', 'operating_room')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'surgeon__first_name', 'surgeon__last_name')
    date_hierarchy = 'scheduled_date'
