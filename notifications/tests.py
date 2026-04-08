"""Tests for notifications app."""
import pytest
from datetime import timedelta
from django.utils import timezone
from notifications.models import Notification
from patients.models import Patient


@pytest.mark.django_db
class TestNotificationModel:
    """Test Notification model."""

    def _create_patient(self):
        return Patient.objects.create(
            unique_id='PAT_NOTIF',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )

    def test_create_notification(self):
        patient = self._create_patient()
        notif = Notification.objects.create(
            recipient='+1234567890',
            notification_type='SMS',
            message='Your appointment is tomorrow at 10 AM',
            patient=patient,
        )
        assert notif.pk is not None
        assert notif.status == 'PENDING'
        assert 'SMS' in str(notif)

    def test_notification_status_choices(self):
        """Test valid status values."""
        for status in ['PENDING', 'SENT', 'FAILED', 'RETRYING']:
            notif = Notification(
                recipient='test@example.com',
                notification_type='EMAIL',
                message='Test message',
                status=status,
            )
            notif.full_clean()  # Should not raise

    def test_mark_sent(self):
        """Test mark_sent method."""
        notif = Notification.objects.create(
            recipient='+1234567890',
            notification_type='SMS',
            message='Test',
        )
        assert notif.status == 'PENDING'
        notif.mark_sent()
        notif.refresh_from_db()
        assert notif.status == 'SENT'

    def test_mark_failed(self):
        """Test mark_failed method with error message."""
        notif = Notification.objects.create(
            recipient='bad@number',
            notification_type='SMS',
            message='Test',
        )
        notif.mark_failed('Invalid phone number')
        notif.refresh_from_db()
        assert notif.status == 'FAILED'
        assert notif.error_message == 'Invalid phone number'

    def test_patient_relation(self):
        """Test notifications can be accessed from patient."""
        patient = Patient.objects.create(
            unique_id='PAT_NOTIF2',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )
        Notification.objects.create(
            recipient='+1111111111',
            notification_type='SMS',
            message='Notification 1',
            patient=patient,
        )
        Notification.objects.create(
            recipient='+2222222222',
            notification_type='SMS',
            message='Notification 2',
            patient=patient,
        )
        assert patient.notifications.count() == 2

    def test_notification_ordering(self):
        """Test notifications are ordered by sent_at descending."""
        patient = Patient.objects.create(
            unique_id='PAT_NOTIF3',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )
        n1 = Notification.objects.create(
            recipient='user1@test.com',
            notification_type='EMAIL',
            message='First',
            patient=patient,
        )
        n2 = Notification.objects.create(
            recipient='user2@test.com',
            notification_type='EMAIL',
            message='Second',
            patient=patient,
        )
        # Latest should be first
        all_notifs = list(Notification.objects.filter(patient=patient))
        assert all_notifs[0].pk == n2.pk
