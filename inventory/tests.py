"""Tests for inventory app REST API."""
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import InventoryItem


def make_admin():
    return User.objects.create_superuser(username='inv_admin', password='pass', email='i@i.com')


@pytest.fixture
def admin_client():
    client = APIClient()
    client.force_authenticate(user=make_admin())
    return client


def make_item(**kwargs):
    defaults = {'name': 'Gloves', 'category': 'PPE', 'quantity': 100, 'unit': 'BOX', 'reorder_level': 10}
    defaults.update(kwargs)
    return InventoryItem.objects.create(**defaults)


@pytest.mark.django_db
class TestInventoryAPI:
    def test_list_items(self, admin_client):
        make_item()
        r = admin_client.get('/api/v1/inventory/')
        assert r.status_code == status.HTTP_200_OK
        assert r.data['count'] == 1

    def test_create_item(self, admin_client):
        r = admin_client.post('/api/v1/inventory/', {
            'name': 'Syringes', 'category': 'MEDICAL_SUPPLIES',
            'quantity': 500, 'unit': 'PIECE', 'reorder_level': 50,
        })
        assert r.status_code == status.HTTP_201_CREATED
        assert InventoryItem.objects.filter(name='Syringes').exists()

    def test_low_stock_action(self, admin_client):
        make_item(name='Low Item', quantity=5, reorder_level=10)
        make_item(name='OK Item', quantity=100, reorder_level=10)
        r = admin_client.get('/api/v1/inventory/low_stock/')
        assert r.status_code == status.HTTP_200_OK
        names = [i['name'] for i in r.data]
        assert 'Low Item' in names
        assert 'OK Item' not in names

    def test_serializer_computed_fields(self, admin_client):
        make_item(name='Bandages', quantity=5, reorder_level=10, cost_per_unit='2.50')
        r = admin_client.get('/api/v1/inventory/')
        item = r.data['results'][0]
        assert item['needs_reorder'] is True
        assert item['total_value'] == '12.50'

    def test_unauthenticated_denied(self):
        r = APIClient().get('/api/v1/inventory/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED
