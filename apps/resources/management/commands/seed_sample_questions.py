from django.core.management.base import BaseCommand

from apps.resources.models import Question, Topic
from apps.resources.sample_questions import seed_sample_questions


class Command(BaseCommand):
    help = 'Үлгү тест суроолорун кошот же жаңыртат. Кайра иштетүү коопсуз.'

    def handle(self, *args, **options):
        result = seed_sample_questions(Question, Topic)
        self.stdout.write(self.style.SUCCESS(
            f"Тема түзүлдү: {result['topics_created']}. "
            f"Суроо түзүлдү: {result['created']}. "
            f"Суроо жаңыланды: {result['updated']}."
        ))
