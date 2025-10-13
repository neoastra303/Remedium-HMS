from django.urls import path
from . import views

urlpatterns = [
    path('patient_report/', views.patient_report, name='patient_report'),
]