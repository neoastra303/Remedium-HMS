"""Project-wide pytest fixtures."""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Provide DRF APIClient for API tests."""
    return APIClient()
