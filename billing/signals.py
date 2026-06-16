from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import Payment


@receiver(post_save, sender=Payment)
def update_invoice_paid(sender, instance, created, **kwargs):
    """Signal to update invoice paid status when a payment is created."""
    if created:
        total_paid = (
            instance.invoice.payments.aggregate(total=Sum("amount"))["total"] or 0
        )
        if total_paid >= instance.invoice.total_amount:
            instance.invoice.paid = True
            instance.invoice.save(update_fields=["paid"])
