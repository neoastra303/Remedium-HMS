from rest_framework import viewsets, filters, permissions
from .models import LabTest
from .serializers import LabTestSerializer


class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.select_related('patient').all()
    serializer_class = LabTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'test_name']
    ordering_fields = ['requested_date', 'status']
    ordering = ['-requested_date']
