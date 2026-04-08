from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('audit-log/', views.audit_log, name='audit_log'),
    path('logout/', views.logout_view, name='logout'),
    path('health/', views.health_check, name='health_check'),
]