from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/update/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
]