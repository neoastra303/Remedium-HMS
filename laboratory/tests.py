"""Tests for laboratory app."""
import pytest
from django.utils import timezone
from datetime import timedelta
from laboratory.models import LabTest
from patients.models import Patient


@pytest.mark.django_db
class TestLabTestModel:
    """Test LabTest model."""

    def _create_patient(self):
        return Patient.objects.create(
            unique_id='PAT_LAB',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )

    def test_create_lab_test(self):
        patient = self._create_patient()
        test = LabTest.objects.create(
            patient=patient,
            test_name='Blood Test',
            status='Requested',
        )
        assert test.pk is not None
        assert test.status == 'Requested'
        assert str(test) == 'Blood Test for PAT_LAB - Test Patient'

    def test_lab_test_auto_requested_date(self):
        """Test requested_date is auto-set."""
        patient = self._create_patient()
        test = LabTest(patient=patient, test_name='X-Ray')
        test.save()
        assert test.requested_date is not None

    def test_lab_test_status_choices(self):
        """Test valid status values."""
        patient = self._create_patient()
        for status in ['Requested', 'Completed', 'Cancelled']:
            test = LabTest(
                patient=patient,
                test_name=f'{status} Test',
                status=status,
            )
            test.full_clean()  # Should not raise
