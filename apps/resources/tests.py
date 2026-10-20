import tempfile
from datetime import date, timedelta

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.account.models import Account, SubscriptionRequest
from apps.resources.free_download import choose_free_resource
from apps.resources.models import NewsPost, PageFreeDownload, Resource, ResourceDownload, SearchQuery


class PagesTests(TestCase):

    def test_news_list_orders_newest_first(self):
        older = NewsPost.objects.create(
            title='Эски жаңылык',
            body='Эски.',
            published_date=date(2026, 9, 16),
        )
        newer = NewsPost.objects.create(
            title='Жаңы жаңылык',
            body='Жаңы.',
            published_date=date(2026, 9, 22),
        )
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])
        self.assertEqual(posts, [newer, older])

    def test_news_post_formatted_date_is_kyrgyz(self):
        post = NewsPost.objects.create(
            title='Тест',
            body='Тест.',
            published_date=date(2026, 9, 22),
        )
        self.assertEqual(post.formatted_date(), '22-сентябрь, 2026-жыл')

    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_shows_plan_download_limits(self):
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'Күнүнө 1 презентация')
        self.assertContains(resp, 'Күнүнө 5 презентация')
        self.assertContains(resp, 'Чексиз жүктөп алуу')


class ResourceCategoryLabelTests(TestCase):
    def test_category_labels_are_kyrgyz(self):
        self.assertEqual(Resource(category='presentation').get_category_display(), 'Презентация')
        self.assertEqual(Resource(category='worksheet').get_category_display(), 'Иш барак')
        self.assertEqual(Resource(category='activity').get_category_display(), 'Мугалим жетектеген ишмердик')


