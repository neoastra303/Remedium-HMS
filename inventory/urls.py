from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('inventory/create/', views.InventoryItemCreateView.as_view(), name='inventoryitem_create'),
    path('inventory/<int:pk>/update/', views.InventoryItemUpdateView.as_view(), name='inventoryitem_update'),
    path('inventory/<int:pk>/delete/', views.InventoryItemDeleteView.as_view(), name='inventoryitem_delete'),
]