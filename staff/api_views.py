from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Staff
from .serializers import StaffSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['staff_id', 'first_name', 'last_name', 'email', 'role']
    ordering_fields = ['hire_date', 'first_name', 'last_name']
    ordering = ['first_name']

    @action(detail=False, methods=['get'])
    def medical_staff(self, request):
        """Get all medical staff."""
        medical = self.queryset.filter(is_medical_staff=True)
        serializer = self.get_serializer(medical, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Get staff by department."""
        department = request.query_params.get('department')
        if department:
            staff = self.queryset.filter(department=department)
            serializer = self.get_serializer(staff, many=True)
            return Response(serializer.data)
        return Response({'error': 'Department parameter required'}, status=400)
