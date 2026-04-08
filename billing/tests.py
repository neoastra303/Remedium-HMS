"""Tests for billing app."""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from billing.models import Invoice, Payment
from patients.models import Patient


@pytest.mark.django_db
class TestInvoiceModel:
    """Test Invoice model."""

    def _create_patient(self):
        """Helper to create a test patient."""
        return Patient.objects.create(
            unique_id="PAT_BILL",
            first_name="Test",
            last_name="Patient",
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender="M",
        )

    def test_create_invoice(self):
        """Test basic invoice creation."""
        patient = self._create_patient()
        invoice = Invoice.objects.create(
            patient=patient,
            total_amount=Decimal("100.00"),
        )
        assert invoice.pk is not None
        assert invoice.paid is False

    def test_negative_amount_raises_error(self):
        """Test negative total amount raises validation error."""
        patient = self._create_patient()
        invoice = Invoice(
            patient=patient,
            total_amount=Decimal("-50.00"),
        )
        with pytest.raises(ValidationError):
            invoice.full_clean()

    def test_due_date_before_issue_date_raises_error(self):
        """Test due date before issue date raises error."""
        patient = self._create_patient()
        invoice = Invoice(
            patient=patient,
            total_amount=Decimal("100.00"),
            issue_date=date.today(),
            due_date=date.today() - timedelta(days=1),
        )
        with pytest.raises(ValidationError):
            invoice.full_clean()


@pytest.mark.django_db
class TestPaymentModel:
    """Test Payment model."""

    def _create_patient(self):
        """Helper to create a test patient."""
        return Patient.objects.create(
            unique_id="PAY_PAT",
            first_name="Test",
            last_name="Patient",
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender="M",
        )

    def _create_invoice(self):
        """Helper to create a test invoice."""
        patient = self._create_patient()
        return Invoice.objects.create(
            patient=patient,
            total_amount=Decimal("100.00"),
        )

    def test_create_payment(self):
        """Test basic payment creation."""
        invoice = self._create_invoice()
        payment = Payment.objects.create(
            invoice=invoice,
            amount=Decimal("50.00"),
            payment_method="CASH",
        )
        assert payment.pk is not None
        assert payment.status == "COMPLETED"

    def test_payment_updates_invoice_paid(self):
        """Test payment updates invoice paid status."""
        invoice = self._create_invoice()
        Payment.objects.create(
            invoice=invoice,
            amount=Decimal("100.00"),
            payment_method="CARD",
        )
        invoice.refresh_from_db()
        assert invoice.paid is True

    def test_partial_payment_keeps_invoice_unpaid(self):
        """Test partial payment keeps invoice unpaid."""
        invoice = self._create_invoice()
        Payment.objects.create(
            invoice=invoice,
            amount=Decimal("50.00"),
            payment_method="CASH",
        )
        invoice.refresh_from_db()
        assert invoice.paid is False
