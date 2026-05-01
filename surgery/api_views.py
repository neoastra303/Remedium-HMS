from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Surgery
from .serializers import SurgerySerializer
from core.permissions import IsAdminOrDoctor


class SurgeryViewSet(viewsets.ModelViewSet):
    queryset = Surgery.objects.select_related('patient', 'surgeon').all()
    serializer_class = SurgerySerializer
    permission_classes = [IsAdminOrDoctor]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['procedure', 'operating_room', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['scheduled_date', 'status', 'procedure']
    ordering = ['-scheduled_date']

    @action(detail=False, methods=['get'])
    def scheduled(self, request):
        """Return all scheduled (upcoming) surgeries."""
        qs = self.get_queryset().filter(status='Scheduled')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
