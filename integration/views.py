from django.shortcuts import render
from rest_framework import generics
from django.views import generic
from patients.models import Patient
from .models import ExternalIntegration # Assuming an Integration model exists
from rest_framework import serializers

class IntegrationListView(generic.ListView):
    model = ExternalIntegration
    template_name = 'integration/integration_list.html'
    context_object_name = 'integrations'
    paginate_by = 10  # Add pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'system_name') # Default sort by name
        return queryset.order_by(order_by)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# Create your views here.
