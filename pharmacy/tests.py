from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
from .models import Prescription
from .forms import PrescriptionForm
from patients.models import Patient
from staff.models import Staff
from django.urls import reverse
import datetime

class PrescriptionModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
        )
        self.prescription = Prescription.objects.create(
            patient=self.patient,
            drug_name="Test Drug",
            dosage="10mg",
            frequency="Once a day",
        )

    def test_prescription_creation(self):
        self.assertEqual(self.prescription.drug_name, "Test Drug")
        self.assertEqual(str(self.prescription), f"Test Drug for {self.patient}")

class PrescriptionFormTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
        )

    def test_prescription_form_valid(self):
        form = PrescriptionForm(data={
            'patient': self.patient.pk,
            'drug_name': 'Test Drug',
            'dosage': '10mg',
            'frequency': 'Once a day',
        })
        self.assertTrue(form.is_valid())

class PrescriptionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
        )
        self.prescription = Prescription.objects.create(
            patient=self.patient,
            drug_name="Test Drug",
            dosage="10mg",
            frequency="Once a day",
        )
        self.view_group = Group.objects.create(name='view_group')
        self.add_group = Group.objects.create(name='add_group')
        self.change_group = Group.objects.create(name='change_group')
        self.delete_group = Group.objects.create(name='delete_group')
        self.view_permission = Permission.objects.get(codename='pharmacy_view_prescription')
        self.add_permission = Permission.objects.get(codename='pharmacy_add_prescription')
        self.change_permission = Permission.objects.get(codename='pharmacy_change_prescription')
        self.delete_permission = Permission.objects.get(codename='pharmacy_delete_prescription')
        self.view_group.permissions.add(self.view_permission)
        self.add_group.permissions.add(self.add_permission)
        self.change_group.permissions.add(self.change_permission)
        self.delete_group.permissions.add(self.delete_permission)

    def test_prescription_list_view_unauthenticated(self):
        response = self.client.get(reverse('prescription_list'))
        self.assertEqual(response.status_code, 403)

    def test_prescription_list_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('prescription_list'))
        self.assertEqual(response.status_code, 403)

    def test_prescription_list_view_with_permission(self):
        self.user.groups.add(self.view_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('prescription_list'))
        self.assertEqual(response.status_code, 200)

    def test_prescription_create_view_with_permission(self):
        self.user.groups.add(self.add_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('prescription_create'))
        self.assertEqual(response.status_code, 200)

    def test_prescription_update_view_with_permission(self):
        self.user.groups.add(self.change_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('prescription_update', args=[self.prescription.pk]))
        self.assertEqual(response.status_code, 200)

    def test_prescription_delete_view_with_permission(self):
        self.user.groups.add(self.delete_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('prescription_delete', args=[self.prescription.pk]))
        self.assertEqual(response.status_code, 200)