from django.shortcuts import render
from django.views import generic
from .models import InventoryItem
from .forms import InventoryItemForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class InventoryItemListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = InventoryItem
    template_name = 'inventory/inventoryitem_list.html'
    context_object_name = 'inventory_items'
    paginate_by = 10  # Add pagination
    permission_required = 'inventory_view_inventoryitem'

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'name') # Default sort by name
        return queryset.order_by(order_by)


class InventoryItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventoryitem_form.html'
    success_url = '/inventory/'
    permission_required = 'inventory_add_inventoryitem'


class InventoryItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventoryitem_form.html'
    success_url = '/inventory/'
    permission_required = 'inventory_change_inventoryitem'


class InventoryItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventoryitem_confirm_delete.html'
    success_url = '/inventory/'
    permission_required = 'inventory_delete_inventoryitem'

# Create your views here.