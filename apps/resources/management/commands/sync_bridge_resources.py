from django.core.management.base import BaseCommand

from apps.resources.bridge_pages import sync_bridge_resources
from apps.resources.models import Resource


class Command(BaseCommand):
    help = (
        'Ensure every file named by the bridge page specs has an active Resource row. '
        'Pass --refresh to overwrite the media copy from bundled_files/ '
        '(use this after swapping a PDF or PPTX that keeps the same filename).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--refresh',
            action='store_true',
            help='Overwrite MEDIA_ROOT copies from the bundled bridge files.',
        )

    def handle(self, *args, **options):
        created, refreshed = sync_bridge_resources(Resource, refresh_media=options['refresh'])
        self.stdout.write(self.style.SUCCESS(
            f'Resource rows created: {created}. Media copies refreshed: {refreshed}.'
        ))
