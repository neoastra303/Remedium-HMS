from django.test import TestCase
from .models import Ward, Room
from .forms import WardForm, RoomForm

class HospitalModelTest(TestCase):
    def setUp(self):
        self.ward = Ward.objects.create(
            name="ICU",
            capacity=10,
        )
        self.room = Room.objects.create(
            ward=self.ward,
            room_number="101",
            capacity=2,
        )

    def test_ward_creation(self):
        self.assertEqual(self.ward.name, "ICU")
        self.assertEqual(self.ward.capacity, 10)
        self.assertEqual(str(self.ward), "ICU")
        
    def test_room_creation(self):
        self.assertEqual(self.room.ward, self.ward)
        self.assertEqual(self.room.room_number, "101")
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(str(self.room), "ICU - Room 101")

class WardFormTest(TestCase):
    def test_ward_form_valid(self):
        form = WardForm(data={
            'name': 'Emergency',
            'capacity': 20,
        })
        self.assertTrue(form.is_valid())

    def test_ward_form_invalid_capacity(self):
        form = WardForm(data={
            'name': 'Emergency',
            'capacity': -5,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('capacity', form.errors)

class RoomFormTest(TestCase):
    def setUp(self):
        self.ward = Ward.objects.create(
            name="ICU",
            capacity=10,
        )

    def test_room_form_valid(self):
        form = RoomForm(data={
            'ward': self.ward.pk,
            'room_number': '201',
            'capacity': 2,
        })
        self.assertTrue(form.is_valid())

    def test_room_form_invalid_capacity(self):
        form = RoomForm(data={
            'ward': self.ward.pk,
            'room_number': '201',
            'capacity': -2,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('capacity', form.errors)

    def test_room_form_empty_room_number(self):
        form = RoomForm(data={
            'ward': self.ward.pk,
            'room_number': '',
            'capacity': 2,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)