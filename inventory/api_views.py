from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from core.permissions import IsAdminUser


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category", "supplier"]
    ordering_fields = ["name", "quantity", "category", "expiry_date"]
    ordering = ["name"]

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """Return items that need reordering."""
        items = [i for i in self.get_queryset() if i.needs_reorder]
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
