from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('integrations/', views.IntegrationListView.as_view(), name='integration_list'),
    path('patients/', views.PatientListAPIView.as_view(), name='patient-list-api'),
    path('integrations/create/', TemplateView.as_view(template_name='integration/integration_form.html'), name='integration_create'),
    path('integrations/<int:pk>/', TemplateView.as_view(template_name='integration/integration_detail.html'), name='integration_detail'),
    path('integrations/<int:pk>/update/', TemplateView.as_view(template_name='integration/integration_form.html'), name='integration_update'),
    path('integrations/<int:pk>/delete/', TemplateView.as_view(template_name='integration/integration_confirm_delete.html'), name='integration_delete'),
]