class DownloadEligibilityDisplayTests(TestCase):
    """A download button used to show identically whether or not the
    user's subscription was actually still active, only erroring after
    the click. These pages should show the real state upfront instead."""

    def setUp(self):
        self.user = Account.objects.create_user(
            email='eligibility@example.com', username='eligibility', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.client.login(email='eligibility@example.com', password='SuperSecret123!')

    def _expire_subscription(self):
        self.user.subscription_end = timezone.now().date() - timedelta(days=1)
        self.user.save(update_fields=['subscription_end'])

    def test_operation_block_shows_renewal_prompt_when_subscription_expired(self):
        self._expire_subscription()
        resp = self.client.get(reverse('koshuu_1_digit'))
        self.assertContains(resp, 'Жазылууңуздун мөөнөтү бүткөн')

    def test_operation_block_does_not_show_renewal_prompt_with_active_subscription(self):
        resp = self.client.get(reverse('koshuu_1_digit'))
        self.assertNotContains(resp, 'Жазылууңуздун мөөнөтү бүткөн')

    def test_directed_numbers_shows_renewal_prompt_when_subscription_expired(self):
        self._expire_subscription()
        resp = self.client.get(reverse('directed_numbers'))
        self.assertContains(resp, 'Жазылууңуздун мөөнөтү бүткөн')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AlgebraLinearLessonPageTests(TestCase):
    """The one-step-equations lesson page (algebra-linear-var1side-noncalc-1step)
    used to be a bare 'materials being prepared' placeholder - it now has a
    real presentation wired up through the same operation_block.html pattern
    as four_basic_operations/koshuu_1_digit."""

    def setUp(self):
        self.user = Account.objects.create_user(
            email='algebra@example.com', username='algebrauser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.client.login(email='algebra@example.com', password='SuperSecret123!')

    def test_page_shows_real_download_once_the_resource_exists(self):
        Resource.objects.create(
            title='Algebra-OneStepVar1Side-NonCalc.pptx',
            category='presentation', is_active=True,
            file=SimpleUploadedFile('Algebra-OneStepVar1Side-NonCalc.pptx', b'data'),
        )
        resp = self.client.get(reverse('algebra_linear_var1side_noncalc_1step'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Белгисиз бир жагында')
        self.assertContains(resp, 'PPT')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SubtractingOneDigitPageTests(TestCase):
    """subtracting-1-digit used to be a bare 'materials being prepared'
    placeholder - it now has real resources wired up through the same
    operation_block.html pattern as koshuu_1_digit."""

    def setUp(self):
        self.user = Account.objects.create_user(
            email='subtracting@example.com', username='subtractinguser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.client.login(email='subtracting@example.com', password='SuperSecret123!')

    def test_page_shows_real_download_once_the_resource_exists(self):
        Resource.objects.create(
            title='Onduktar_KemituuBingo.pptx',
            category='presentation', is_active=True,
            file=SimpleUploadedFile('Onduktar_KemituuBingo.pptx', b'data'),
        )
        resp = self.client.get(reverse('subtracting_1_digit'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Бинго')
        self.assertContains(resp, 'PPT')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AddingSubtractingOneDigitPageTests(TestCase):
    """adding-subtracting-1-digit used to be a bare 'materials being
    prepared' placeholder - it now has real resources wired up through
    the same operation_block.html pattern as koshuu_1_digit."""

    def setUp(self):
        self.user = Account.objects.create_user(
            email='addsub@example.com', username='addsubuser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.client.login(email='addsub@example.com', password='SuperSecret123!')

    def test_page_shows_real_download_once_the_resource_exists(self):
        Resource.objects.create(
            title='Onduktar_Koshuu_Kemituu_Bingo.pptx',
            category='presentation', is_active=True,
            file=SimpleUploadedFile('Onduktar_Koshuu_Kemituu_Bingo.pptx', b'data'),
        )
        resp = self.client.get(reverse('adding_subtracting_1_digit'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Бинго')
        self.assertContains(resp, 'PPT')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SearchViewTests(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def _make_resource(self, title, description=''):
        return Resource.objects.create(
            title=title, description=description, category='presentation', is_active=True,
            file=SimpleUploadedFile(f'{title}.txt', b'data'),
        )

    def test_query_below_the_minimum_length_runs_no_search(self):
        self._make_resource('Алгебра')
        resp = self.client.get(reverse('search'), {'q': 'а'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['has_results'])

    def test_query_at_the_minimum_length_finds_a_matching_resource(self):
        self._make_resource('Алгебра: киришүү')
        resp = self.client.get(reverse('search'), {'q': 'ал'})
        self.assertTrue(resp.context['has_results'])

    def test_repeated_requests_beyond_the_rate_limit_are_blocked(self):
        for _ in range(30):
            resp = self.client.get(reverse('search'), {'q': 'математика'})
            self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('search'), {'q': 'математика'})
        self.assertEqual(resp.status_code, 403)

    def test_submitting_a_search_logs_a_search_query(self):
        self._make_resource('Алгебра: киришүү')
        self.client.get(reverse('search'), {'q': 'алгебра'})
        self.assertEqual(SearchQuery.objects.count(), 1)
        logged = SearchQuery.objects.get()
        self.assertEqual(logged.query, 'алгебра')
        self.assertEqual(logged.results_count, 1)

    def test_zero_result_search_is_logged_with_a_zero_count(self):
        self.client.get(reverse('search'), {'q': 'жокнерсе'})
        logged = SearchQuery.objects.get()
        self.assertEqual(logged.results_count, 0)

    def test_query_below_the_minimum_length_is_not_logged(self):
        self.client.get(reverse('search'), {'q': 'а'})
        self.assertEqual(SearchQuery.objects.count(), 0)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DownloadLimitEnforcementTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='dl@example.com', username='dluser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.current_plan = SubscriptionRequest.PLAN_THREE_MONTHS
        self.user.save(update_fields=['is_active', 'current_plan'])
        self.client.login(email='dl@example.com', password='SuperSecret123!')

    def _make_resource(self, category, title='R'):
        return Resource.objects.create(
            title=title, category=category, is_active=True,
            file=SimpleUploadedFile(f'{title}.txt', b'data'),
        )

    def test_second_same_day_download_in_same_category_is_blocked(self):
        first = self._make_resource('presentation', 'First')
        second = self._make_resource('presentation', 'Second')
        self.client.get(reverse('download_resource', args=[first.pk]))
        resp = self.client.get(reverse('download_resource', args=[second.pk]), follow=True)
        self.assertContains(resp, 'чегине жеттиңиз')
        self.assertEqual(ResourceDownload.objects.filter(resource=second).count(), 0)

    def test_different_category_is_unaffected_by_other_categorys_limit(self):
        presentation = self._make_resource('presentation', 'P')
        worksheet = self._make_resource('worksheet', 'W')
        self.client.get(reverse('download_resource', args=[presentation.pk]))
        resp = self.client.get(reverse('download_resource', args=[worksheet.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_redownloading_the_same_resource_is_never_blocked(self):
        # Review finding: a retry or accidental double-click used to be
        # blocked as "limit reached" on the very file the user just got.
        resource = self._make_resource('presentation', 'P')
        self.client.get(reverse('download_resource', args=[resource.pk]))
        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_a_file_missing_from_disk_shows_a_friendly_error_instead_of_crashing(self):
        resource = self._make_resource('presentation', 'Gone')
        import os
        os.remove(resource.file.path)
        resp = self.client.get(reverse('download_resource', args=[resource.pk]), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'жеткиликсиз')
        self.assertEqual(ResourceDownload.objects.filter(resource=resource).count(), 0)

    def test_a_different_resource_is_still_blocked_after_the_limit_is_used(self):
        first = self._make_resource('presentation', 'First')
        second = self._make_resource('presentation', 'Second')
        self.client.get(reverse('download_resource', args=[first.pk]))
        self.client.get(reverse('download_resource', args=[first.pk]))
        resp = self.client.get(reverse('download_resource', args=[second.pk]), follow=True)
        self.assertContains(resp, 'чегине жеттиңиз')

    def test_one_year_plan_has_no_limit(self):
        self.user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        self.user.save(update_fields=['current_plan'])
        for i in range(6):
            r = self._make_resource('presentation', f'P{i}')
            resp = self.client.get(reverse('download_resource', args=[r.pk]))
            self.assertEqual(resp.status_code, 200)

    def test_anonymous_download_redirects_to_login(self):
        resource = self._make_resource('presentation', 'Anon')
        self.client.logout()
        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp.url)

    def test_expired_subscription_blocks_before_the_limit_check_runs(self):
        self.user.subscription_end = timezone.now().date() - timedelta(days=1)
        self.user.save(update_fields=['subscription_end'])
        resource = self._make_resource('presentation', 'P')
        resp = self.client.get(reverse('download_resource', args=[resource.pk]), follow=True)
        self.assertContains(resp, 'мөөнөтү бүткөн')
        self.assertNotContains(resp, 'чегине жеттиңиз')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class FreeDownloadTests(TestCase):
    def setUp(self):
        self.free = self._make_resource('FreeFile')
        self.paid = self._make_resource('PaidFile')
        choose_free_resource('unit-page', [self.free, self.paid])
        PageFreeDownload.objects.filter(page_key='unit-page').update(
            resource=self.free, pinned=True,
        )

    def _make_resource(self, title, category='presentation'):
        return Resource.objects.create(
            title=title, category=category, is_active=True,
            file=SimpleUploadedFile(f'{title}.bin', b'data'),
        )

    def _account(self, email, plan, end):
        user = Account.objects.create_user(
            email=email, username=email.split('@')[0], password='SuperSecret123!',
        )
        user.is_active = True
        user.current_plan = plan
        user.subscription_end = end
        user.save(update_fields=['is_active', 'current_plan', 'subscription_end'])
        return user

    def test_anonymous_can_download_the_free_file(self):
        resp = self.client.get(reverse('download_resource', args=[self.free.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('attachment', resp['Content-Disposition'])

    def test_anonymous_other_file_redirects_to_login(self):
        resp = self.client.get(reverse('download_resource', args=[self.paid.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp.url)

    def test_expired_can_download_the_free_file_and_is_refused_the_other(self):
        self._account(
            'expired-free@example.com',
            SubscriptionRequest.PLAN_THREE_MONTHS,
            timezone.now().date() - timedelta(days=1),
        )
        self.client.login(email='expired-free@example.com', password='SuperSecret123!')
        free_resp = self.client.get(reverse('download_resource', args=[self.free.pk]))
        self.assertEqual(free_resp.status_code, 200)
        paid_resp = self.client.get(reverse('download_resource', args=[self.paid.pk]))
        self.assertEqual(paid_resp.status_code, 302)
        self.assertIn('/account/', paid_resp.url)

    def test_active_subscription_can_download_both(self):
        self._account(
            'active-free@example.com',
            SubscriptionRequest.PLAN_ONE_YEAR,
            timezone.now().date() + timedelta(days=30),
        )
        self.client.login(email='active-free@example.com', password='SuperSecret123!')
        for resource in (self.free, self.paid):
            resp = self.client.get(reverse('download_resource', args=[resource.pk]))
            self.assertEqual(resp.status_code, 200)

    def test_the_free_file_stays_the_same_and_an_admin_pin_wins(self):
        first = choose_free_resource('stable-page', [self.free, self.paid])
        second = choose_free_resource('stable-page', [self.free, self.paid])
        self.assertEqual(first.id, second.id)
        pinned = self.paid if first.id == self.free.id else self.free
        PageFreeDownload.objects.filter(page_key='stable-page').update(
            resource=pinned, pinned=True,
        )
        self.assertEqual(choose_free_resource('stable-page', [self.free, self.paid]).id, pinned.id)

    def test_to_fractions_shows_one_free_badge_to_anonymous_visitors(self):
        prefix = 'Ekvivalenettuuluk_Onduktardan_menen_Bolchoktor-'
        self._make_resource(prefix + '1234.pptx')
        self._make_resource(prefix + 'BingoOyunu.pptx')
        resp = self.client.get(reverse('to_fractions'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.decode().count('Акысыз'), 1)
        self.assertContains(resp, 'Файлды жүктөп алуу үчүн сайтка катталышыңыз керек')

    def test_four_basic_operations_shows_one_free_badge_to_anonymous_visitors(self):
        self._make_resource('4-Amal-intro.pptx')
        one = self._make_resource('amaldar_tartibi_ozun_tuz_v2.pptx')
        # The live page already stored this file. Pinning it here checks
        # that a saved choice for page_key four_basic_operations still wins.
        choose_free_resource('four_basic_operations', [one])
        PageFreeDownload.objects.filter(page_key='four_basic_operations').update(
            resource=one, pinned=True,
        )
        resp = self.client.get(reverse('four_basic_operations'))
        html = resp.content.decode()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(html.count('Акысыз'), 1)
        self.assertIn(f'/resources/download/{one.pk}/', html)
        self.assertRegex(
            html,
            rf'3C · 3[\s\S]*?Амалдар тартиби: Өзүң түз[\s\S]*?'
            rf'/resources/download/{one.pk}/[\s\S]*?Акысыз',
        )
        self.assertNotIn('1-2-3-4', html)
        self.assertIn('Жаратуу', html)
        self.assertContains(resp, 'Файлды жүктөп алуу үчүн сайтка катталышыңыз керек')
        self.assertContains(resp, 'mk-zoom')

    def test_four_basic_materials_keep_order_and_files(self):
        from apps.resources.data.four_basic_operations_data import (
            FOUR_BASIC_OPERATIONS_SECTIONS,
        )
        from apps.resources.topic_pages import FOUR_BASIC_OPERATIONS
        expected = [
            (block['title'], list(block['files']))
            for section in FOUR_BASIC_OPERATIONS_SECTIONS
            for block in section['blocks']
        ]
        got = [
            (item['title'], [name for _label, name in item['files']])
            for section in FOUR_BASIC_OPERATIONS['sections']
            for item in section['items']
            if item['grade'] == 0
        ]
        self.assertEqual(got, expected)
        resp = self.client.get(reverse('four_basic_operations'))
        html = resp.content.decode()
        positions = [html.index(title) for title, _files in expected]
        self.assertEqual(positions, sorted(positions))


    def test_four_basic_operations_has_grade_tabs(self):
        from apps.resources.topic_pages import FOUR_BASIC_OPERATIONS
        resp = self.client.get(reverse('four_basic_operations'))
        html = resp.content.decode()
        for label in ('Жалпы', '1-класс', '2-класс', '3-класс', '4-класс', '5-класс'):
            self.assertIn(f'>{label}<span class="grade-tab__count">', html)
        self.assertIn('data-grade="3"', html)
        self.assertIn('Көбөйтүү жадыбалы', html)
        self.assertIn('mk-zoom--read', html)
        # Switching grades must mark the newly shown rows as revealed.
        # They start hidden, and the scroll-in observer does not fire
        # when `hidden` is removed, which left them at opacity 0.
        self.assertIn("if (show) r.classList.add('is-in')", html)
        # Every grade-level file ships with the app and every thumbnail exists.
        from pathlib import Path
        from django.contrib.staticfiles import finders
        bundled = Path(__file__).resolve().parent / 'bundled_files'
        for section in FOUR_BASIC_OPERATIONS['sections']:
            for item in section['items']:
                if not item['grade']:
                    continue
                for _label, name in item['files']:
                    self.assertTrue((bundled / name).is_file(), name)
                image = FOUR_BASIC_OPERATIONS['images'][item['svg']]
                self.assertIsNotNone(finders.find(image), image)
        for res in FOUR_BASIC_OPERATIONS['teacher_resources']:
            for _label, name in res['files']:
                self.assertTrue((bundled / name).is_file(), name)

    def test_grade_topic_pages_render_with_their_files(self):
        from pathlib import Path
        from django.contrib.staticfiles import finders
        from apps.resources.data.grade_topic_pages import GRADE_TOPIC_PAGES, NEW_FILES
        bundled = Path(__file__).resolve().parent / 'bundled_files'
        for name in NEW_FILES:
            self.assertTrue((bundled / name).is_file(), name)
        found = set(Resource.objects.filter(title__in=NEW_FILES, is_active=True).values_list('title', flat=True))
        self.assertEqual(found, set(NEW_FILES))
        for spec in GRADE_TOPIC_PAGES:
            for image in spec['images'].values():
                self.assertIsNotNone(finders.find(image), image)
        html = self.client.get(reverse('koshuu_1_digit')).content.decode()
        self.assertIn('topic-page__grade', html)
        self.assertIn('5-класс', html)
        html = self.client.get(reverse('integers_adding_subtracting_1_2_digit')).content.decode()
        self.assertIn('>1-класс<span class="grade-tab__count">', html)
        self.assertIn('>2-класс<span class="grade-tab__count">', html)
        html = self.client.get(reverse('hcf_lcm_prime_factorisation_mixed')).content.decode()
        self.assertIn('6-класс', html)
        self.assertIn('Атышуу', html)

    def test_directed_numbers_page_has_grade_packs_and_older_activities(self):
        from pathlib import Path
        from django.contrib.staticfiles import finders
        from apps.resources.data.directed_numbers_page import DIRECTED_NUMBERS, NEW_FILES
        from apps.resources.models import SubSubtopic, Subtopic, Topic
        bundled = Path(__file__).resolve().parent / 'bundled_files'
        for name in NEW_FILES:
            self.assertTrue((bundled / name).is_file(), name)
        found = set(Resource.objects.filter(title__in=NEW_FILES, is_active=True).values_list('title', flat=True))
        self.assertEqual(found, set(NEW_FILES))
        for image in DIRECTED_NUMBERS['images'].values():
            self.assertIsNotNone(finders.find(image), image)
        topic = Topic.objects.create(title='Сандар', slug='sandar-dn-test')
        subtopic = Subtopic.objects.create(title='Багытталган сандар', slug='bagyttalgan-dn-test', topic=topic)
        sub = SubSubtopic.objects.create(title='Эсептөөлөр', slug='eseptoo-dn-test', subtopic=subtopic)
        Resource.objects.create(title='4-Amal-BagyttalganSandarMenenBingo.pptx', file='resources/files/b.pptx',
                                category='activity', is_active=True, topic=topic, subtopic=subtopic,
                                subsubtopic=sub)
        html = self.client.get(reverse('directed_numbers')).content.decode()
        for label in ('>Жалпы<', '>5-класс<', '>6-класс<'):
            self.assertIn(label, html)
        self.assertIn('Бинго', html)
        self.assertIn('Атышуу', html)

    def test_grade_level_resources_exist_after_migrations(self):
        from apps.resources.data.four_basic_operations_grades import (
            GRADE_ITEMS,
            GRADE_TEACHER_FILES,
        )
        names = {name for _s, item in GRADE_ITEMS for _l, name in item['files']}
        names |= {name for _g, _s, name in GRADE_TEACHER_FILES}
        found = set(Resource.objects.filter(title__in=names, is_active=True).values_list('title', flat=True))
        self.assertEqual(found, names)


class AnalyticsDashboardTests(TestCase):
    def setUp(self):
        self.staff = Account.objects.create_user(
            email='staff@example.com', username='staffuser', password='SuperSecret123!'
        )
        self.staff.is_active = True
        self.staff.is_staff = True
        self.staff.save(update_fields=['is_active', 'is_staff'])
        self.client.login(email='staff@example.com', password='SuperSecret123!')

    def test_dashboard_renders_with_the_search_queries_section(self):
        SearchQuery.objects.create(query='алгебра', results_count=3)
        SearchQuery.objects.create(query='жокнерсе', results_count=0)
        resp = self.client.get(reverse('analytics_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Top search queries')
        self.assertContains(resp, 'Searches with no results')
        self.assertContains(resp, 'жокнерсе')


class PricingPageTests(TestCase):
    def test_pricing_page_loads_and_shows_all_plans(self):
        resp = self.client.get(reverse('pricing'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '3 ай')
        self.assertContains(resp, '6 ай')
        self.assertContains(resp, '1 жыл')
        self.assertContains(resp, '1499 сом')
        self.assertContains(resp, '2999 сом')
        self.assertContains(resp, '4999 сом')
        self.assertContains(resp, 'Чексиз')

    def test_footer_links_to_pricing_page(self):
        resp = self.client.get(reverse('about'))
        self.assertContains(resp, reverse('pricing'))
        self.assertContains(resp, 'Баалар')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ResourceImageWebPConversionTests(TestCase):
    """Resource.save() re-encodes any newly-uploaded image as lossless
    WebP (see docs/deployment-notes.md) - same pixels, usually 40-60%
    smaller than the PNG/JPEG it replaces."""

    def _make_png_bytes(self):
        from io import BytesIO
        from PIL import Image as PILImage
        buf = BytesIO()
        PILImage.new('RGBA', (20, 10), (255, 0, 0, 255)).save(buf, format='PNG')
        return buf.getvalue()

    def test_uploaded_png_is_converted_to_webp_on_save(self):
        resource = Resource.objects.create(
            title='WebpTest.pptx', category='presentation', is_active=True,
            file=SimpleUploadedFile('WebpTest.pptx', b'data'),
            image=SimpleUploadedFile('shot.png', self._make_png_bytes(), content_type='image/png'),
        )
        self.assertTrue(resource.image.name.endswith('.webp'))

        from PIL import Image as PILImage
        with resource.image.open('rb') as f:
            decoded = PILImage.open(f)
            decoded.load()
            self.assertEqual(decoded.format, 'WEBP')
            self.assertEqual(decoded.size, (20, 10))

    def test_resource_without_an_image_is_unaffected(self):
        resource = Resource.objects.create(
            title='NoImage.pptx', category='presentation', is_active=True,
            file=SimpleUploadedFile('NoImage.pptx', b'data'),
        )
        self.assertFalse(resource.image)

    def test_an_already_webp_image_is_not_reconverted(self):
        resource = Resource.objects.create(
            title='AlreadyWebp.pptx', category='presentation', is_active=True,
            file=SimpleUploadedFile('AlreadyWebp.pptx', b'data'),
            image=SimpleUploadedFile('shot.png', self._make_png_bytes(), content_type='image/png'),
        )
        webp_name = resource.image.name
        resource.title = 'AlreadyWebp renamed'
        resource.save()
        self.assertEqual(resource.image.name, webp_name)
