from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
from .models import Staff
from .forms import StaffForm
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime

class StaffModelTest(TestCase):
    def test_staff_creation(self):
        staff = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="DOCTOR",
            phone="+15555555556",
        )
        self.assertEqual(staff.first_name, "James")
        self.assertEqual(staff.last_name, "Smith")
        self.assertEqual(str(staff), "doc1 - James Smith (DOCTOR)")

class StaffFormTest(TestCase):
    def test_staff_form_valid(self):
        form = StaffForm(data={
            'staff_id': 'nurse1',
            'first_name': 'Mary',
            'last_name': 'Jane',
            'role': 'NURSE',
            'phone': '+15555555557',
        })
        self.assertTrue(form.is_valid())

class StaffViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.staff = Staff.objects.create(
            staff_id="doc1",
            first_name="James",
            last_name="Smith",
            role="DOCTOR",
            phone="+15555555556",
        )
        self.view_group = Group.objects.create(name='view_group')
        self.add_group = Group.objects.create(name='add_group')
        self.change_group = Group.objects.create(name='change_group')
        self.delete_group = Group.objects.create(name='delete_group')
        self.view_permission = Permission.objects.get(codename='staff_view_staff')
        self.add_permission = Permission.objects.get(codename='staff_add_staff')
        self.change_permission = Permission.objects.get(codename='staff_change_staff')
        self.delete_permission = Permission.objects.get(codename='staff_delete_staff')
        self.view_group.permissions.add(self.view_permission)
        self.add_group.permissions.add(self.add_permission)
        self.change_group.permissions.add(self.change_permission)
        self.delete_group.permissions.add(self.delete_permission)

    def test_staff_list_view_unauthenticated(self):
        response = self.client.get(reverse('staff_list'))
        self.assertEqual(response.status_code, 403)

    def test_staff_list_view_no_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('staff_list'))
        self.assertEqual(response.status_code, 403)

    def test_staff_list_view_with_permission(self):
        self.user.groups.add(self.view_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('staff_list'))
        self.assertEqual(response.status_code, 200)

    def test_staff_create_view_with_permission(self):
        self.user.groups.add(self.add_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('staff_create'))
        self.assertEqual(response.status_code, 200)

    def test_staff_update_view_with_permission(self):
        self.user.groups.add(self.change_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('staff_update', args=[self.staff.pk]))
        self.assertEqual(response.status_code, 200)

    def test_staff_delete_view_with_permission(self):
        self.user.groups.add(self.delete_group)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('staff_delete', args=[self.staff.pk]))
        self.assertEqual(response.status_code, 200)