from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'full_name', 'gender', 'age', 'phone', 'is_admitted', 'admission_date']
    list_filter = ['gender', 'admission_date', 'ward', 'insurance_provider']
    search_fields = ['unique_id', 'first_name', 'last_name', 'phone', 'email']
    date_hierarchy = 'admission_date'
    list_per_page = 25
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('unique_id', 'first_name', 'last_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'insurance_provider')
        }),
        ('Hospital Stay', {
            'fields': ('admission_date', 'discharge_date', 'ward', 'room')
        }),
    )
    
    readonly_fields = ['age']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Age'
    
    def is_admitted(self, obj):
        return obj.is_admitted
    is_admitted.boolean = True
    is_admitted.short_description = 'Currently Admitted'
