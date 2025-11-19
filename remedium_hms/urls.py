from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients.api_views import PatientViewSet
from staff.api_views import StaffViewSet
from appointments.api_views import AppointmentViewSet
from billing.api_views import InvoiceViewSet

# API Router
api_router = DefaultRouter()
api_router.register(r'patients', PatientViewSet, basename='patient')
api_router.register(r'staff', StaffViewSet, basename='staff')
api_router.register(r'appointments', AppointmentViewSet, basename='appointment')
api_router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("api/", include(api_router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("core.urls")), # Include core app urls
    path("", include("patients.urls")), # Include patients app urls
    path("", include("staff.urls")),  # Include staff app urls
    path("", include("appointments.urls")), # Include appointments app urls
    path("", include("billing.urls")), # Include billing app urls
    path("", include("inventory.urls")), # Include inventory app urls
    path("", include("laboratory.urls")), # Include laboratory app urls
    path("", include("pharmacy.urls")), # Include pharmacy app urls
    path("", include("hospital.urls")), # Include hospital app urls
    path("", include("reporting.urls")), # Include reporting app urls
    path("", include("integration.urls")), # Include integration app urls
    path("", include("surgery.urls")), # Include surgery app urls
    path("", include("care_monitoring.urls")), # Include care_monitoring app urls
]