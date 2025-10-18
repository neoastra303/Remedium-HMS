from django.test import TestCase
from .forms import InventoryItemForm

class InventoryItemFormTest(TestCase):
    def test_inventory_item_form_valid(self):
        form = InventoryItemForm(data={
            'name': 'Bandages',
            'category': 'MEDICAL_SUPPLIES',
            'quantity': 100,
            'unit': 'BOX',
            'reorder_level': 20,
        })
        self.assertTrue(form.is_valid())

    def test_inventory_item_form_invalid_quantity(self):
        form = InventoryItemForm(data={
            'name': 'Bandages',
            'category': 'Medical Supplies',
            'quantity': -100,
            'unit': 'Box',
            'reorder_level': 20,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_inventory_item_form_invalid_reorder_level(self):
        form = InventoryItemForm(data={
            'name': 'Bandages',
            'category': 'Medical Supplies',
            'quantity': 100,
            'unit': 'Box',
            'reorder_level': -20,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('reorder_level', form.errors)
from .models import InventoryItem

class InventoryItemModelTest(TestCase):
    def setUp(self):
        self.item = InventoryItem.objects.create(
            name="Bandages",
            category="Medical Supplies",
            quantity=100,
            unit="Box",
            reorder_level=20,
        )

    def test_inventory_item_creation(self):
        self.assertEqual(self.item.name, "Bandages")
        self.assertEqual(self.item.quantity, 100)
        self.assertEqual(str(self.item), "Bandages (100 Box)")