from django.urls import path
from . import views


urlpatterns = [
    path(
        "patients/<int:patient_pk>/documents/",
        views.PatientDocumentListView.as_view(),
        name="patient_document_list",
    ),
    path(
        "patients/<int:patient_pk>/documents/upload/",
        views.PatientDocumentCreateView.as_view(),
        name="patient_document_upload",
    ),
    path(
        "encounters/create/",
        views.EncounterCreateView.as_view(),
        name="encounter_create",
    ),
    path(
        "encounters/<int:pk>/",
        views.EncounterDetailView.as_view(),
        name="encounter_detail",
    ),
    path(
        "encounters/<int:pk>/update/",
        views.EncounterUpdateView.as_view(),
        name="encounter_update",
    ),
    path(
        "encounters/<int:pk>/delete/",
        views.EncounterDeleteView.as_view(),
        name="encounter_delete",
    ),
]
