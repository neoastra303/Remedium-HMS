"""Tests for surgery app."""
import pytest
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from surgery.models import Surgery
from patients.models import Patient
from staff.models import Staff


@pytest.mark.django_db
class TestSurgeryModel:
    """Test Surgery model."""

    def _create_patient(self):
        return Patient.objects.create(
            unique_id='PAT_SURG',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )

    def _create_surgeon(self):
        return Staff.objects.create(
            staff_id='DOC_SURG',
            first_name='Dr. Surgeon',
            last_name='Test',
            role='SURGEON',
        )

    def test_create_surgery(self):
        patient = self._create_patient()
        surgeon = self._create_surgeon()
        surgery = Surgery.objects.create(
            patient=patient,
            surgeon=surgeon,
            scheduled_date=timezone.now() + timedelta(days=7),
            operating_room='OR-1',
            procedure='Appendectomy',
        )
        assert surgery.pk is not None
        assert surgery.status == 'Scheduled'

    def test_surgery_status_choices(self):
        """Test valid status values."""
        patient = self._create_patient()
        surgeon = self._create_surgeon()
        for status in ['Scheduled', 'Completed', 'Cancelled']:
            surgery = Surgery(
                patient=patient,
                surgeon=surgeon,
                scheduled_date=timezone.now() + timedelta(days=1),
                operating_room='OR-2',
                procedure='Test',
                status=status,
            )
            surgery.full_clean()  # Should not raise

    def test_unique_operating_room_schedule(self):
        """Test room cannot be double-booked at exact same datetime."""
        patient = self._create_patient()
        surgeon = self._create_surgeon()
        fixed_datetime = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=10)
        Surgery.objects.create(
            patient=patient,
            surgeon=surgeon,
            scheduled_date=fixed_datetime,
            operating_room='OR-3',
            procedure='Test 1',
        )
        patient2 = Patient.objects.create(
            unique_id='PAT_SURG2',
            first_name='Second',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 25),
            gender='F',
        )
        with pytest.raises(Exception):  # IntegrityError
            Surgery.objects.create(
                patient=patient2,
                surgeon=surgeon,
                scheduled_date=fixed_datetime,  # Exact same datetime
                operating_room='OR-3',
                procedure='Test 2',
            )

    def test_surgery_str_representation(self):
        """Test string representation."""
        patient = self._create_patient()
        surgeon = self._create_surgeon()
        surgery = Surgery(
            patient=patient,
            surgeon=surgeon,
            scheduled_date=timezone.now() + timedelta(days=7),
            operating_room='OR-1',
            procedure='Appendectomy',
        )
        assert 'Appendectomy' in str(surgery) or 'Surgery' in str(surgery)
