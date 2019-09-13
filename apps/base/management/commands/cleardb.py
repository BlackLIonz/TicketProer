from django.core.management.base import BaseCommand

from apps.users.models import User, Organization
from apps.locations.models import Address, Place
from apps.events.models import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        Event.objects.all().delete()
        Place.objects.all().delete()
        Address.objects.all().delete()
        Organization.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('DB was successfully cleared'))