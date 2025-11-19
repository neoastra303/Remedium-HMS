from rest_framework import serializers
from .models import Appointment
from patients.serializers import PatientSerializer
from staff.serializers import StaffSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = StaffSerializer(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_detail', 'doctor', 'doctor_detail',
            'appointment_date', 'reason', 'status'
        ]
        read_only_fields = ['id']
