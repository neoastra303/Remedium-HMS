from django.db import models
from django.utils import timezone
from django.conf import settings
from cryptography.fernet import Fernet


def get_encryption_key():
    """Get or create encryption key from Django settings."""
    # Use SECRET_KEY as basis for encryption (not ideal but better than plaintext)
    import hashlib
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    # Fernet requires 32 url-safe base64-encoded bytes
    import base64
    return base64.urlsafe_b64encode(key)


def encrypt_value(value):
    """Encrypt a value using Fernet symmetric encryption."""
    if not value:
        return value
    f = Fernet(get_encryption_key())
    return f.encrypt(value.encode()).decode()


def decrypt_value(value):
    """Decrypt a Fernet-encrypted value."""
    if not value:
        return value
    f = Fernet(get_encryption_key())
    return f.decrypt(value.encode()).decode()


class ExternalIntegration(models.Model):
    SYSTEM_TYPES = [
        ('EMR', 'Electronic Medical Records'),
        ('PHARMACY_HUB', 'External Pharmacy Hub'),
        ('INSURANCE', 'Insurance Gateway'),
        ('LAB_EQUIPMENT', 'Laboratory Equipment'),
    ]
    
    system_name = models.CharField(max_length=100)
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPES, default='EMR')
    api_endpoint = models.URLField()
    api_key = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Encrypted API Key (use set_api_key/get_api_key methods)"
    )

    def set_api_key(self, raw_key):
        """Encrypt and store the API key."""
        self.api_key = encrypt_value(raw_key)

    def get_api_key(self):
        """Decrypt and return the API key."""
        if not self.api_key:
            return None
        return decrypt_value(self.api_key)
    last_sync = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Inactive')
    last_sync_result = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def trigger_sync(self):
        """Placeholder for actual synchronization logic."""
        # Here we would normally use requests or a task queue like Celery
        self.status = 'Synchronizing'
        self.save()
        # Simulation of successful sync
        self.last_sync = timezone.now()
        self.status = 'Active'
        self.last_sync_result = {"status": "success", "message": "Records synchronized."}
        self.save()

    def __str__(self):
        return f"{self.system_name} ({self.get_system_type_display()})"


# Create your models here.
