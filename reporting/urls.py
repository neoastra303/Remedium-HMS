from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('patient_report/', views.patient_report, name='patient_report'),
    path('reports/create/', views.ReportCreateView.as_view(), name='report_generate'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('reports/<int:pk>/download/', views.download_report, name='report_download'),
]