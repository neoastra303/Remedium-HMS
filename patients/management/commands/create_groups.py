from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates default user groups (Doctor, Nurse, Administrator, Patient) for the HMS application.'

    def handle(self, *args, **kwargs):
        groups_to_create = ['Doctor', 'Nurse', 'Administrator', 'Patient']
        #print("Running create_groups command")
        for group_name in groups_to_create:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created group: '{group_name}'"))