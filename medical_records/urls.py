from django.urls import path
from . import views


urlpatterns = [
    path('patients/<int:patient_pk>/documents/', views.PatientDocumentListView.as_view(), name='patient_document_list'),
    path('patients/<int:patient_pk>/documents/upload/', views.PatientDocumentCreateView.as_view(), name='patient_document_upload'),
]
