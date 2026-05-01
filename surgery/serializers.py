from rest_framework import serializers
from .models import Surgery


class SurgerySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    surgeon_name = serializers.CharField(source='surgeon.__str__', read_only=True)

    class Meta:
        model = Surgery
        fields = [
            'id', 'patient', 'patient_name', 'surgeon', 'surgeon_name',
            'scheduled_date', 'operating_room', 'procedure', 'status', 'notes',
        ]
        read_only_fields = ['id']
