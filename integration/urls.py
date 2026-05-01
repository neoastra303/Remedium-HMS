from django.urls import path
from . import views

app_name = 'integration'

urlpatterns = [
    path('integrations/', views.IntegrationListView.as_view(), name='integration_list'),
    path('integrations/create/', views.IntegrationCreateView.as_view(), name='integration_create'),
    path('integrations/<int:pk>/', views.IntegrationDetailView.as_view(), name='integration_detail'),
    path('integrations/<int:pk>/update/', views.IntegrationUpdateView.as_view(), name='integration_update'),
    path('integrations/<int:pk>/delete/', views.IntegrationDeleteView.as_view(), name='integration_delete'),
    path('integrations/<int:pk>/sync/', views.trigger_sync, name='integration_sync'),
]
