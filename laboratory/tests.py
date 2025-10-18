from django.test import TestCase
from .models import LabTest
from patients.models import Patient
import datetime

class LabTestModelTest(TestCase):
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
        self.lab_test = LabTest.objects.create(
            patient=self.patient,
            test_name="Blood Test",
        )

    def test_lab_test_creation(self):
        self.assertEqual(self.lab_test.patient, self.patient)
        self.assertEqual(self.lab_test.test_name, "Blood Test")
        self.assertEqual(str(self.lab_test), f"Blood Test for {self.patient}")