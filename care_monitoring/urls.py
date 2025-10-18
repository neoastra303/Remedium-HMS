from django.urls import path
from . import views

app_name = 'care_monitoring'

urlpatterns = [
    path('patientcares/', views.PatientCareListView.as_view(), name='patientcare_list'),
    path('patientcares/<int:pk>/', views.PatientCareDetailView.as_view(), name='patientcare_detail'),
    path('patientcares/create/', views.PatientCareCreateView.as_view(), name='patientcare_create'),
    path('patientcares/<int:pk>/update/', views.PatientCareUpdateView.as_view(), name='patientcare_update'),
    path('patientcares/<int:pk>/delete/', views.PatientCareDeleteView.as_view(), name='patientcare_delete'),
]