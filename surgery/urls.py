from django.urls import path
from . import views

urlpatterns = [
    path('surgeries/', views.SurgeryListView.as_view(), name='surgery_list'),
    path('surgeries/create/', views.SurgeryCreateView.as_view(), name='surgery_create'),
    path('surgeries/<int:pk>/update/', views.SurgeryUpdateView.as_view(), name='surgery_update'),
    path('surgeries/<int:pk>/delete/', views.SurgeryDeleteView.as_view(), name='surgery_delete'),
    path('surgeries/<int:pk>/', views.SurgeryDetailView.as_view(), name='surgery_detail'),
]