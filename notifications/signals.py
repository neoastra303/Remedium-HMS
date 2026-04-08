from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from .models import Notification
from django.core.mail import send_mail

@receiver(post_save, sender=Appointment)
def send_appointment_notification(sender, instance, created, **kwargs):
    if created:
        # Simulate sending SMS/Email
        message = f"Hello {instance.patient.first_name}, your appointment with {instance.doctor.full_name} is scheduled for {instance.appointment_date}."
        
        # Log notification
        if instance.patient.phone:
            Notification.objects.create(
                recipient=instance.patient.phone,
                notification_type='SMS',
                message=message
            )
        
        if instance.patient.email:
            Notification.objects.create(
                recipient=instance.patient.email,
                notification_type='EMAIL',
                message=message
            )
            # Actually try to send email if configured (console backend by default)
            try:
                send_mail(
                    'Appointment Confirmation',
                    message,
                    'noreply@hospital.com',
                    [instance.patient.email],
                    fail_silently=True,
                )
            except:
                pass
