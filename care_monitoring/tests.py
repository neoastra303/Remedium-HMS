"""Tests for care_monitoring app REST API."""

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from care_monitoring.models import PatientCare
from patients.models import Patient


def make_admin():
    return User.objects.create_superuser(
        username="care_admin", password="pass", email="c@c.com"
    )


@pytest.fixture
def admin_client():
    client = APIClient()
    client.force_authenticate(user=make_admin())
    return client


@pytest.fixture
def patient():
    return Patient.objects.create(
        unique_id="PAT_CARE",
        first_name="Bob",
        last_name="Jones",
        date_of_birth=timezone.now().date() - timedelta(days=365 * 50),
        gender="M",
    )


@pytest.mark.django_db
class TestPatientCareAPI:
    def test_list_records(self, admin_client, patient):
        PatientCare.objects.create(patient=patient, status="STABLE")
        r = admin_client.get("/api/v1/care-monitoring/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["count"] == 1

    def test_create_record(self, admin_client, patient):
        r = admin_client.post(
            "/api/v1/care-monitoring/",
            {
                "patient": patient.pk,
                "status": "STABLE",
                "heart_rate": 72,
                "temperature": "37.0",
            },
        )
        assert r.status_code == status.HTTP_201_CREATED

    def test_critical_action(self, admin_client, patient):
        PatientCare.objects.create(patient=patient, status="CRITICAL")
        PatientCare.objects.create(patient=patient, status="STABLE")
        r = admin_client.get("/api/v1/care-monitoring/critical/")
        assert r.status_code == status.HTTP_200_OK
        assert all(rec["status"] == "CRITICAL" for rec in r.data)

    def test_serializer_computed_fields(self, admin_client, patient):
        PatientCare.objects.create(
            patient=patient,
            status="STABLE",
            weight="70.0",
            height="175.0",
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
        )
        r = admin_client.get("/api/v1/care-monitoring/")
        rec = r.data["results"][0]
        assert rec["blood_pressure"] == "120/80"
        assert rec["bmi"] is not None
        assert rec["patient_name"] == "Bob Jones"

    def test_invalid_bp_rejected(self, admin_client, patient):
        # systolic must be > diastolic
        r = admin_client.post(
            "/api/v1/care-monitoring/",
            {
                "patient": patient.pk,
                "status": "STABLE",
                "blood_pressure_systolic": 70,
                "blood_pressure_diastolic": 90,
            },
        )
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthenticated_denied(self):
        r = APIClient().get("/api/v1/care-monitoring/")
        assert r.status_code == status.HTTP_401_UNAUTHORIZED
