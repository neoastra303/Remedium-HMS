"""Project-wide pytest fixtures."""
import os
import pytest
from rest_framework.test import APIClient

# Ensure SECRET_KEY is long enough for JWT (≥32 bytes) during tests
os.environ.setdefault(
    'SECRET_KEY',
    'test-secret-key-for-pytest-that-is-long-enough-for-jwt-hmac-sha256-minimum-32-bytes'
)


@pytest.fixture
def api_client():
    """Provide DRF APIClient for API tests."""
    return APIClient()
