from django import forms
from .models import Surgery

class SurgeryForm(forms.ModelForm):
    class Meta:
        model = Surgery
        fields = '__all__'
