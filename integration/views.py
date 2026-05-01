from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics, serializers
from patients.models import Patient
from .models import ExternalIntegration


class IntegrationListView(LoginRequiredMixin, generic.ListView):
    model = ExternalIntegration
    template_name = 'integration/integration_list.html'
    context_object_name = 'integrations'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by(self.request.GET.get('order_by', 'system_name'))


class IntegrationDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExternalIntegration
    template_name = 'integration/integration_detail.html'
    context_object_name = 'integration'


class IntegrationCreateView(LoginRequiredMixin, generic.CreateView):
    model = ExternalIntegration
    fields = ['system_name', 'system_type', 'api_endpoint', 'notes']
    template_name = 'integration/integration_form.html'
    success_url = reverse_lazy('integration_list')


class IntegrationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ExternalIntegration
    fields = ['system_name', 'system_type', 'api_endpoint', 'notes']
    template_name = 'integration/integration_form.html'
    success_url = reverse_lazy('integration_list')


class IntegrationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ExternalIntegration
    template_name = 'integration/integration_confirm_delete.html'
    success_url = reverse_lazy('integration_list')


def trigger_sync(request, pk):
    integration = get_object_or_404(ExternalIntegration, pk=pk)
    integration.trigger_sync()
    messages.success(request, f"Sync triggered for {integration.system_name}.")
    return redirect('integration_detail', pk=pk)


# DRF views (kept for API compatibility)
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
