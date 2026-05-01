from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PatientCare
from .serializers import PatientCareSerializer
from core.permissions import IsClinicalStaff


class PatientCareViewSet(viewsets.ModelViewSet):
    queryset = PatientCare.objects.select_related('patient', 'monitored_by').all()
    serializer_class = PatientCareSerializer
    permission_classes = [IsClinicalStaff]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'status']
    ordering_fields = ['monitoring_date', 'status']
    ordering = ['-monitoring_date']

    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Return records where patient status is Critical."""
        qs = self.get_queryset().filter(status='CRITICAL')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
