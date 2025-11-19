from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
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
        """Mark an invoice as paid."""
        invoice = self.get_object()
        invoice.paid = True
        invoice.save()
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)
