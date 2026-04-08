"""Tests for care_monitoring app."""
import pytest
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
from care_monitoring.models import PatientCare
from patients.models import Patient
from staff.models import Staff


@pytest.mark.django_db
class TestPatientCareModel:
    """Test PatientCare model."""

    def _create_patient(self):
        return Patient.objects.create(
            unique_id='PAT_CARE',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )

    def _create_nurse(self):
        return Staff.objects.create(
            staff_id='NRS_CARE',
            first_name='Nurse',
            last_name='Test',
            role='NURSE',
        )

    def test_create_patient_care(self):
        patient = self._create_patient()
        nurse = self._create_nurse()
        care = PatientCare.objects.create(
            patient=patient,
            status='STABLE',
            temperature=Decimal('37.0'),
            heart_rate=72,
            monitored_by=nurse,
        )
        assert care.pk is not None
        assert care.status == 'STABLE'

    def test_blood_pressure_validation(self):
        """Systolic must be higher than diastolic."""
        patient = self._create_patient()
        care = PatientCare(
            patient=patient,
            status='STABLE',
            blood_pressure_systolic=80,
            blood_pressure_diastolic=120,
        )
        with pytest.raises(ValidationError):
            care.full_clean()

    def test_vital_signs_critical(self):
        """Test critical condition detection."""
        patient = self._create_patient()
        # High temperature
        care = PatientCare(
            patient=patient,
            status='CRITICAL',
            temperature=Decimal('41.0'),
        )
        assert care.is_vital_signs_critical is True

        # Normal vitals
        care2 = PatientCare(
            patient=patient,
            status='STABLE',
            temperature=Decimal('37.0'),
            heart_rate=72,
        )
        assert care2.is_vital_signs_critical is False

    def test_bmi_calculation(self):
        """Test BMI calculation."""
        patient = self._create_patient()
        care = PatientCare(
            patient=patient,
            status='STABLE',
            weight=Decimal('70.0'),
            height=Decimal('175.0'),
        )
        care.save()
        assert care.bmi is not None
        assert 22 <= care.bmi <= 23  # Normal BMI range

    def test_status_choices(self):
        """Test valid status values."""
        patient = self._create_patient()
        for status in ['STABLE', 'CRITICAL', 'IMPROVING', 'DETERIORATING', 'DISCHARGED', 'OBSERVATION']:
            care = PatientCare(patient=patient, status=status)
            care.full_clean()  # Should not raise
