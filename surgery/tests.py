"""Tests for surgery app REST API."""
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from surgery.models import Surgery
from patients.models import Patient
from staff.models import Staff


def make_admin():
    return User.objects.create_superuser(username='surg_admin', password='pass', email='s@s.com')


@pytest.fixture
def admin_client():
    client = APIClient()
    client.force_authenticate(user=make_admin())
    return client


@pytest.fixture
def patient():
    return Patient.objects.create(
        unique_id='PAT_SURG', first_name='Jane', last_name='Doe',
        date_of_birth=timezone.now().date() - timedelta(days=365 * 40), gender='F',
    )


@pytest.fixture
def surgeon():
    return Staff.objects.create(staff_id='SURG01', first_name='Dr', last_name='Smith', role='SURGEON')


@pytest.mark.django_db
class TestSurgeryAPI:
    def test_list_surgeries(self, admin_client, patient, surgeon):
        Surgery.objects.create(
            patient=patient, surgeon=surgeon,
            scheduled_date=timezone.now() + timedelta(days=1),
            operating_room='OR-1', procedure='Appendectomy',
        )
        r = admin_client.get('/api/v1/surgeries/')
        assert r.status_code == status.HTTP_200_OK
        assert r.data['count'] == 1

    def test_create_surgery(self, admin_client, patient, surgeon):
        r = admin_client.post('/api/v1/surgeries/', {
            'patient': patient.pk,
            'surgeon': surgeon.pk,
            'scheduled_date': (timezone.now() + timedelta(days=2)).isoformat(),
            'operating_room': 'OR-2',
            'procedure': 'Cholecystectomy',
            'status': 'Scheduled',
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_scheduled_action(self, admin_client, patient, surgeon):
        Surgery.objects.create(
            patient=patient, surgeon=surgeon,
            scheduled_date=timezone.now() + timedelta(days=1),
            operating_room='OR-3', procedure='Hip Replacement', status='Scheduled',
        )
        Surgery.objects.create(
            patient=patient, surgeon=surgeon,
            scheduled_date=timezone.now() - timedelta(days=1),
            operating_room='OR-4', procedure='Old Surgery', status='Completed',
        )
        r = admin_client.get('/api/v1/surgeries/scheduled/')
        assert r.status_code == status.HTTP_200_OK
        assert all(s['status'] == 'Scheduled' for s in r.data)

    def test_serializer_includes_patient_name(self, admin_client, patient, surgeon):
        Surgery.objects.create(
            patient=patient, surgeon=surgeon,
            scheduled_date=timezone.now() + timedelta(days=1),
            operating_room='OR-5', procedure='Test',
        )
        r = admin_client.get('/api/v1/surgeries/')
        assert r.data['results'][0]['patient_name'] == 'Jane Doe'

    def test_unauthenticated_denied(self):
        r = APIClient().get('/api/v1/surgeries/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED
