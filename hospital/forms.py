from django import forms
from .models import Ward, Room

class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['name', 'capacity']

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity <= 0:
            raise forms.ValidationError("Capacity must be a positive number.")
        return capacity


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['ward', 'room_number', 'capacity']

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity <= 0:
            raise forms.ValidationError("Capacity must be a positive number.")
        return capacity

    def clean_room_number(self):
        room_number = self.cleaned_data.get('room_number')
        if not room_number or not room_number.strip():
            raise forms.ValidationError("Room number cannot be empty.")
        return room_number