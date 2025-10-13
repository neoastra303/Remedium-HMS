from django.urls import path
from . import views

urlpatterns = [
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/create/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/<int:pk>/update/', views.PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', views.PrescriptionDeleteView.as_view(), name='prescription_delete'),
]