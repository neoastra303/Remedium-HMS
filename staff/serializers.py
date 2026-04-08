from rest_framework import serializers
from rest_framework.fields import CharField, BooleanField
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    full_name = CharField(read_only=True)
    is_medical_staff = BooleanField(read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id', 'staff_id', 'first_name', 'last_name', 'full_name', 'role',
            'department', 'phone', 'email', 'schedule', 'hire_date', 'is_active',
            'is_medical_staff'
        ]
        read_only_fields = ['id', 'full_name', 'is_medical_staff', 'hire_date']
