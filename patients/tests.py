from django.test import TestCase
from .models import Patient
from .forms import PatientForm
import datetime

class PatientModelTest(TestCase):
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

    def test_patient_creation(self):
        self.assertEqual(self.patient.first_name, "John")
        self.assertEqual(self.patient.last_name, "Doe")
        self.assertEqual(str(self.patient), "12345 - John Doe")

class PatientFormTest(TestCase):
    def test_patient_form_valid(self):
        form = PatientForm(data={
            'unique_id': '54321',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1992-02-02',
            'gender': 'F',
            'address': '456 Oak Ave',
            'phone': '+1234567890',
            'email': 'jane.doe@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_patient_form_invalid_phone(self):
        form = PatientForm(data={
            'unique_id': '54321',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1992-02-02',
            'gender': 'Female',
            'address': '456 Oak Ave',
            'phone': 'invalid-phone',
            'email': 'jane.doe@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_patient_form_duplicate_email(self):
        Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="Male",
            address="123 Main St",
            phone="555-555-5555",
            email='john.doe@example.com',
        )
        form = PatientForm(data={
            'unique_id': '54321',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1992-02-02',
            'gender': 'Female',
            'address': '456 Oak Ave',
            'phone': '+1234567890',
            'email': 'john.doe@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)