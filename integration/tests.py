from django.test import TestCase
from django.utils import timezone
from .models import ExternalIntegration
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class ExternalIntegrationModelTest(TestCase):
    def setUp(self):
        self.integration = ExternalIntegration.objects.create(
            system_name="Test EMR",
            system_type="EMR",
            api_endpoint="https://api.testemr.com/v1",
        )

    def test_integration_creation(self):
        self.assertEqual(self.integration.system_name, "Test EMR")
        self.assertEqual(self.integration.status, "Inactive")
        self.assertEqual(str(self.integration), "Test EMR (Electronic Medical Records)")

    def test_trigger_sync_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.integration.trigger_sync()


class ExternalIntegrationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", password="password", email="admin@test.com"
        )
        self.client.force_authenticate(user=self.user)
        self.integration = ExternalIntegration.objects.create(
            system_name="Test EMR",
            system_type="EMR",
            api_endpoint="https://api.testemr.com/v1",
        )

    def test_list_integrations(self):
        url = reverse("integration-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_sync_action(self):
        url = reverse("integration-sync", args=[self.integration.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)
        self.assertEqual(response.data["status"], "not_implemented")
