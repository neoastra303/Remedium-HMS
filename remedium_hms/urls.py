from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# API ViewSets
from patients.api_views import PatientViewSet
from staff.api_views import StaffViewSet
from appointments.api_views import AppointmentViewSet
from billing.api_views import InvoiceViewSet
from integration.api_views import ExternalIntegrationViewSet
from laboratory.api_views import LabTestViewSet
from pharmacy.api_views import PrescriptionViewSet
from hospital.api_views import WardViewSet, RoomViewSet
from inventory.api_views import InventoryItemViewSet
from surgery.api_views import SurgeryViewSet
from care_monitoring.api_views import PatientCareViewSet

# Views for root-level URL aliases (non-namespaced names used in templates)
from core.views import homepage
from patients.views import PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView, PatientHistoryView
from appointments.views import AppointmentListView
from staff.views import StaffListView
from laboratory.views import LabTestListView
from surgery.views import SurgeryListView
from inventory.views import InventoryItemListView
from pharmacy.views import PrescriptionListView
from billing.views import InvoiceListView
from integration.views import IntegrationListView
from reporting.views import ReportListView
from notifications.views import NotificationListView
from medical_records.views import PatientDocumentListView

# API Router
api_router = DefaultRouter()
api_router.register(r'patients', PatientViewSet, basename='patient')
api_router.register(r'staff', StaffViewSet, basename='staff')
api_router.register(r'appointments', AppointmentViewSet, basename='appointment')
api_router.register(r'invoices', InvoiceViewSet, basename='invoice')
api_router.register(r'integrations', ExternalIntegrationViewSet, basename='integration')
api_router.register(r'lab-tests', LabTestViewSet, basename='labtest')
api_router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
api_router.register(r'wards', WardViewSet, basename='ward')
api_router.register(r'rooms', RoomViewSet, basename='room')
api_router.register(r'inventory', InventoryItemViewSet, basename='inventory')
api_router.register(r'surgeries', SurgeryViewSet, basename='surgery')
api_router.register(r'care-monitoring', PatientCareViewSet, basename='care-monitoring')

urlpatterns = [
    # ── Root-level aliases so templates can use {% url 'name' %} without namespace ──
    path("", homepage, name='home'),
    path("patients/", PatientListView.as_view(), name='patient_list'),
    path("patients/<int:pk>/", PatientDetailView.as_view(), name='patient_detail'),
    path("patients/create/", PatientCreateView.as_view(), name='patient_create'),
    path("patients/<int:pk>/update/", PatientUpdateView.as_view(), name='patient_update'),
    path("patients/<int:pk>/delete/", PatientDeleteView.as_view(), name='patient_delete'),
    path("patients/<int:pk>/history/", PatientHistoryView.as_view(), name='patient_history'),
    path("appointments/", AppointmentListView.as_view(), name='appointment_list'),
    path("staff/", StaffListView.as_view(), name='staff_list'),
    path("labtests/", LabTestListView.as_view(), name='labtest_list'),
    path("surgeries/", SurgeryListView.as_view(), name='surgery_list'),
    path("inventory/", InventoryItemListView.as_view(), name='inventoryitem_list'),
    path("prescriptions/", PrescriptionListView.as_view(), name='prescription_list'),
    path("invoices/", InvoiceListView.as_view(), name='invoice_list'),
    path("integrations/", IntegrationListView.as_view(), name='integration_list'),
    path("reports/", ReportListView.as_view(), name='report_list'),
    path("notifications/", NotificationListView.as_view(), name='notification_list'),
    path("patients/<int:patient_pk>/documents/", PatientDocumentListView.as_view(), name='patient_document_list'),

    # ── Django built-ins ──
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("api-auth/", include("rest_framework.urls")),

    # ── REST API ──
    path("api/v1/", include(api_router.urls)),
    path("api/v1/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name='token_verify'),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name='schema'),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ── App URL includes (namespaced, for {% url 'app:name' %} usage) ──
    path("", include("core.urls")),
    path("", include("patients.urls")),
    path("", include("staff.urls")),
    path("", include("appointments.urls")),
    path("", include("billing.urls")),
    path("", include("inventory.urls")),
    path("", include("laboratory.urls")),
    path("", include("pharmacy.urls")),
    path("", include("hospital.urls")),
    path("", include("reporting.urls")),
    path("", include("integration.urls")),
    path("", include("surgery.urls")),
    path("", include("medical_records.urls")),
    path("", include("notifications.urls")),
    path("", include("care_monitoring.urls")),
]
