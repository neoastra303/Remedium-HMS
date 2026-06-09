from rest_framework import serializers
from .models import Ward, Room


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ["id", "name", "capacity"]


class RoomSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = Room
        fields = ["id", "ward", "ward_name", "room_number", "capacity"]
