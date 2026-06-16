"""Project-wide pytest configuration and fixtures.

Environment variables must be set at module level (not in pytest_configure)
so they are available before pytest-django accesses Django settings.
"""

import os
import pytest
from rest_framework.test import APIClient

os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-for-pytest-that-is-long-enough-for-jwt-hmac-sha256-minimum-32-bytes",
)
os.environ.setdefault(
    "FIELD_ENCRYPTION_KEY",
    "esFW8YRhGRd_zARYth-nU0z166FmsxIpgB3aJlZ7UVQ=",
)
os.environ.setdefault("DB_ENGINE", "django.db.backends.sqlite3")
os.environ.setdefault("DB_NAME", ":memory:")


@pytest.fixture
def api_client():
    """Provide DRF APIClient for API tests."""
    return APIClient()
