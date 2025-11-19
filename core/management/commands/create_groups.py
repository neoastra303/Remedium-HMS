from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Creates default user groups and assigns permissions. Alias for setup_roles.'

    def handle(self, *args, **kwargs):
        call_command('setup_roles')
