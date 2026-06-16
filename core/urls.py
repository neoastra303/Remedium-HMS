from django.urls import path
from . import views


urlpatterns = [
    path("audit-log/", views.audit_log, name="audit_log"),
    path("logout/", views.logout_view, name="logout"),
]
