"""Tests for medical_records app."""
import pytest
import io
from datetime import timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from medical_records.models import PatientDocument
from patients.models import Patient


@pytest.mark.django_db
class TestPatientDocumentModel:
    """Test PatientDocument model."""

    def _create_patient(self):
        return Patient.objects.create(
            unique_id='PAT_DOC',
            first_name='Test',
            last_name='Patient',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 30),
            gender='M',
        )

    def _create_pdf_file(self):
        """Create a minimal PDF-like file for testing."""
        content = b'%PDF-1.4 dummy content'
        return SimpleUploadedFile(
            "test_document.pdf",
            content,
            content_type='application/pdf'
        )

    def test_create_patient_document(self):
        patient = self._create_patient()
        pdf_file = self._create_pdf_file()
        doc = PatientDocument.objects.create(
            patient=patient,
            document_type='LAB_REPORT',
            title='Blood Test Results',
            file=pdf_file,
        )
        assert doc.pk is not None
        assert doc.document_type == 'LAB_REPORT'
        assert 'Blood Test' in str(doc)

    def test_document_types(self):
        """Test valid document type choices."""
        patient = self._create_patient()
        pdf_file = self._create_pdf_file()
        for doc_type in ['LAB_REPORT', 'XRAY', 'MRI', 'PRESCRIPTION', 'INSURANCE', 'OTHER']:
            doc = PatientDocument(
                patient=patient,
                document_type=doc_type,
                title=f'{doc_type} Document',
                file=pdf_file,
            )
            doc.full_clean()  # Should not raise

    def test_invalid_file_extension_rejected(self):
        """Test that .doc/.docx files are rejected."""
        patient = self._create_patient()
        doc_file = SimpleUploadedFile(
            "test.docx",
            b'mock word content',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        doc = PatientDocument(
            patient=patient,
            document_type='OTHER',
            title='Invalid Doc',
            file=doc_file,
        )
        with pytest.raises(ValidationError):
            doc.full_clean()

    def test_patient_documents_relation(self):
        """Test patient can have multiple documents."""
        patient = self._create_patient()
        pdf1 = self._create_pdf_file()
        pdf2 = self._create_pdf_file()
        pdf2.name = "test2.pdf"
        PatientDocument.objects.create(
            patient=patient, document_type='LAB_REPORT', title='Doc 1', file=pdf1
        )
        PatientDocument.objects.create(
            patient=patient, document_type='XRAY', title='Doc 2', file=pdf2
        )
        assert patient.documents.count() == 2
