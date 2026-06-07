from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ExternalIntegration
from .serializers import ExternalIntegrationSerializer
from core.permissions import IsAdminUser


class ExternalIntegrationViewSet(viewsets.ModelViewSet):
    queryset = ExternalIntegration.objects.all().order_by('system_name')
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
        except NotImplementedError as e:
            return Response({
                "status": "not_implemented",
                "message": str(e)
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
