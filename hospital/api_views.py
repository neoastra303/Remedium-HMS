from rest_framework import viewsets, filters
from .models import Ward, Room
from .serializers import WardSerializer, RoomSerializer
from core.permissions import IsAdminUser


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "capacity"]
    ordering = ["name"]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related("ward").all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["room_number", "ward__name"]
    ordering_fields = ["room_number", "ward__name"]
    ordering = ["ward__name", "room_number"]
