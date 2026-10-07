import tempfile
from datetime import date, timedelta

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.account.models import Account, SubscriptionRequest

from .models import Exam, ExamQuestion, NewsPost, Question, Resource, ResourceDownload, SearchQuery


class ExamFlowTests(TestCase):
    def setUp(self):
        self.teacher = Account.objects.create_user(
            email='teacher@example.com', username='teacher', password='SuperSecret123!'
        )
        self.teacher.is_active = True
        self.teacher.save(update_fields=['is_active'])
        self.client.login(email='teacher@example.com', password='SuperSecret123!')

        self.mcq = Question.objects.create(
            created_by=self.teacher,
            question_type='mcq',
            text='2 + 2 канча?',
            choice_a='3', choice_b='4', choice_c='5', choice_d='6',
            correct_choice='b',
            marks=2,
        )
        self.exam = Exam.objects.create(title='Сынак тест', created_by=self.teacher)
        ExamQuestion.objects.create(exam=self.exam, question=self.mcq, order=1)
        self.exam.is_published = True
        self.exam.save(update_fields=['is_published'])

    def test_question_requires_correct_choice_for_mcq(self):
        bad = Question(
            created_by=self.teacher, question_type='mcq', text='Жооп жок суроо',
            choice_a='1', choice_b='2',
        )
        with self.assertRaises(Exception):
            bad.full_clean()

    def test_unpublished_exam_is_not_takeable(self):
        self.exam.is_published = False
        self.exam.save(update_fields=['is_published'])
        resp = self.client.get(reverse('exam_take', args=[self.exam.access_code]))
        self.assertEqual(resp.status_code, 404)

    def test_published_exam_take_page_loads(self):
        resp = self.client.get(reverse('exam_take', args=[self.exam.access_code]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '2 + 2 канча?')

    def test_correct_answer_scores_full_marks(self):
        resp = self.client.post(reverse('exam_submit', args=[self.exam.access_code]), {
            'student_name': 'Айгерим',
            f'question_{self.mcq.id}': 'b',
        })
        attempt = self.exam.attempts.get(student_name='Айгерим')
        self.assertEqual(attempt.score, 2)
        self.assertRedirects(resp, reverse('exam_result', args=[self.exam.access_code, attempt.pk]))

    def test_wrong_answer_scores_zero(self):
        self.client.post(reverse('exam_submit', args=[self.exam.access_code]), {
            'student_name': 'Нурбек',
            f'question_{self.mcq.id}': 'a',
        })
        attempt = self.exam.attempts.get(student_name='Нурбек')
        self.assertEqual(attempt.score, 0)

    def test_teacher_can_create_exam_and_add_question(self):
        resp = self.client.post(reverse('exam_create'), {'title': 'Экинчи тест'})
        new_exam = Exam.objects.get(title='Экинчи тест')
        self.assertRedirects(resp, reverse('exam_detail', args=[new_exam.pk]))

        self.client.post(reverse('exam_detail', args=[new_exam.pk]), {
            'action': 'add_question', 'question_id': self.mcq.id,
        })
        self.assertTrue(
            ExamQuestion.objects.filter(exam=new_exam, question=self.mcq).exists()
        )

    def test_exam_detail_is_only_visible_to_its_owner(self):
        other = Account.objects.create_user(
            email='other@example.com', username='other', password='SuperSecret123!'
        )
        other.is_active = True
        other.save(update_fields=['is_active'])
        self.client.logout()
        self.client.login(email='other@example.com', password='SuperSecret123!')

        resp = self.client.get(reverse('exam_detail', args=[self.exam.pk]))
        self.assertEqual(resp.status_code, 404)


class PagesTests(TestCase):
    def test_news_list_shows_posts_newest_first(self):
        NewsPost.objects.create(title='Эски жаңылык', body='...', published_date=date(2026, 1, 1))
        NewsPost.objects.create(title='Жаңы жаңылык', body='...', published_date=date(2026, 6, 1))

        resp = self.client.get(reverse('news_list'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertLess(content.index('Жаңы жаңылык'), content.index('Эски жаңылык'))

    def test_news_post_formats_date_in_kyrgyz(self):
        post = NewsPost.objects.create(title='T', body='...', published_date=date(2026, 9, 22))
        self.assertEqual(post.formatted_date(), '22-сентябрь, 2026-жыл')

    def test_about_page_loads(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'MathKGZ')

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

    def test_expired_subscription_blocks_before_the_limit_check_runs(self):
        self.user.subscription_end = timezone.now().date() - timedelta(days=1)
        self.user.save(update_fields=['subscription_end'])
        resource = self._make_resource('presentation', 'P')
        resp = self.client.get(reverse('download_resource', args=[resource.pk]), follow=True)
        self.assertContains(resp, 'мөөнөтү бүткөн')
        self.assertNotContains(resp, 'чегине жеттиңиз')


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
