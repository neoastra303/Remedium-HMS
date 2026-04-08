from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from .models import Invoice
from .serializers import InvoiceSerializer
from core.permissions import IsBillingStaff


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsBillingStaff]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__unique_id', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['issue_date', 'due_date', 'total_amount']
    ordering = ['-issue_date']

    @action(detail=False, methods=['get'])
    def unpaid(self, request):
        """Get all unpaid invoices."""
        unpaid = self.queryset.filter(paid=False)
        serializer = self.get_serializer(unpaid, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue invoices."""
        from django.utils import timezone
        overdue = self.queryset.filter(
            due_date__lt=timezone.now().date(),
            paid=False
        )
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark an invoice as paid by creating a payment record."""
        invoice = self.get_object()
        if invoice.paid:
            return Response(
                {'error': 'Invoice is already marked as paid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create a payment record for audit trail
        amount = request.data.get('amount', invoice.total_amount)
        payment_method = request.data.get('payment_method', 'CASH')
        transaction_id = request.data.get('transaction_id', '')

        from .models import Payment
        try:
            Payment.objects.create(
                invoice=invoice,
                amount=amount,
                payment_method=payment_method,
                transaction_id=transaction_id,
            )
        except DjangoValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        invoice.refresh_from_db()
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)
