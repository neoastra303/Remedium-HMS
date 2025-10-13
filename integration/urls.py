from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.PatientListAPIView.as_view(), name='patient-list-api'),
]