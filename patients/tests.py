from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
from .models import Patient
from .forms import PatientForm
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime

class PatientModelTest(TestCase):
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

    def test_patient_creation(self):
        self.assertEqual(self.patient.first_name, "John")
        self.assertEqual(self.patient.last_name, "Doe")
        self.assertEqual(str(self.patient), "12345 - John Doe")

    def test_invalid_phone(self):
        with self.assertRaises(ValidationError):
            patient = Patient(
                unique_id="54321",
                first_name="Jane",
                last_name="Doe",
                date_of_birth=datetime.date(1992, 2, 2),
                gender="F",
                address="456 Oak Ave",
                phone="invalid-phone",
                email='jane.doe@example.com',
            )
            patient.full_clean()

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

    def test_patient_form_duplicate_email(self):
        Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
            address="123 Main St",
            phone="+15555555555",
            email='john.doe@example.com',
        )
        form = PatientForm(data={
            'unique_id': '54321',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1992-02-02',
            'gender': 'F',
            'address': '456 Oak Ave',
            'phone': '+1234567890',
            'email': 'john.doe@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class PatientViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.view_group = Group.objects.create(name='view_group')
        self.add_group = Group.objects.create(name='add_group')
        self.change_group = Group.objects.create(name='change_group')
        self.delete_group = Group.objects.create(name='delete_group')
        self.view_permission = Permission.objects.get(codename='patients_view_patient')
        self.add_permission = Permission.objects.get(codename='patients_add_patient')
        self.change_permission = Permission.objects.get(codename='patients_change_patient')
        self.delete_permission = Permission.objects.get(codename='patients_delete_patient')
        self.view_group.permissions.add(self.view_permission)
        self.add_group.permissions.add(self.add_permission)
        self.change_group.permissions.add(self.change_permission)
        self.delete_group.permissions.add(self.delete_permission)
        self.patient = Patient.objects.create(
            unique_id="12345",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            gender="M",
            address="123 Main St",
            phone="+15555555555",
        )

    def test_patient_list_view_unauthenticated(self):
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/patients/')

    def test_patient_list_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 403)

    def test_patient_list_view_with_permission(self):
        self.user.groups.add(self.view_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)

    def test_patient_create_view_unauthenticated(self):
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/patients/create/')

    def test_patient_create_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 403)

    def test_patient_create_view_with_permission(self):
        self.user.groups.add(self.add_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 200)

    def test_patient_create_view_form_valid(self):
        self.user.groups.add(self.add_group)
        self.client.login(username='testuser', password='password')
        form_data = {
            'unique_id': '54321',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1992-02-02',
            'gender': 'F',
            'address': '456 Oak Ave',
            'phone': '+1234567890',
            'email': 'jane.doe@example.com',
        }
        response = self.client.post(reverse('patient_create'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patient_list'))
        self.assertTrue(Patient.objects.filter(unique_id='54321').exists())

    def test_patient_update_view_unauthenticated(self):
        response = self.client.get(reverse('patient_update', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/patients/{self.patient.pk}/update/')

    def test_patient_update_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_update', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 403)

    def test_patient_update_view_with_permission(self):
        self.user.groups.add(self.change_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_update', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)

    def test_patient_update_view_form_valid(self):
        self.user.groups.add(self.change_group)
        self.client.login(username='testuser', password='password')
        form_data = {
            'unique_id': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'address': '123 Main St',
            'phone': '+15555555555',
            'email': 'john.doe.updated@example.com',
        }
        response = self.client.post(reverse('patient_update', args=[self.patient.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patient_list'))
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.email, 'john.doe.updated@example.com')

    def test_patient_delete_view_unauthenticated(self):
        response = self.client.get(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/patients/{self.patient.pk}/delete/')

    def test_patient_delete_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 403)

    def test_patient_delete_view_with_permission(self):
        self.user.groups.add(self.delete_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)

    def test_patient_delete_view_post(self):
        self.user.groups.add(self.delete_group)
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patient_list'))
        self.assertFalse(Patient.objects.filter(pk=self.patient.pk).exists())