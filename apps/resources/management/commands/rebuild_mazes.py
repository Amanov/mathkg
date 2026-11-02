"""Repaint every maze so the correct route is not the same shape."""

from django.core.management.base import BaseCommand

from apps.resources.generators.maze_build import rebuild_folder


class Command(BaseCommand):
    help = 'Give each maze its own seeded route and write the PDFs again.'

    def handle(self, *args, **options):
        placed = rebuild_folder()
        self.stdout.write(f'mazes {len(placed)}')
