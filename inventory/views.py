from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .models import InventoryItem
from .forms import InventoryItemForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class InventoryItemListView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.ListView
):
    model = InventoryItem
    template_name = "inventory/inventoryitem_list.html"
    context_object_name = "inventory_items"
    paginate_by = 10
    permission_required = "inventory.inventory_view_inventoryitem"
    raise_exception = True

    def get_queryset(self):
        return super().get_queryset().order_by(self.request.GET.get("order_by", "name"))


class InventoryItemDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView
):
    model = InventoryItem
    template_name = "inventory/inventoryitem_detail.html"
    context_object_name = "item"
    permission_required = "inventory.inventory_view_inventoryitem"
    raise_exception = True


class InventoryItemCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/inventoryitem_form.html"
    success_url = reverse_lazy("inventoryitem_list")
    permission_required = "inventory.inventory_add_inventoryitem"
    raise_exception = True


class InventoryItemUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/inventoryitem_form.html"
    success_url = reverse_lazy("inventoryitem_list")
    permission_required = "inventory.inventory_change_inventoryitem"
    raise_exception = True


class InventoryItemDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView
):
    model = InventoryItem
    template_name = "inventory/inventoryitem_confirm_delete.html"
    success_url = reverse_lazy("inventoryitem_list")
    permission_required = "inventory.inventory_delete_inventoryitem"
    raise_exception = True
