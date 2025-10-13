"""
URL configuration for remedium_hms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("patients.urls")), # Include patients app urls
    path("", include("staff.urls")),  # Include staff app urls
    path("", include("appointments.urls")), # Include appointments app urls
    path("", include("billing.urls")), # Include billing app urls
    path("", include("inventory.urls")), # Include inventory app urls
    path("", include("laboratory.urls")), # Include laboratory app urls
    path("", include("pharmacy.urls")), # Include pharmacy app urls
    path("", include("reporting.urls")), # Include reporting app urls
    path("", include("integration.urls")), # Include integration app urls
    path("", include("surgery.urls")), # Include surgery app urls
]

