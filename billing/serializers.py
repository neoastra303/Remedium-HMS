from rest_framework import serializers
from .models import Invoice
from patients.serializers import PatientSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'patient', 'patient_detail', 'issue_date', 'due_date',
            'total_amount', 'paid', 'insurance_claimed', 'details'
        ]
        read_only_fields = ['id']
