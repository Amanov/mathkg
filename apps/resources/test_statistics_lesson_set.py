from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from apps.resources.data.statistics_lesson_set import NAMES
from apps.resources.models import Resource


class StatisticsLessonSetTests(TestCase):
    def test_page_lists_every_pack_file_in_kyrgyz_sections(self):
        bundled = Path(__file__).resolve().parent / 'bundled_files'
        for name in NAMES:
            self.assertTrue((bundled / name).is_file(), name)
        self.assertEqual(
            set(Resource.objects.filter(title__in=NAMES, is_active=True).values_list('title', flat=True)),
            set(NAMES),
        )
        resp = self.client.get(reverse('statistika_ortocho'))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        for heading in (
            'Презентациялар', 'Тактадагы суроолор', 'Иш барактары',
            'Иш-аракеттер', 'Мугалим жетектеген', 'Мугалим',
        ):
            self.assertIn(heading, html)
        self.assertIn('topic-page__grade"><span>6–7 кл.</span>', html)
        self.assertIn('Кайсы команда жакшыраак?', html)
        self.assertIn('thumb-deck-01.png', html)
        self.assertNotIn('Presentations', html)
        self.assertNotIn('Worksheets', html)
