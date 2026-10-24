from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.resources.bridge_pages import import_draft_tree, sync_bridge_resources
from apps.resources.models import Resource


class Command(BaseCommand):
    help = (
        'Replace bridge page specs and download files from a draft tree '
        '(one folder per URL slug, each with page-draft/index.html plus PDFs and PPTX). '
        'Pass --sync to upsert Resource rows and overwrite the media copies.'
    )

    def add_arguments(self, parser):
        parser.add_argument('root', help='Directory that contains the slug folders.')
        parser.add_argument(
            '--sync',
            action='store_true',
            help='Upsert Resource rows and refresh files under MEDIA_ROOT.',
        )

    def handle(self, *args, **options):
        root = Path(options['root'])
        if not root.is_dir():
            raise CommandError(f'Not a directory: {root}')
        summaries = import_draft_tree(root)
        if not summaries:
            raise CommandError(f'No page-draft/index.html folders under {root}')
        for row in summaries:
            self.stdout.write(
                f"{row['slug']}: {row['items']} materials, {row['files']} files, {row['thumbs']} thumbnails"
            )
        if options['sync']:
            created, refreshed = sync_bridge_resources(Resource, refresh_media=True)
            self.stdout.write(self.style.SUCCESS(
                f'Resource rows created: {created}. Media copies refreshed: {refreshed}.'
            ))
        self.stdout.write(self.style.SUCCESS(f'Imported {len(summaries)} bridge pages.'))
