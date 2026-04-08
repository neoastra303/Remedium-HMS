"""Tests for staff app."""
import pytest
from django.core.exceptions import ValidationError
from staff.models import Staff


@pytest.mark.django_db
class TestStaffModel:
    """Test Staff model."""

    def test_create_staff(self):
        """Test basic staff creation."""
        staff = Staff.objects.create(
            staff_id="STF001",
            first_name="John",
            last_name="Doe",
            role="Doctor",
        )
        assert staff.pk is not None
        assert str(staff) == "STF001 - John Doe (DOCTOR)"

    def test_full_name_property(self):
        """Test full_name property."""
        staff = Staff(
            staff_id="STF002",
            first_name="Jane",
            last_name="Smith",
            role="Nurse",
        )
        assert staff.full_name == "Jane Smith"

    def test_staff_id_must_be_unique(self):
        """Test staff_id constraint."""
        Staff.objects.create(
            staff_id="DUP_STF",
            first_name="First",
            last_name="User",
            role="Admin",
        )
        with pytest.raises(Exception):  # IntegrityError
            Staff.objects.create(
                staff_id="DUP_STF",
                first_name="Second",
                last_name="User",
                role="Admin",
            )
