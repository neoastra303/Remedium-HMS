from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Prescription
from .serializers import PrescriptionSerializer, DrugInfoSerializer, AdverseEventSerializer
from .openfda_service import search_drug_label, search_adverse_events


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    Manage prescriptions and access drug information.

    list: Return all prescriptions.
    retrieve: Return a specific prescription.
    drug_info: Return FDA drug label information for a medication.
    adverse_events: Return FDA adverse event summary for a medication.
    """
    queryset = Prescription.objects.select_related('patient', 'prescribed_by').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'drug_name']
    ordering_fields = ['prescribed_date']
    ordering = ['-prescribed_date']

    @action(detail=False, methods=['get'], url_path='drug-info')
    def drug_info(self, request):
        """
        Get FDA drug label information from OpenFDA.

        Query parameter `q` is required (drug name).

        Returns generic name, brand names, manufacturer, warnings,
        adverse reactions, dosage info, and drug interactions.
        """
        drug_name = request.query_params.get('q', '').strip()
        if not drug_name:
            return Response(
                {'error': 'Query parameter "q" (drug name) is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = search_drug_label(drug_name)
        if 'error' in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        serializer = DrugInfoSerializer(result)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='adverse-events')
    def adverse_events(self, request):
        """
        Get FDA adverse event report summary for a medication from OpenFDA.

        Query parameter `q` is required (drug name).

        Returns the top 10 most reported adverse reactions and total report count.
        """
        drug_name = request.query_params.get('q', '').strip()
        if not drug_name:
            return Response(
                {'error': 'Query parameter "q" (drug name) is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = search_adverse_events(drug_name)
        if 'error' in result:
            return Response(result, status=status.HTTP_502_BAD_GATEWAY)

        serializer = AdverseEventSerializer(result)
        return Response(serializer.data)
