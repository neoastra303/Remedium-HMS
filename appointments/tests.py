from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from staff.models import Staff
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime
from django.utils import timezone

class AppointmentModelTest(TestCase):
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
        self.doctor = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="Doctor",
            phone="+15555555556",
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() + datetime.timedelta(days=1),
            reason="Checkup",
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(str(self.appointment), f"{self.patient} with {self.doctor} on {self.appointment.appointment_date}")

    def test_past_appointment_date(self):
        with self.assertRaises(ValidationError):
            appointment = Appointment(
                patient=self.patient,
                doctor=self.doctor,
                appointment_date=timezone.now() - datetime.timedelta(days=1),
                reason="Checkup",
            )
            appointment.full_clean()

class AppointmentFormTest(TestCase):
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
        self.doctor = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="Doctor",
            phone="+15555555556",
        )

    def test_appointment_form_valid(self):
        form = AppointmentForm(data={
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'appointment_date': timezone.now() + datetime.timedelta(days=1),
            'reason': 'Checkup',
        })
        self.assertTrue(form.is_valid())

class AppointmentViewTest(TestCase):
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
        self.doctor = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="Doctor",
            phone="+15555555556",
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() + datetime.timedelta(days=1),
            reason="Checkup",
        )
        self.view_group = Group.objects.create(name='view_group')
        self.add_group = Group.objects.create(name='add_group')
        self.change_group = Group.objects.create(name='change_group')
        self.delete_group = Group.objects.create(name='delete_group')
        self.view_permission = Permission.objects.get(codename='appointments_view_appointment')
        self.add_permission = Permission.objects.get(codename='appointments_add_appointment')
        self.change_permission = Permission.objects.get(codename='appointments_change_appointment')
        self.delete_permission = Permission.objects.get(codename='appointments_delete_appointment')
        self.view_group.permissions.add(self.view_permission)
        self.add_group.permissions.add(self.add_permission)
        self.change_group.permissions.add(self.change_permission)
        self.delete_group.permissions.add(self.delete_permission)

    def test_appointment_list_view_unauthenticated(self):
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 302)

    def test_appointment_list_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 403)

    def test_appointment_list_view_with_permission(self):
        self.user.groups.add(self.view_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_create_view_with_permission(self):
        self.user.groups.add(self.add_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('appointment_create'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_update_view_with_permission(self):
        self.user.groups.add(self.change_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('appointment_update', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 200)

    def test_appointment_delete_view_with_permission(self):
        self.user.groups.add(self.delete_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('appointment_delete', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 200)