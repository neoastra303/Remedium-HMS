from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'drug_name', 'dosage', 'frequency', 'prescribed_by', 'notes']
