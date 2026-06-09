from rest_framework import serializers
from .models import ExternalIntegration


class ExternalIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalIntegration
        fields = "__all__"
        extra_kwargs = {"api_key": {"write_only": True}}

    def create(self, validated_data):
        raw_api_key = validated_data.pop("api_key", None)
        integration = ExternalIntegration(**validated_data)
        if raw_api_key:
            integration.set_api_key(raw_api_key)
        integration.save()
        return integration

    def update(self, instance, validated_data):
        raw_api_key = validated_data.pop("api_key", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if raw_api_key:
            instance.set_api_key(raw_api_key)
        instance.save()
        return instance
