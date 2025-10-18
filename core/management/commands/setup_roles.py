from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates default user groups and assigns permissions.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating default user groups...")

        # Define roles and their permissions
        roles = {
            'Admin': [
                'patients_view_patient', 'patients_add_patient', 'patients_change_patient', 'patients_delete_patient',
                'staff_view_staff', 'staff_add_staff', 'staff_change_staff', 'staff_delete_staff',
                'appointments_view_appointment', 'appointments_add_appointment', 'appointments_change_appointment', 'appointments_delete_appointment',
                'billing_view_invoice', 'billing_add_invoice', 'billing_change_invoice', 'billing_delete_invoice',
                'inventory_view_inventoryitem', 'inventory_add_inventoryitem', 'inventory_change_inventoryitem', 'inventory_delete_inventoryitem',
                'laboratory_view_labtest', 'laboratory_add_labtest', 'laboratory_change_labtest', 'laboratory_delete_labtest',
                'pharmacy_view_prescription', 'pharmacy_add_prescription', 'pharmacy_change_prescription', 'pharmacy_delete_prescription',
                'reporting_view_report', 'reporting_add_report', 'reporting_change_report', 'reporting_delete_report',
                'surgery_view_surgery', 'surgery_add_surgery', 'surgery_change_surgery', 'surgery_delete_surgery',
                'care_monitoring_view_patientcare', 'care_monitoring_add_patientcare', 'care_monitoring_change_patientcare', 'care_monitoring_delete_patientcare',
            ],
            'Doctor': [
                'patients_view_patient', 'patients_change_patient',
                'appointments_view_appointment', 'appointments_add_appointment', 'appointments_change_appointment',
                'laboratory_view_labtest', 'laboratory_add_labtest',
                'pharmacy_view_prescription', 'pharmacy_add_prescription',
                'care_monitoring_view_patientcare', 'care_monitoring_add_patientcare', 'care_monitoring_change_patientcare',
                'surgery_view_surgery', 'surgery_add_surgery', 'surgery_change_surgery',
            ],
            'Nurse': [
                'patients_view_patient', 'patients_change_patient',
                'appointments_view_appointment', 'appointments_change_appointment',
                'care_monitoring_view_patientcare', 'care_monitoring_add_patientcare', 'care_monitoring_change_patientcare',
            ],
            'Receptionist': [
                'patients_view_patient', 'patients_add_patient', 'patients_change_patient',
                'appointments_view_appointment', 'appointments_add_appointment', 'appointments_change_appointment',
                'billing_view_invoice',
            ],
            'Pharmacist': [
                'patients_view_patient',
                'pharmacy_view_prescription', 'pharmacy_change_prescription',
                'inventory_view_inventoryitem',
            ],
            'Lab Technician': [
                'patients_view_patient',
                'laboratory_view_labtest', 'laboratory_change_labtest',
            ],
        }

        for role_name, perms_list in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group \'{role_name}\' created.'))
            else:
                self.stdout.write(f'Group \'{role_name}\' already exists.')

            # Clear existing permissions for the group before adding new ones
            group.permissions.clear()

            for perm_codename in perms_list:
                try:
                    app_label_perm, codename_perm = perm_codename.split('_', 1)
                    action, model_name = codename_perm.split('_', 1)
                    self.stdout.write(f'DEBUG: Looking for ContentType with app_label={app_label_perm}, model={model_name}')
                    content_type = ContentType.objects.get(app_label=app_label_perm, model=model_name)
                    permission = Permission.objects.get(content_type=content_type, codename=codename_perm)
                    group.permissions.add(permission)
                except ContentType.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Content type for app_label={app_label_perm}, model={model_name} not found. Skipping permission {perm_codename}."))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permission {perm_codename} not found. Skipping.'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding permission {perm_codename} to group {role_name}: {e}'))

            self.stdout.write(self.style.SUCCESS(f'Permissions assigned to group \'{role_name}\''))

        self.stdout.write(self.style.SUCCESS('Default user groups and permissions setup complete.'))
