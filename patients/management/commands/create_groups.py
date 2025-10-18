from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates default user groups (Doctor, Nurse, Administrator, Patient) for the HMS application.'

    def handle(self, *args, **kwargs):
        groups_to_create = ['Doctor', 'Nurse', 'Administrator', 'Patient']
        for group_name in groups_to_create:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created group: '{group_name}'"))

            if group_name == 'Doctor':
                # Assign permissions to Doctor group
                permissions = [
                    'appointments_view_appointment', 'appointments_add_appointment', 'appointments_change_appointment', 'appointments_delete_appointment',
                    'patients_view_patient',
                    'laboratory_view_labtest', 'laboratory_add_labtest', 'laboratory_change_labtest', 'laboratory_delete_labtest',
                    'view_surgery', 'add_surgery', 'change_surgery', 'delete_surgery',
                    'view_prescription', 'add_prescription', 'change_prescription', 'delete_prescription',
                ]
                for perm in permissions:
                    try:
                        permission = Permission.objects.get(codename=perm)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permission '{perm}' not found."))
                self.stdout.write(self.style.SUCCESS(f"Successfully assigned permissions to '{group_name}' group."))

            if group_name == 'Administrator':
                # Assign all permissions to Administrator group
                permissions = Permission.objects.all()
                group.permissions.set(permissions)
                self.stdout.write(self.style.SUCCESS(f"Successfully assigned all permissions to '{group_name}' group."))

            if group_name == 'Patient':
                # Assign permissions to Patient group
                permissions = [
                    'patients_view_patient',
                    'appointments_view_appointment',
                ]
                for perm in permissions:
                    try:
                        permission = Permission.objects.get(codename=perm)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permission '{perm}' not found."))
                self.stdout.write(self.style.SUCCESS(f"Successfully assigned permissions to '{group_name}' group."))

            if group_name == 'Nurse':
                # Assign permissions to Nurse group
                permissions = [
                    'appointments_view_appointment',
                    'patients_view_patient',
                    'laboratory_view_labtest',
                    'view_surgery',
                    'view_prescription',
                ]
                for perm in permissions:
                    try:
                        permission = Permission.objects.get(codename=perm)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permission '{perm}' not found."))
                self.stdout.write(self.style.SUCCESS(f"Successfully assigned permissions to '{group_name}' group."))