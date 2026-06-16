from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from core.views import DeleteSuccessMixin, SuccessQueryParamMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics, serializers
from patients.models import Patient
from .models import ExternalIntegration


class IntegrationListView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.ListView
):
    model = ExternalIntegration
    template_name = "integration/integration_list.html"
    context_object_name = "integrations"
    paginate_by = 10
    ordering = ["system_name"]
    permission_required = "integration.view_externalintegration"
    raise_exception = True
    ALLOWED_ORDER_BY = [
        "system_name",
        "system_type",
        "status",
        "last_sync",
        "-system_name",
        "-system_type",
        "-status",
        "-last_sync",
    ]

    def get_queryset(self):
        order_by = self.request.GET.get("order_by", "system_name")
        if order_by not in self.ALLOWED_ORDER_BY:
            order_by = "system_name"
        return super().get_queryset().order_by(order_by)


class IntegrationDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView
):
    model = ExternalIntegration
    template_name = "integration/integration_detail.html"
    context_object_name = "integration"
    permission_required = "integration.view_externalintegration"
    raise_exception = True


class IntegrationCreateView(
    LoginRequiredMixin, PermissionRequiredMixin,
    SuccessQueryParamMixin, SuccessMessageMixin,
    generic.CreateView
):
    model = ExternalIntegration
    fields = ["system_name", "system_type", "api_endpoint", "notes"]
    template_name = "integration/integration_form.html"
    success_url = reverse_lazy("integration_list")
    permission_required = "integration.add_externalintegration"
    raise_exception = True
    success_message = "Integration created successfully."


class IntegrationUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin,
    SuccessQueryParamMixin, SuccessMessageMixin,
    generic.UpdateView
):
    model = ExternalIntegration
    fields = ["system_name", "system_type", "api_endpoint", "notes"]
    template_name = "integration/integration_form.html"
    success_url = reverse_lazy("integration_list")
    permission_required = "integration.change_externalintegration"
    raise_exception = True
    success_query_param = "updated"
    success_message = "Integration updated successfully."


class IntegrationDeleteView(
    DeleteSuccessMixin, LoginRequiredMixin, PermissionRequiredMixin,
    SuccessMessageMixin, generic.DeleteView
):
    model = ExternalIntegration
    template_name = "integration/integration_confirm_delete.html"
    success_url = reverse_lazy("integration_list")
    permission_required = "integration.delete_externalintegration"
    raise_exception = True
    success_message = "Integration deleted successfully."


@login_required
@permission_required("integration.change_externalintegration", raise_exception=True)
def trigger_sync(request, pk):
    integration = get_object_or_404(ExternalIntegration, pk=pk)
    integration.trigger_sync()
    messages.success(request, f"Sync triggered for {integration.system_name}.")
    return redirect("integration_detail", pk=pk)


# DRF views (kept for API compatibility)
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
