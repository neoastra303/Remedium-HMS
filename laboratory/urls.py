from django.urls import path
from . import views

urlpatterns = [
    path('labtests/', views.LabTestListView.as_view(), name='labtest_list'),
    path('labtests/create/', views.LabTestCreateView.as_view(), name='labtest_create'),
    path('labtests/<int:pk>/update/', views.LabTestUpdateView.as_view(), name='labtest_update'),
    path('labtests/<int:pk>/delete/', views.LabTestDeleteView.as_view(), name='labtest_delete'),
    path('labtests/<int:pk>/', views.LabTestDetailView.as_view(), name='labtest_detail'),
]