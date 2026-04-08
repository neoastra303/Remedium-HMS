"""Tests for appointments app."""
import pytest
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from appointments.models import Appointment
from patients.models import Patient
from staff.models import Staff


@pytest.mark.django_db
class TestAppointmentModel:
    """Test Appointment model."""

    def _create_patient(self):
        """Helper to create a test patient."""
        return Patient.objects.create(
            unique_id="PAT_APPT",
            first_name="Test",
            last_name="Patient",
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender="M",
        )

    def _create_doctor(self):
        """Helper to create a test doctor."""
        return Staff.objects.create(
            staff_id="DOC001",
            first_name="Dr. Test",
            last_name="Doctor",
            role="Doctor",
        )

    def test_create_appointment(self):
        """Test basic appointment creation."""
        patient = self._create_patient()
        doctor = self._create_doctor()
        appt = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=timezone.now() + timedelta(days=1),
            reason="Checkup",
        )
        assert appt.pk is not None
        assert appt.status == "Scheduled"

    def test_appointment_str(self):
        """Test string representation."""
        patient = self._create_patient()
        doctor = self._create_doctor()
        appt = Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=timezone.now() + timedelta(days=1),
        )
        assert str(appt)

    def test_past_appointment_raises_error(self):
        """Test creating appointment in the past raises error."""
        patient = self._create_patient()
        doctor = self._create_doctor()
        appt = Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=timezone.now() - timedelta(days=1),
        )
        with pytest.raises(ValidationError):
            appt.full_clean()

    def test_status_choices(self):
        """Test status field accepts valid choices."""
        patient = self._create_patient()
        doctor = self._create_doctor()
        for status in ["Scheduled", "Completed", "Cancelled"]:
            appt = Appointment(
                patient=patient,
                doctor=doctor,
                appointment_date=timezone.now() + timedelta(days=1),
                status=status,
            )
            appt.full_clean()  # Should not raise
