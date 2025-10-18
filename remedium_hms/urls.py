from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
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