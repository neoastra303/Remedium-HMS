import pytest
from patients.models import Patient
from datetime import date
from django.db import connection

@pytest.mark.django_db
class TestDatabaseEnhancements:
    """Test soft deletes and encryption."""

    def test_soft_delete(self):
        """Verify that records are soft deleted and hidden from default manager."""
        patient = Patient.objects.create(
            unique_id="SD001",
            first_name="Soft",
            last_name="Delete",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            phone="123456789"
        )
        
        # Initial check
        assert Patient.objects.count() == 1
        assert not patient.is_deleted
        
        # Soft delete
        patient.delete()
        
        # Verify hidden from default manager
        assert Patient.objects.count() == 0
        
        # Verify visible in all_objects manager
        assert Patient.all_objects.count() == 1
        
        # Refresh from DB
        patient.refresh_from_db()
        assert patient.is_deleted
        assert patient.deleted_at is not None
        
        # Restore
        patient.restore()
        assert Patient.objects.count() == 1
        assert not patient.is_deleted

    def test_encryption_at_rest(self):
        """Verify that data is encrypted in the database but decrypted in Python."""
        sensitive_phone = "1234567890"
        patient = Patient.objects.create(
            unique_id="ENC001",
            first_name="Encrypted",
            last_name="Patient",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            phone=sensitive_phone
        )
        
        # Check value in Python (should be decrypted)
        assert patient.phone == sensitive_phone
        
        # Check value in Database (should NOT be plain text)
        with connection.cursor() as cursor:
            cursor.execute("SELECT phone FROM patients_patient WHERE unique_id='ENC001'")
            row = cursor.fetchone()
            db_value = row[0]
            
            # Encrypted values usually start with a specific prefix or are long base64 strings
            assert db_value != sensitive_phone
            # django-encrypted-model-fields values are long strings
            assert len(db_value) > 32 
