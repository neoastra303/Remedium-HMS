from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    path('patients/<int:patient_pk>/documents/upload/', views.PatientDocumentCreateView.as_view(), name='patient_document_upload'),
]
