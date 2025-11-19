from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name']
    ordering_fields = ['appointment_date', 'status']
    ordering = ['-appointment_date']

    @action(detail=False, methods=['get'])
    def scheduled(self, request):
        """Get all scheduled appointments."""
        scheduled = self.queryset.filter(status='Scheduled')
        serializer = self.get_serializer(scheduled, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments."""
        now = timezone.now()
        upcoming = self.queryset.filter(
            appointment_date__gte=now,
            status='Scheduled'
        ).order_by('appointment_date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
