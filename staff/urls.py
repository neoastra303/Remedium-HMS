from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/toggle/', views.toggle_user_status, name='user_status_toggle'),
    path('users/<int:pk>/reset-password/', views.admin_reset_password, name='user_password_reset'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
    path('staff/<int:staff_pk>/shifts/add/', views.ShiftCreateView.as_view(), name='shift_create'),
    path('shifts/<int:pk>/delete/', views.ShiftDeleteView.as_view(), name='shift_delete'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
]