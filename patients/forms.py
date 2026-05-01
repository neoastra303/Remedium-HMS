from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'unique_id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'address', 'phone', 'email', 'insurance_provider',
            'emergency_contact_name', 'emergency_contact_phone',
            'medical_history', 'admission_date', 'discharge_date', 'ward', 'room',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = widget.attrs.get('class', '')
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = f'{css} form-select'.strip()
            elif isinstance(widget, forms.Textarea):
                widget.attrs['class'] = f'{css} form-control'.strip()
            else:
                widget.attrs['class'] = f'{css} form-control'.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Patient.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A patient with this email already exists.")
        return email
