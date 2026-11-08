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
        self.assertEqual(by_key['ulgu-tf-half']['answer'], 'А')
        self.assertEqual(Decimal('0.5'), Fraction(1, 2))
        self.assertEqual(by_key['ulgu-tf-quarter']['answer'], 'Б')
        self.assertLess(Fraction(1, 4), Fraction(1, 2))
        self.assertEqual(by_key['ulgu-match-fdp']['answer'], '1–В, 2–А, 3–Б')
        self.assertEqual(Decimal('0.25'), Fraction(1, 4))
        self.assertEqual(Decimal('0.75'), Fraction(3, 4))
        self.assertEqual(by_key['ulgu-blank-half']['answer'], '1')
        self.assertEqual(by_key['ulgu-blank-sixth']['answer'], '1')
        self.assertEqual(Fraction(3, 6), Fraction(1, 2))
        self.assertEqual(by_key['ulgu-d-times-six']['answer'], '15')
        self.assertEqual(Decimal('2.5') * 6, 15)
        self.assertEqual(by_key['ulgu-d-diagram']['answer'], '8')
        self.assertEqual(4 * 2, 8)
        self.assertEqual(by_key['ulgu-d-very-hard']['answer'], '100')
        self.assertEqual(Decimal('2.5') * 80 / 2, 100)
        from apps.resources.sample_questions import stored_format
        formats = {stored_format(row) for row in SAMPLE_QUESTIONS}
        self.assertTrue({
            'choice', 'short_response', 'extended', 'calculation', 'diagram',
            'true_false', 'matching', 'fill_blank',
        } <= formats)

        for row in SAMPLE_QUESTIONS:
            option_bits = []
            for value in row['options'].values():
                if isinstance(value, dict):
                    option_bits.extend(value.values())
                else:
                    option_bits.append(value)
            text = row['text'] + row['answer'] + row.get('solution', '') + ''.join(option_bits)
            self.assertNotIn('чеч', text)
            self.assertNotIn('оқушы', text)
            self.assertNotRegex(text, r'\d+\.\d+')
            if row['question_type'] == 'word_problem':
                self.assertIn('Маселени чыгар', row['text'])
            if 'алма' in row['text']:
                self.assertIn('окуучу', text.casefold())
            if row.get('question_format') == 'true_false':
                self.assertEqual(set(row['options']), {'А', 'Б'})
                self.assertIn(row['answer'], row['options'])
            elif row['question_type'] == 'multiple_choice':
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
        self.assertIn('question_format', registered.list_filter)
        self.assertEqual(Question._meta.get_field('difficulty').verbose_name, 'Деңгээл')

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
            'topics': ['tema-' + self.fractions.slug, 'tema-' + self.decimals.slug],
            'test_type': GeneratedTest.TYPE_FORMATIVE,
            'formats': ['choice', 'short_response', 'extended', 'true_false', 'matching', 'fill_blank'],
            'levels': ['easy', 'medium', 'hard'],
            'duration_minutes': 30,
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
            if f'value="tema-{self.fractions.slug}"' in item and 'name="topics"' in item
        )
        self.assertIn('checked', tag)
        self.assertIn('Бул айда 0 / 3', html)
        self.assertIn('Деңгээл', html)
        self.assertIn('Суроолордун түрү', html)
        self.assertIn('Кыска жооп', html)
        self.assertIn('Кеңири жооп', html)
        self.assertIn('Эсептөө', html)
        self.assertIn('Сүрөт боюнча', html)
        self.assertIn('Туура/туура эмес', html)
        self.assertIn('Дал келтирүү', html)
        self.assertIn('Боштукту толтуруу', html)
        self.assertIn('Тесттин узактыгы', html)
        self.assertIn('Убакытты көрсөтүү', html)
        self.assertIn('PDF түзүү', html)
        self.assertIn('Темаларга кайтуу', html)
        self.assertIn('Өтө оор', html)
        self.assertNotIn('Кыйындык', html)
        self.assertNotIn('кыйындык', html)
        self.assertNotIn('Суроолордун саны', html)
        self.assertEqual(len(headings(html)['h1']), 1)

    def test_generates_variants_without_repeats_and_a_pdf(self):
        self.client.force_login(self.user)
        response = self._post(variant_count=4, duration_minutes=20, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Жооп ачкычы жана баалоо схемасы')
        self.assertContains(response, 'PDF жүктөп алуу')
        generated = GeneratedTest.objects.get(user=self.user)
        self.assertEqual(generated.variant_count, 4)
        for variant in generated.payload['variants']:
            ids = [item['id'] for item in variant['questions']]
            self.assertGreaterEqual(len(ids), 1)
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(sum(item['points'] for item in variant['questions']), variant['points'])
        self.assertEqual(len(generated.payload['variants']), 4)

        pdf = self.client.get(reverse('test_maker_pdf', args=[generated.pk]))
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))

    def test_pdf_endpoint_returns_a_real_pdf(self):
        """The download Isa hit: create a paper, then GET /test-tuzuu/<id>/pdf/."""
        self.client.force_login(self.user)
        created = self._post(
            formats=['choice', 'short_response', 'extended', 'matching', 'true_false'],
            levels=['easy', 'medium'],
            duration_minutes=45,
            variant_count=1,
            show_timer='on',
            title='Бөлчөк текшерүү',
        )
        self.assertEqual(created.status_code, 302)
        generated = GeneratedTest.objects.get(user=self.user)
        self.assertTrue(generated.payload['variants'][0]['questions'])
        pdf = self.client.get(reverse('test_maker_pdf', args=[generated.pk]))
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))
        self.assertGreater(len(pdf.content), 1000)
        doc = pymupdf.open(stream=pdf.content, filetype='pdf')
        self.assertGreaterEqual(doc.page_count, 2)
        text = ''.join(page.get_text() for page in doc)
        self.assertIn('Бөлчөк текшерүү', text)
        self.assertIn('Убакыт: 45 мүнөт', text)
        self.assertIn('Жооп ачкычы', text)
        self.assertIn('5-класс', text)

        other = _user('other@example.com', 'otheruser')
        self.client.force_login(other)
        denied = self.client.get(reverse('test_maker_pdf', args=[generated.pk]))
        self.assertEqual(denied.status_code, 404)

    def test_trial_limit_is_three_per_month_and_paid_is_unlimited(self):
        self.client.force_login(self.user)
        for _ in range(3):
            response = self._post(duration_minutes=15, variant_count=1)
            self.assertEqual(response.status_code, 302)
        blocked = self._post(duration_minutes=15, variant_count=1)
        self.assertEqual(blocked.status_code, 200)
        self.assertContains(blocked, 'айына 3 тест')
        self.assertEqual(GeneratedTest.objects.filter(user=self.user).count(), 3)

        GeneratedTest.objects.filter(user=self.user).update(
            created_at=timezone.now() - timedelta(days=40),
        )
        again = self._post(duration_minutes=15, variant_count=1)
        self.assertEqual(again.status_code, 302)

        paid = _user(
            'paid@example.com',
            'paiduser',
            current_plan=PLAN_ONE_YEAR,
            subscription_end=timezone.localdate() + timedelta(days=30),
        )
        self.client.force_login(paid)
        for _ in range(4):
            response = self._post(duration_minutes=15, variant_count=1)
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
        blocked = self._post(duration_minutes=15, variant_count=1)
        self.assertEqual(blocked.status_code, 200)
        self.assertContains(blocked, 'айына 3 тест')

    def test_too_many_questions_does_not_spend_the_quota(self):
        self.client.force_login(self.user)
        response = self._post(levels=['very_hard'], formats=['diagram'], duration_minutes=5, variant_count=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'суроо жок')
        self.assertEqual(GeneratedTest.objects.filter(user=self.user).count(), 0)

    def test_unpublished_questions_are_left_out(self):
        Question.objects.filter(grade=5).update(is_published=False)
        self.client.force_login(self.user)
        response = self._post(duration_minutes=10, variant_count=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(GeneratedTest.objects.count(), 0)

    def test_hard_only_borrows_when_the_bank_is_short(self):
        self.client.force_login(self.user)
        response = self._post(
            formats=['extended'],
            levels=['easy', 'medium', 'hard', 'very_hard'],
            duration_minutes=15,
            variant_count=1,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        generated = GeneratedTest.objects.get()
        items = generated.payload['variants'][0]['questions']
        self.assertTrue(items)
        self.assertTrue(all(item['format'] == 'extended' for item in items))
        self.assertLessEqual(abs(generated.payload['planned_minutes'] - 15), 10)

    def test_each_question_format_can_appear_on_the_paper(self):
        self.client.force_login(self.user)
        written = self._post(
            formats=['extended', 'short_response'],
            duration_minutes=20,
            variant_count=1,
            show_timer='on',
            follow=True,
        )
        self.assertEqual(written.status_code, 200)
        paper = GeneratedTest.objects.get(user=self.user).payload
        items = paper['variants'][0]['questions']
        self.assertTrue(all(item['format'] in {'extended', 'short_response'} for item in items))
        self.assertTrue(any(item['solution'] for item in items))
        self.assertTrue(paper['show_timer'])
        from apps.resources.test_pdf import WRITE_LINE, _key_html, _variant_html
        html = _variant_html(paper, paper['variants'][0])
        self.assertIn(WRITE_LINE, html)
        self.assertIn('Деңгээл:', html)
        self.assertIn('Убакыт:', html)

        GeneratedTest.objects.all().delete()
        mixed = self._post(
            formats=['choice', 'true_false', 'matching', 'fill_blank', 'calculation', 'diagram', 'extended'],
            levels=['easy', 'medium', 'hard', 'very_hard'],
            duration_minutes=90,
            variant_count=1,
            follow=True,
        )
        self.assertEqual(mixed.status_code, 200)
        mixed_paper = GeneratedTest.objects.get(user=self.user).payload
        formats = {item['format'] for item in mixed_paper['variants'][0]['questions']}
        self.assertTrue({'choice', 'true_false', 'matching', 'fill_blank', 'calculation'} <= formats)
        key = _key_html(mixed_paper)
        self.assertIn('1/2 = 0,5', key)
        self.assertIn('Туура', key)
        self.assertIn('<table class="match">', _variant_html(mixed_paper, mixed_paper['variants'][0]))

    def test_links_on_home_menu_and_topic_page(self):
        home = self.client.get(reverse('home'))
        html = home.content.decode()
        self.assertNotIn('home-test-card', html)
        self.assertNotIn('бир нече варианттан турган тестти даярдаңыз', html)
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
                    'format': 'extended',
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
        # Cambridge-style page: rules block, faint squared working space, marks in [ ].
        self.assertIn('АДЕГЕНДЕ УШУЛАРДЫ ОКУ', question_page)
        self.assertIn('[2]', question_page)
        self.assertIn('ТЕСТТИН АЯГЫ', question_page)
        grid_lines = [d for d in doc[0].get_drawings() if d.get('color') and d['color'][2] > 0.9]
        self.assertGreater(len(grid_lines), 0)
        font_names = [font[3] for font in doc[0].get_fonts()]
        self.assertTrue(
            any('Inter' in name for name in font_names),
            font_names,
        )


class TourTests(TestCase):
    def test_new_user_sees_the_welcome_tour_once(self):
        user = _user('newtour@example.com', 'newtour')
        self.assertFalse(user.tour_seen)
        self.client.force_login(user)
        home = self.client.get(reverse('home'))
        self.assertContains(home, 'data-welcome-tour="1"')
        self.assertContains(home, 'data-tour="search"')
        self.assertContains(home, 'Жардам')
        marked = self.client.post(reverse('tour_seen'), {'tour': 'welcome'})
        self.assertEqual(marked.status_code, 204)
        user.refresh_from_db()
        self.assertTrue(user.tour_seen)
        again = self.client.get(reverse('home'))
        self.assertContains(again, 'data-welcome-tour="0"')

    def test_test_maker_tour_is_separate_and_name_prints(self):
        user = _user('named@example.com', 'nameduser')
        user.tour_seen = True
        user.save(update_fields=['tour_seen'])
        self.client.force_login(user)
        page = self.client.get(reverse('test_maker'))
        self.assertContains(page, 'data-test-tour="1"')
        self.assertContains(page, 'Тесттин аты')
        self.assertContains(page, 'data-tour-replay="test"')
        self.client.post(reverse('tour_seen'), {'tour': 'test'})
        user.refresh_from_db()
        self.assertTrue(user.test_tour_seen)
        self.assertTrue(user.tour_seen)
        response = self.client.post(reverse('test_maker'), {
            'grade': 5,
            'topics': ['tema-ulgu-bolchoktor'],
            'test_type': 'formative',
            'formats': ['choice'],
            'levels': ['easy'],
            'duration_minutes': 10,
            'variant_count': 1,
            'title': 'Бөлчөк текшерүү',
            'show_timer': 'on',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Бөлчөк текшерүү')
