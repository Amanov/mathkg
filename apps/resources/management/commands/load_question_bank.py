from django.core.management.base import BaseCommand

from apps.resources.models import Question, Topic
from apps.resources.question_bank import load_question_bank


class Command(BaseCommand):
    help = 'Load or refresh the test-maker question bank from data/question_bank.json.'

    def handle(self, *args, **options):
        created, updated, skipped = load_question_bank(Question, Topic)
        self.stdout.write(
            f'Question bank: {created} added, {updated} refreshed, '
            f'{skipped} packs skipped (their menu area topic is missing).'
        )
