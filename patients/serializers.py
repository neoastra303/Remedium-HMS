from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    is_admitted = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'unique_id', 'first_name', 'last_name', 'full_name', 'date_of_birth', 
            'age', 'gender', 'address', 'phone', 'email', 'insurance_provider',
            'emergency_contact_name', 'emergency_contact_phone', 'medical_history',
            'admission_date', 'discharge_date', 'is_admitted', 'ward', 'room'
        ]
        read_only_fields = ['id', 'age', 'full_name', 'is_admitted']

    def get_age(self, obj):
        return obj.age

    def get_full_name(self, obj):
        return obj.full_name

    def get_is_admitted(self, obj):
        return obj.is_admitted
