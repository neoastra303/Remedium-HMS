from django.test import TestCase
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from staff.models import Staff
import datetime
from django.utils import timezone

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="Male",
            address="123 Main St",
            phone="555-555-5555",
        )
        self.doctor = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="Doctor",
            phone="555-555-5556",
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.make_aware(datetime.datetime(2025, 10, 20, 10, 0, 0)),
            reason="Checkup",
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(str(self.appointment), f"{self.patient} with {self.doctor} on {self.appointment.appointment_date}")

class AppointmentFormTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="Male",
            address="123 Main St",
            phone="555-555-5555",
        )
        self.doctor = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="Doctor",
            phone="555-555-5556",
        )

    def test_appointment_form_valid(self):
        form = AppointmentForm(data={
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'appointment_date': timezone.now() + datetime.timedelta(days=1),
            'reason': 'Checkup',
            'status': 'Scheduled',
        })
        self.assertTrue(form.is_valid())

    def test_appointment_form_invalid_date(self):
        form = AppointmentForm(data={
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'appointment_date': timezone.now() - datetime.timedelta(days=1),
            'reason': 'Checkup',
            'status': 'Scheduled',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('appointment_date', form.errors)