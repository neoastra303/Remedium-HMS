from django.test import TestCase
from .models import Invoice
from .forms import InvoiceForm
from patients.models import Patient
import datetime

class InvoiceModelTest(TestCase):
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
        self.invoice = Invoice.objects.create(
            patient=self.patient,
            total_amount=100.00,
            details="Test invoice",
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.patient, self.patient)
        self.assertEqual(self.invoice.total_amount, 100.00)
        self.assertEqual(str(self.invoice), f"Invoice #{self.invoice.id} for {self.patient}")

class InvoiceFormTest(TestCase):
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

    def test_invoice_form_valid(self):
        form = InvoiceForm(data={
            'patient': self.patient.pk,
            'total_amount': 100.00,
            'paid': False,
            'insurance_claimed': False,
            'details': 'Test invoice',
        })
        self.assertTrue(form.is_valid())

    def test_invoice_form_invalid_total_amount(self):
        form = InvoiceForm(data={
            'patient': self.patient.pk,
            'total_amount': -100.00,
            'paid': False,
            'insurance_claimed': False,
            'details': 'Test invoice',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('total_amount', form.errors)