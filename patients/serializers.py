from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, BooleanField
from .models import Patient


class PatientBriefSerializer(serializers.ModelSerializer):
    """Non-clinical staff view - excludes sensitive PHI fields."""
    full_name = CharField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'unique_id', 'first_name', 'last_name', 'full_name',
            'gender', 'address', 'phone', 'email',
            'admission_date', 'discharge_date', 'ward', 'room'
        ]
        read_only_fields = ['id', 'full_name']


class PatientFullSerializer(serializers.ModelSerializer):
    """Clinical staff view - includes all fields including PHI."""
    age = IntegerField(read_only=True)
    full_name = CharField(read_only=True)
    is_admitted = BooleanField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'unique_id', 'first_name', 'last_name', 'full_name', 'date_of_birth',
            'age', 'gender', 'address', 'phone', 'email', 'insurance_provider',
            'emergency_contact_name', 'emergency_contact_phone', 'medical_history',
            'admission_date', 'discharge_date', 'is_admitted', 'ward', 'room'
        ]
        read_only_fields = ['id', 'age', 'full_name', 'is_admitted']


# Alias for backward compatibility
PatientSerializer = PatientFullSerializer
