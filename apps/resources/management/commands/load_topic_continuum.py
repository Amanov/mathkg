from django.core.management.base import BaseCommand

from apps.resources.continuum import load_topic_continuum
from apps.resources.models import TopicContinuum


class Command(BaseCommand):
    help = (
        'Load learning-paths.csv and grade-tags.csv into TopicContinuum. '
        'Idempotent: running it again updates rows in place.'
    )

    def handle(self, *args, **options):
        count = load_topic_continuum(TopicContinuum)
        self.stdout.write(self.style.SUCCESS(f'Loaded {count} topic path rows.'))
