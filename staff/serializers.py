from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_medical_staff = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = [
            'id', 'staff_id', 'first_name', 'last_name', 'full_name', 'role',
            'department', 'phone', 'email', 'schedule', 'hire_date', 'is_active',
            'is_medical_staff'
        ]
        read_only_fields = ['id', 'full_name', 'is_medical_staff', 'hire_date']

    def get_full_name(self, obj):
        return obj.full_name

    def get_is_medical_staff(self, obj):
        return obj.is_medical_staff
