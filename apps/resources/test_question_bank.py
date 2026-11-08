"""The test-maker bank built from the site's topic packs."""

import re
from collections import Counter

from django.test import TestCase
from django.urls import reverse

from apps.resources.assessment import published_topic_stats
from apps.resources.models import GeneratedTest, Question
from apps.resources.models import Topic
from apps.resources.question_bank import AREA_TITLES, bank_themes, load_question_bank
from apps.resources.test_assessment import _user


def _load_bank():
    for slug, title in AREA_TITLES.items():
        Topic.objects.get_or_create(slug=slug, defaults={'title': title})
    return load_question_bank(Question, Topic)


class QuestionBankTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        _load_bank()

    def test_every_bank_question_is_valid_for_its_format(self):
        rows = Question.objects.filter(sample_key__startswith='bank-')
        self.assertGreater(rows.count(), 4000)
        for row in rows:
            row.full_clean()

    def test_every_pack_has_all_levels_and_several_formats(self):
        for theme in bank_themes():
            levels = Counter(q['difficulty'] for q in theme['questions'])
            formats = {q['question_format'] for q in theme['questions']}
            for level in ('easy', 'medium', 'hard'):
                self.assertGreaterEqual(levels[level], 3, (theme['slug'], level))
            self.assertGreaterEqual(len(formats), 5, theme['slug'])
            self.assertTrue(1 <= theme['grade'] <= 11)

    def test_choice_and_true_false_answers_point_at_an_option(self):
        for row in Question.objects.filter(
            sample_key__startswith='bank-', question_format__in=['choice', 'true_false'],
        ):
            self.assertIn(row.answer, row.options, row.sample_key)

    def test_matching_answer_uses_every_pair_once(self):
        for row in Question.objects.filter(sample_key__startswith='bank-', question_format='matching'):
            pairs = re.findall(r'(\d)–([АБВГ])', row.answer)
            self.assertEqual(sorted(n for n, _ in pairs), sorted(row.options['left']))
            self.assertEqual(sorted(letter for _, letter in pairs), sorted(row.options['right']))

    def test_loading_again_changes_nothing(self):
        before = Question.objects.count()
        created, updated, skipped = load_question_bank(Question, Topic)
        self.assertEqual((created, skipped), (0, 0))
        self.assertEqual(Question.objects.count(), before)
        self.assertGreater(updated, 0)

    def test_packs_are_offered_per_grade(self):
        stats = published_topic_stats()
        self.assertIn('8-klass-pifagor', stats)
        self.assertEqual(list(stats['8-klass-pifagor']), [8])
        self.assertEqual(stats.info['8-klass-pifagor']['title'], 'Пифагордун теоремасы')


class BankTestMakerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        _load_bank()

    def setUp(self):
        self.client.force_login(_user('bank@example.com', 'bankuser'))

    def test_a_grade_8_test_and_its_pdf(self):
        response = self.client.post(reverse('test_maker'), {
            'grade': 8,
            'topics': ['8-klass-pifagor'],
            'test_type': 'formative',
            'formats': [f for f, _ in Question.FORMAT_CHOICES],
            'levels': ['easy', 'medium', 'hard', 'very_hard'],
            'duration_minutes': 40,
            'variant_count': 2,
        })
        self.assertEqual(response.status_code, 302)
        generated = GeneratedTest.objects.get()
        paper = generated.payload
        self.assertEqual(paper['topics_label'], 'Пифагордун теоремасы')
        self.assertFalse(paper['sample_only'])
        self.assertEqual([t.slug for t in generated.topics.all()], ['geometry'])
        pdf = self.client.get(reverse('test_maker_pdf', args=[generated.pk]))
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))

    def test_area_link_ticks_that_areas_packs_for_the_grade(self):
        page = self.client.get(reverse('test_maker') + '?tema=geometry&klass=8')
        html = page.content.decode()
        tag = next(t for t in re.findall(r'<input\b[^>]*>', html) if 'value="8-klass-pifagor"' in t)
        self.assertIn('checked', tag)
        self.assertIn('data-area="Геометрия"', tag)


class MissingAreaTests(TestCase):
    def test_packs_wait_for_their_area_topic(self):
        Question.objects.filter(topic__slug__in=AREA_TITLES).delete()
        Topic.objects.filter(slug__in=AREA_TITLES).delete()
        created, updated, skipped = load_question_bank(Question, Topic)
        self.assertEqual((created, updated), (0, 0))
        self.assertEqual(skipped, len(bank_themes()))
