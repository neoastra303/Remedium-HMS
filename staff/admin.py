from django.contrib import admin
from .models import Staff, Shift

class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 1

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'first_name', 'last_name', 'role', 'department', 'is_active')
    list_filter = ('role', 'department', 'is_active')
    search_fields = ('staff_id', 'first_name', 'last_name', 'email')
    inlines = [ShiftInline]

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('staff', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
