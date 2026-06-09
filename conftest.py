"""Project-wide pytest configuration and fixtures."""

import os
import pytest
from rest_framework.test import APIClient


def pytest_configure(config):
    """Set test environment variables before Django initialises."""
    os.environ.setdefault(
        "SECRET_KEY",
        "test-secret-key-for-pytest-that-is-long-enough-for-jwt-hmac-sha256-minimum-32-bytes",
    )
    os.environ.setdefault("DB_ENGINE", "django.db.backends.sqlite3")
    os.environ.setdefault("DB_NAME", ":memory:")


@pytest.fixture
def api_client():
    """Provide DRF APIClient for API tests."""
    return APIClient()
