from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
from .models import Invoice
from .forms import InvoiceForm
from patients.models import Patient
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime
from django.utils import timezone

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
            address="123 Main St",
            phone="+15555555555",
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

    def test_negative_total_amount(self):
        with self.assertRaises(ValidationError):
            invoice = Invoice(
                patient=self.patient,
                total_amount=-100.00,
            )
            invoice.full_clean()

    def test_due_date_before_issue_date(self):
        with self.assertRaises(ValidationError):
            invoice = Invoice(
                patient=self.patient,
                total_amount=100.00,
                issue_date=datetime.date.today(),
                due_date=datetime.date.today() - datetime.timedelta(days=1),
            )
            invoice.full_clean()

class InvoiceFormTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
            address="123 Main St",
            phone="+15555555555",
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

class InvoiceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
            address="123 Main St",
            phone="+15555555555",
        )
        self.invoice = Invoice.objects.create(
            patient=self.patient,
            total_amount=100.00,
            details="Test invoice",
        )
        self.view_group = Group.objects.create(name='view_group')
        self.add_group = Group.objects.create(name='add_group')
        self.change_group = Group.objects.create(name='change_group')
        self.delete_group = Group.objects.create(name='delete_group')
        self.view_permission = Permission.objects.get(codename='billing_view_invoice')
        self.add_permission = Permission.objects.get(codename='billing_add_invoice')
        self.change_permission = Permission.objects.get(codename='billing_change_invoice')
        self.delete_permission = Permission.objects.get(codename='billing_delete_invoice')
        self.view_group.permissions.add(self.view_permission)
        self.add_group.permissions.add(self.add_permission)
        self.change_group.permissions.add(self.change_permission)
        self.delete_group.permissions.add(self.delete_permission)

    def test_invoice_list_view_unauthenticated(self):
        response = self.client.get(reverse('invoice_list'))
        self.assertEqual(response.status_code, 403)

    def test_invoice_list_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('invoice_list'))
        self.assertEqual(response.status_code, 403)

    def test_invoice_list_view_with_permission(self):
        self.user.groups.add(self.view_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('invoice_list'))
        self.assertEqual(response.status_code, 200)

    def test_invoice_create_view_with_permission(self):
        self.user.groups.add(self.add_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('invoice_create'))
        self.assertEqual(response.status_code, 200)

    def test_invoice_update_view_with_permission(self):
        self.user.groups.add(self.change_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('invoice_update', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)

    def test_invoice_delete_view_with_permission(self):
        self.user.groups.add(self.delete_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('invoice_delete', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)