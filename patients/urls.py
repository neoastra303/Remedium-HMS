from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('patients/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/update/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('patients/<int:pk>/history/', views.PatientHistoryView.as_view(), name='patient_history'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
]