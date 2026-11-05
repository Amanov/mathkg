"""Test maker: bank, limits, variants, PDF, and where the page is linked."""
import re
from datetime import timedelta
from decimal import Decimal
from fractions import Fraction
from io import StringIO

import pymupdf
from django.contrib import admin
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.account.models import PLAN_ONE_YEAR, Account
from apps.resources.assessment import (
    difficulty_quotas,
    render_test_pdf,
    single_grade_number,
)
from apps.resources.models import GeneratedTest, Question, Subtopic, Topic
from apps.resources.sample_questions import NBSP, SAMPLE_QUESTIONS
from apps.resources.test_heading_structure import headings


def _user(email, username, **fields):
    user = Account.objects.create_user(
        email=email,
        username=username,
        password='SuperSecret123!',
    )
    user.is_active = True
    for key, value in fields.items():
        setattr(user, key, value)
    user.save()
    return user


class SampleBankTests(TestCase):
    def test_samples_are_kyrgyz_and_correct(self):
        self.assertGreaterEqual(len(SAMPLE_QUESTIONS), 10)
        by_key = {row['sample_key']: row for row in SAMPLE_QUESTIONS}
        self.assertEqual(by_key['ulgu-f-half-quarter']['answer'], 'Б')
        self.assertEqual(Fraction(1, 2) + Fraction(1, 4), Fraction(3, 4))
        self.assertEqual(by_key['ulgu-f-same-den']['answer'], '5/7')
        self.assertEqual(Fraction(2, 7) + Fraction(3, 7), Fraction(5, 7))
        self.assertEqual(by_key['ulgu-f-of-whole']['answer'], 'Б')
        self.assertEqual(20 * Fraction(3, 5), 12)
        self.assertEqual(by_key['ulgu-f-subtract']['answer'], '1/3')
        self.assertEqual(Fraction(5, 6) - Fraction(1, 2), Fraction(1, 3))
        self.assertEqual(by_key['ulgu-f-cloth']['answer'], '750')
        self.assertEqual(1000 - 1000 * Fraction(1, 4), 750)
        self.assertIn(f'1{NBSP}000', by_key['ulgu-f-cloth']['text'])
        self.assertEqual(by_key['ulgu-f-divide']['answer'], 'Б')
        self.assertEqual(Fraction(2, 3) / Fraction(1, 6), 4)
        self.assertEqual(by_key['ulgu-f-equal']['answer'], 'В')
        self.assertEqual(Fraction(1, 2), Decimal('0.5'))
        self.assertEqual(Fraction(1, 2), Fraction(3, 6))
        self.assertEqual(by_key['ulgu-d-add']['answer'], 'А')
        self.assertEqual(Decimal('0.3') + Decimal('0.4'), Decimal('0.7'))
        self.assertEqual(by_key['ulgu-d-mul']['answer'], '10')
        self.assertEqual(Decimal('2.5') * 4, 10)
        self.assertEqual(by_key['ulgu-d-apples']['answer'], '200')
        self.assertEqual(Decimal('2.5') * 80, 200)
        self.assertEqual(by_key['ulgu-d-to-fraction']['answer'], '3/4')
        self.assertEqual(Decimal('0.75'), Fraction(3, 4))
        self.assertEqual(by_key['ulgu-d-area']['answer'], '7')
        self.assertEqual(Decimal('3.5') * 2, 7)

        for row in SAMPLE_QUESTIONS:
            text = row['text'] + row['answer'] + ''.join(row['options'].values())
            self.assertNotIn('чеч', text)
            self.assertNotIn('оқушы', text)
            self.assertNotRegex(text, r'\d+\.\d+')
            if row['question_type'] == 'word_problem':
                self.assertIn('Маселени чыгар', row['text'])
            if 'алма' in row['text']:
                self.assertIn('окуучу', text.casefold())
            if row['question_type'] == 'multiple_choice':
                self.assertEqual(set(row['options']), {'А', 'Б', 'В', 'Г'})
                self.assertIn(row['answer'], row['options'])
            self.assertIn(row['grade'], (5, 6))
            question = Question.objects.get(sample_key=row['sample_key'])
            question.full_clean()
            self.assertTrue(question.is_sample)
            self.assertTrue(question.is_published)

    def test_seed_command_is_idempotent(self):
        before = Question.objects.filter(is_sample=True).count()
        self.assertGreaterEqual(before, 12)
        call_command('seed_sample_questions', stdout=StringIO())
        call_command('seed_sample_questions', stdout=StringIO())
        self.assertEqual(Question.objects.filter(is_sample=True).count(), before)

    def test_admin_filters_grade_topic_and_difficulty(self):
        registered = admin.site._registry[Question]
        self.assertIn('grade', registered.list_filter)
        self.assertIn('topic', registered.list_filter)
        self.assertIn('difficulty', registered.list_filter)

    def test_single_grade_badge_only(self):
        self.assertEqual(single_grade_number('5 кл.'), '5')
        self.assertEqual(single_grade_number('5-класс'), '5')
        self.assertEqual(single_grade_number('6–7 кл.'), '')


