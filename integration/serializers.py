from rest_framework import serializers
from .models import ExternalIntegration


class ExternalIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalIntegration
        fields = '__all__'
        extra_kwargs = {
            'api_key': {'write_only': True}
        }
