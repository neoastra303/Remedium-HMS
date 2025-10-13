from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
]