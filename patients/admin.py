from django.contrib import admin
from .models import Patient
from django.contrib.auth.models import Group

admin.site.register(Patient)

def create_groups():
    groups = ['Doctor', 'Nurse', 'Administrator', 'Patient']
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Created group {group_name}")
        else:
            print(f"Group {group_name} already exists")

create_groups()

# Register your models here.
