from django import forms
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['staff_id', 'first_name', 'last_name', 'role', 'department', 'phone', 'email', 'schedule']
