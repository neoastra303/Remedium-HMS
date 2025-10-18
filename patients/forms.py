from django import forms
from .models import Patient
import re
from datetime import date

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'unique_id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'address', 'phone', 'email', 'insurance_provider', 'emergency_contact_name',
            'emergency_contact_phone', 'medical_history', 'admission_date', 'discharge_date',
            'ward', 'room'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise forms.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Patient.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A patient with this email already exists.")
        return email

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get('emergency_contact_phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise forms.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        admission_date = cleaned_data.get("admission_date")
        discharge_date = cleaned_data.get("discharge_date")

        if admission_date and discharge_date and discharge_date < admission_date:
            raise forms.ValidationError(
                "Discharge date cannot be before the admission date."
            )
