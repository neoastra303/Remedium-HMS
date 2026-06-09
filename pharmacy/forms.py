from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'service', 'drug_name', 'status', 'dosage', 'frequency', 'prescribed_by', 'notes']
