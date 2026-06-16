from rest_framework import serializers
from .models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    needs_reorder = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    total_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "name",
            "category",
            "quantity",
            "unit",
            "reorder_level",
            "cost_per_unit",
            "supplier",
            "expiry_date",
            "created_at",
            "updated_at",
            "needs_reorder",
            "is_expired",
            "total_value",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
