from django.urls import path
from . import views

urlpatterns = [
    # Ward URLs
    path('wards/', views.WardListView.as_view(), name='ward_list'),
    path('wards/<int:pk>/', views.WardDetailView.as_view(), name='ward_detail'),
    path('wards/create/', views.WardCreateView.as_view(), name='ward_create'),
    path('wards/<int:pk>/update/', views.WardUpdateView.as_view(), name='ward_update'),
    path('wards/<int:pk>/delete/', views.WardDeleteView.as_view(), name='ward_delete'),
    
    # Room URLs
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/update/', views.RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),
]