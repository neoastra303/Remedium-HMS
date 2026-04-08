from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import ExternalIntegration
from .serializers import ExternalIntegrationSerializer


class ExternalIntegrationViewSet(viewsets.ModelViewSet):
    queryset = ExternalIntegration.objects.all()
    serializer_class = ExternalIntegrationSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Trigger a manual synchronization for this integration."""
        integration = self.get_object()
        try:
            integration.trigger_sync()
            return Response({
                "status": "success",
                "message": f"Sync triggered for {integration.system_name}",
                "last_sync": integration.last_sync
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
