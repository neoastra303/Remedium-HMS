from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Patient
from .serializers import PatientSerializer
from core.permissions import IsClinicalStaff
from core.serializers import StandardErrorSerializer


from django_filters.rest_framework import DjangoFilterBackend


@extend_schema_view(
    list=extend_schema(
        summary="List all patients",
        description="Retrieve a paginated list of all patients in the system.",
    ),
    retrieve=extend_schema(
        summary="Get patient details",
        description="Retrieve detailed information about a specific patient by ID.",
    ),
    create=extend_schema(
        summary="Register new patient",
        description="Create a new patient record in the system.",
    ),
    update=extend_schema(
        summary="Update patient",
        description="Update all fields of an existing patient record.",
    ),
    partial_update=extend_schema(
        summary="Partial update patient",
        description="Update specific fields of an existing patient record.",
    ),
    destroy=extend_schema(
        summary="Delete patient",
        description="Permanently remove a patient record from the system.",
    ),
)
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsClinicalStaff]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["gender", "ward", "room"]
    search_fields = ["unique_id", "first_name", "last_name", "email"]
    ordering_fields = ["admission_date", "first_name", "last_name"]
    ordering = ["-admission_date"]

    @extend_schema(
        summary="List admitted patients",
        description="Retrieve a list of all patients currently admitted to the hospital (those with an admission date but no discharge date).",
        responses={200: PatientSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def admitted_patients(self, request):
        """Get all currently admitted patients."""
        admitted = self.queryset.filter(
            admission_date__isnull=False, discharge_date__isnull=True
        )
        serializer = self.get_serializer(admitted, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Discharge patient",
        description="Mark a patient as discharged. Sets the discharge date to the current time.",
        request=None,
        responses={200: PatientSerializer, 400: StandardErrorSerializer},
    )
    @action(detail=True, methods=["post"])
    def discharge(self, request, pk=None):
        """Discharge a patient."""
        patient = self.get_object()
        if not patient.is_admitted:
            raise ValidationError({"detail": "Patient is not currently admitted."})
        patient.discharge_date = timezone.now()
        patient.save()
        serializer = self.get_serializer(patient)
        return Response(serializer.data)
