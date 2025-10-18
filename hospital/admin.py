from django.contrib import admin
from .models import Ward, Room

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']
    list_filter = ['capacity']
    search_fields = ['name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['ward', 'room_number', 'capacity']
    list_filter = ['ward', 'capacity']
    search_fields = ['room_number', 'ward__name']