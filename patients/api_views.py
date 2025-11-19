from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['unique_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['admission_date', 'first_name', 'last_name']
    ordering = ['-admission_date']

    @action(detail=False, methods=['get'])
    def admitted_patients(self, request):
        """Get all currently admitted patients."""
        admitted = self.queryset.filter(admission_date__isnull=False, discharge_date__isnull=True)
        serializer = self.get_serializer(admitted, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def discharge(self, request, pk=None):
        """Discharge a patient."""
        patient = self.get_object()
        patient.discharge_date = timezone.now()
        patient.save()
        serializer = self.get_serializer(patient)
        return Response(serializer.data)
