from django import forms
from .models import Appointment
from django.utils import timezone


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date and appointment_date < timezone.now():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return appointment_date

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")

        if doctor and appointment_date:
            if Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    "This doctor is already booked for this time slot."
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].required = True
        self.fields['doctor'].required = True
        self.fields['appointment_date'].required = True
        # Reason is optional in the model, but we can make it required in the form if needed
        # self.fields['reason'].required = True