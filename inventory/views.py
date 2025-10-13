from django.shortcuts import render
from django.views import generic
from .models import InventoryItem


class InventoryItemListView(generic.ListView):
    model = InventoryItem
    template_name = 'inventory/inventoryitem_list.html'
    context_object_name = 'inventory_items'


class InventoryItemCreateView(generic.CreateView):
    model = InventoryItem
    fields = '__all__'
    template_name = 'inventory/inventoryitem_form.html'
    success_url = '/inventory/'


class InventoryItemUpdateView(generic.UpdateView):
    model = InventoryItem
    fields = '__all__'
    template_name = 'inventory/inventoryitem_form.html'
    success_url = '/inventory/'


class InventoryItemDeleteView(generic.DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventoryitem_confirm_delete.html'
    success_url = '/inventory/'

# Create your views here.
