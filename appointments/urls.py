from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
]