from django.core.management.base import BaseCommand

from apps.resources.bridge_menu import apply_bridge_menu
from apps.resources.models import MenuItem


class Command(BaseCommand):
    help = (
        'Add the bridge pages to the area menu. Idempotent. '
        'Does not remove or rename anything already in the menu.'
    )

    def handle(self, *args, **options):
        created = apply_bridge_menu(MenuItem)
        if created:
            self.stdout.write('Created: ' + ', '.join(created))
        else:
            self.stdout.write('Menu already had the bridge pages.')
        self.stdout.write(self.style.SUCCESS('Bridge menu links are in place.'))
