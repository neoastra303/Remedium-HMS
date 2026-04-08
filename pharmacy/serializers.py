from rest_framework import serializers
from .models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            'id', 'patient', 'drug_name', 'dosage', 'frequency',
            'prescribed_date', 'prescribed_by', 'notes',
        ]
        read_only_fields = ['id', 'prescribed_date']


class DrugInfoSerializer(serializers.Serializer):
    """Serializer for OpenFDA drug label information."""
    generic_name = serializers.CharField(read_only=True)
    brand_name = serializers.CharField(read_only=True)
    manufacturer = serializers.CharField(read_only=True)
    route = serializers.ListField(child=serializers.CharField(), read_only=True)
    substance_name = serializers.ListField(child=serializers.CharField(), read_only=True)
    product_type = serializers.ListField(child=serializers.CharField(), read_only=True)
    warnings = serializers.CharField(read_only=True, allow_blank=True)
    adverse_reactions = serializers.CharField(read_only=True, allow_blank=True)
    dosage_administration = serializers.CharField(read_only=True, allow_blank=True)
    drug_interactions = serializers.CharField(read_only=True, allow_blank=True)
    indications = serializers.CharField(read_only=True, allow_blank=True)


class AdverseEventSerializer(serializers.Serializer):
    """Serializer for OpenFDA adverse event summary."""
    drug_name = serializers.CharField(read_only=True)
    top_adverse_reactions = serializers.ListField(child=serializers.DictField(), read_only=True)
    total_reports = serializers.IntegerField(read_only=True)