class QuotaMathTests(TestCase):
    def test_mixes_add_up(self):
        self.assertEqual(
            difficulty_quotas(5, GeneratedTest.MIX_EQUAL),
            {'easy': 2, 'medium': 2, 'hard': 1},
        )
        self.assertEqual(
            difficulty_quotas(4, GeneratedTest.MIX_EASY),
            {'easy': 4, 'medium': 0, 'hard': 0},
        )
        for count in (1, 5, 10, 30):
            for mix, _label in GeneratedTest.MIX_CHOICES:
                self.assertEqual(sum(difficulty_quotas(count, mix).values()), count)


class TestMakerPageTests(TestCase):
    def setUp(self):
        self.user = _user('trial@example.com', 'trialuser')
        self.fractions = Topic.objects.get(slug='ulgu-bolchoktor')
        self.decimals = Topic.objects.get(slug='ulgu-onduktar')

    def _post(self, follow=False, **overrides):
        data = {
            'grade': 5,
            'topics': [self.fractions.pk, self.decimals.pk],
            'test_type': GeneratedTest.TYPE_FORMATIVE,
            'question_count': 5,
            'difficulty_mix': GeneratedTest.MIX_EQUAL,
            'variant_count': 2,
        }
        data.update(overrides)
        return self.client.post(reverse('test_maker'), data, follow=follow)

    def test_login_required(self):
        response = self.client.get(reverse('test_maker'))
        self.assertRedirects(response, '/login/?next=/test-tuzuu/')

    def test_page_has_one_h1_and_preselects_the_topic(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('test_maker') + f'?tema={self.fractions.slug}&klass=5'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(headings(response.content.decode())['h1'], ['Тест түзүү'])
        html = response.content.decode()
        tags = re.findall(r'<input\b[^>]*>', html)
        tag = next(
            item for item in tags
            if f'value="{self.fractions.pk}"' in item and 'name="topics"' in item
        )
        self.assertIn('checked', tag)
        self.assertIn('Бул айда 0 / 3', html)

    def test_generates_variants_without_repeats_and_a_pdf(self):
        self.client.force_login(self.user)
        response = self._post(variant_count=4, question_count=3, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Жооп ачкычы жана баалоо схемасы')
        self.assertContains(response, 'PDF жүктөп алуу')
        generated = GeneratedTest.objects.get(user=self.user)
        self.assertEqual(generated.variant_count, 4)
        seen = []
        for variant in generated.payload['variants']:
            ids = [item['id'] for item in variant['questions']]
            self.assertEqual(len(ids), 3)
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(sum(item['points'] for item in variant['questions']), variant['points'])
            seen.append(tuple(ids))
        self.assertEqual(len(generated.payload['variants']), 4)

        pdf = self.client.get(reverse('test_maker_pdf', args=[generated.pk]))
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))

        other = _user('other@example.com', 'otheruser')
        self.client.force_login(other)
        denied = self.client.get(reverse('test_maker_pdf', args=[generated.pk]))
        self.assertEqual(denied.status_code, 404)

    def test_trial_limit_is_three_per_month_and_paid_is_unlimited(self):
        self.client.force_login(self.user)
        for _ in range(3):
            response = self._post(question_count=3, variant_count=1)
            self.assertEqual(response.status_code, 302)
        blocked = self._post(question_count=3, variant_count=1)
        self.assertEqual(blocked.status_code, 200)
        self.assertContains(blocked, 'айына 3 тест')
        self.assertEqual(GeneratedTest.objects.filter(user=self.user).count(), 3)

        GeneratedTest.objects.filter(user=self.user).update(
            created_at=timezone.now() - timedelta(days=40),
        )
        again = self._post(question_count=3, variant_count=1)
        self.assertEqual(again.status_code, 302)

        paid = _user(
            'paid@example.com',
            'paiduser',
            current_plan=PLAN_ONE_YEAR,
            subscription_end=timezone.localdate() + timedelta(days=30),
        )
        self.client.force_login(paid)
        for _ in range(4):
            response = self._post(question_count=3, variant_count=1)
            self.assertEqual(response.status_code, 302, response.content.decode()[:500])
        self.assertEqual(GeneratedTest.objects.filter(user=paid).count(), 4)
        home = self.client.get(reverse('test_maker'))
        self.assertContains(home, 'чексиз')

    def test_expired_plan_falls_back_to_the_free_limit(self):
        expired = _user(
            'expired@example.com',
            'expireduser',
            current_plan=PLAN_ONE_YEAR,
            subscription_end=timezone.localdate() - timedelta(days=1),
        )
        for _ in range(3):
            GeneratedTest.objects.create(
                user=expired,
                grade=5,
                test_type=GeneratedTest.TYPE_FORMATIVE,
                question_count=1,
                variant_count=1,
                difficulty_mix=GeneratedTest.MIX_EQUAL,
                payload={},
            )
        self.client.force_login(expired)
        blocked = self._post(question_count=3, variant_count=1)
        self.assertEqual(blocked.status_code, 200)
        self.assertContains(blocked, 'айына 3 тест')

    def test_too_many_questions_does_not_spend_the_quota(self):
        self.client.force_login(self.user)
        response = self._post(question_count=30, variant_count=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'жарыяланган суроо')
        self.assertEqual(GeneratedTest.objects.filter(user=self.user).count(), 0)

    def test_unpublished_questions_are_left_out(self):
        Question.objects.filter(grade=5).update(is_published=False)
        self.client.force_login(self.user)
        response = self._post(question_count=1, variant_count=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(GeneratedTest.objects.count(), 0)

    def test_hard_only_borrows_when_the_bank_is_short(self):
        self.client.force_login(self.user)
        response = self._post(
            difficulty_mix=GeneratedTest.MIX_HARD,
            question_count=3,
            variant_count=1,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        generated = GeneratedTest.objects.get()
        self.assertTrue(generated.payload['borrowed'])
        ids = [item['id'] for item in generated.payload['variants'][0]['questions']]
        self.assertEqual(len(ids), len(set(ids)))

    def test_links_on_home_menu_and_topic_page(self):
        home = self.client.get(reverse('home'))
        html = home.content.decode()
        self.assertIn('home-test-card', html)
        self.assertIn(reverse('test_maker'), html)
        self.assertIn('header-test-link', html)
        self.assertEqual(headings(html)['h1'], ['Мугалимдер үчүн заманбап математикалык ресурстар'])

        topic = self.client.get(reverse('topic_detail', args=[self.fractions.slug]))
        self.assertContains(topic, 'Бул тема боюнча тест түзүү')
        self.assertContains(topic, f'tema={self.fractions.slug}')
        self.assertEqual(headings(topic.content.decode())['h1'], [self.fractions.title])

        Subtopic.objects.create(title='Кошуу', slug='ulgu-koshuu', topic=self.fractions)
        sub = self.client.get(reverse('subtopic_detail', args=[self.fractions.slug, 'ulgu-koshuu']))
        self.assertContains(sub, 'Бул тема боюнча тест түзүү')
        self.assertContains(sub, f'tema={self.fractions.slug}')


class PdfFontTests(TestCase):
    def test_pdf_uses_a_kyrgyz_font_and_hides_the_key_on_the_question_page(self):
        payload = {
            'grade': 5,
            'grade_label': '5-класс',
            'test_type': 'formative',
            'test_type_label': 'Калыптандыруучу',
            'mix_label': 'Баары бирдей',
            'topics_label': 'Бөлчөктөр (үлгү)',
            'created_label': '05.11.2026',
            'borrowed': False,
            'sample_only': True,
            'marking_note': 'Ар бир суроого жазылган балл коюлат.',
            'variants': [{
                'number': 1,
                'points': 2,
                'questions': [{
                    'id': 1,
                    'number': 1,
                    'text': 'Маселени чыгар. Кеңдиги 2,5 м болсо, бөлүгү канча?',
                    'type': 'word_problem',
                    'type_label': 'Тексттик маселе',
                    'options': [],
                    'answer': '750',
                    'points': 2,
                    'difficulty': 'medium',
                    'difficulty_label': 'Орто',
                    'topic': 'Бөлчөктөр (үлгү)',
                    'is_sample': True,
                }],
            }],
        }
        pdf = render_test_pdf(payload)
        self.assertTrue(pdf.startswith(b'%PDF'))
        doc = pymupdf.open(stream=pdf, filetype='pdf')
        self.assertGreaterEqual(doc.page_count, 2)
        question_page = doc[0].get_text()
        key_page = ''.join(page.get_text() for page in doc)
        self.assertIn('Кеңдиги', question_page)
        self.assertIn('бөлүгү', question_page)
        self.assertIn('2,5', question_page)
        self.assertNotIn('Жооп ачкычы', question_page)
        self.assertNotIn('750', question_page)
        self.assertIn('Жооп ачкычы', key_page)
        self.assertIn('750', key_page)
        font_names = [font[3] for font in doc[0].get_fonts()]
        self.assertTrue(
            any('MathKG-Kyrgyz' in name or 'DejaVu' in name for name in font_names),
            font_names,
        )
