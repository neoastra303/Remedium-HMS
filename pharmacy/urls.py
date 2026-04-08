from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('prescriptions/create/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/<int:pk>/update/', views.PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', views.PrescriptionDeleteView.as_view(), name='prescription_delete'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
]