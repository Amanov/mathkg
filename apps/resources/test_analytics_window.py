"""Analytics dashboard cutoff: count from a chosen instant, delete nothing."""

import tempfile
from datetime import datetime, timedelta, timezone as dt_timezone

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.account.models import Account
from apps.resources.models import (
    AnalyticsWindow,
    ButtonClick,
    LoginEvent,
    PageReaction,
    PageReactionCount,
    Resource,
    ResourceDownload,
    SearchQuery,
    SiteVisit,
)
from apps.resources.views.analytics import format_stats_since


def _stamp(model, pk, **fields):
    model.objects.filter(pk=pk).update(**fields)


def _user(email, username):
    account = Account.objects.create_user(
        email=email, username=username, password='SuperSecret123!',
    )
    account.is_active = True
    account.save(update_fields=['is_active'])
    return account


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AnalyticsSinceTests(TestCase):
    def setUp(self):
        self.superuser = Account.objects.create_superuser(
            email='isa@example.com', username='isa', password='SuperSecret123!',
        )
        self.staff = _user('staff@example.com', 'staffuser')
        self.staff.is_staff = True
        self.staff.save(update_fields=['is_staff'])
        self.client.force_login(self.superuser)
        self.url = reverse('analytics_dashboard')

    def _visit(self, session_key, path, when):
        row = SiteVisit.objects.create(session_key=session_key, path=path)
        _stamp(SiteVisit, row.pk, visited_at=when)
        return row

    def _resource(self):
        return Resource.objects.create(
            title='Window.pdf',
            category='worksheet',
            is_active=True,
            file=SimpleUploadedFile('window.pdf', b'data'),
        )

    def test_rows_before_since_are_excluded_from_every_panel(self):
        now = timezone.now()
        old = now - timedelta(days=10)
        new = now - timedelta(hours=1)
        teacher_old = _user('old@example.com', 'oldteacher')
        teacher_new = _user('new@example.com', 'newteacher')
        resource = self._resource()

        self._visit('s-old', '/old-page/', old)
        self._visit('s-new', '/new-page/', new)

        click = ButtonClick.objects.create(label='ЭскиБаскыч')
        _stamp(ButtonClick, click.pk, clicked_at=old)
        click = ButtonClick.objects.create(label='ЖаңыБаскыч')
        _stamp(ButtonClick, click.pk, clicked_at=new)

        for query, results, when in (
            ('эскисуроо', 0, old),
            ('жаңысуроо', 0, new),
            ('жаңытабылды', 4, new),
        ):
            row = SearchQuery.objects.create(query=query, results_count=results)
            _stamp(SearchQuery, row.pk, searched_at=when)

        for user, when in ((teacher_old, old), (teacher_new, new)):
            row = LoginEvent.objects.create(user=user)
            _stamp(LoginEvent, row.pk, logged_in_at=when)

        for user, when in ((teacher_old, old), (teacher_new, new)):
            row = ResourceDownload.objects.create(resource=resource, user=user)
            _stamp(ResourceDownload, row.pk, downloaded_at=when)

        PageReaction.objects.create(
            path='/reaction-old/', face=PageReaction.FACE_HAPPY,
            visitor_key='a' * 32, material='ЭскиЖакты',
        )
        _stamp(PageReaction, PageReaction.objects.get(path='/reaction-old/').pk, created_at=old)
        PageReaction.objects.create(
            path='/reaction-new/', face=PageReaction.FACE_HAPPY,
            visitor_key='b' * 32, material='ЖаңыЖакты',
        )
        _stamp(PageReaction, PageReaction.objects.get(path='/reaction-new/').pk, created_at=new)
        PageReaction.objects.create(
            path='/reaction-sad/', face=PageReaction.FACE_SAD,
            visitor_key='c' * 32, material='ЖаңыКапа',
        )
        _stamp(PageReaction, PageReaction.objects.get(path='/reaction-sad/').pk, created_at=new)
        PageReactionCount.objects.create(
            path='/reaction-old/', material='ЭскиЖакты', happy_count=9,
        )

        AnalyticsWindow.set_since(now - timedelta(days=2))
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        ctx = resp.context

        self.assertEqual(ctx['total_visits'], 1)
        self.assertEqual(ctx['unique_visitors'], 1)
        self.assertEqual(ctx['visits_this_week'], 1)
        self.assertEqual(ctx['visits_this_month'], 1)
        self.assertEqual(ctx['total_sessions_tracked'], 1)
        self.assertEqual(ctx['returning_visitors'], 0)
        self.assertEqual(
            {row['path']: row['views'] for row in ctx['top_pages']},
            {'/new-page/': 1},
        )
        self.assertEqual(sum(ctx['chart_traffic_visits']), 1)

        self.assertEqual(ctx['total_clicks'], 1)
        self.assertEqual(ctx['chart_button_labels'], ['ЖаңыБаскыч'])
        self.assertNotContains(resp, 'ЭскиБаскыч')

        self.assertEqual(ctx['total_searches'], 2)
        self.assertEqual(set(ctx['chart_query_labels']), {'жаңысуроо', 'жаңытабылды'})
        self.assertEqual(
            [row['query'] for row in ctx['zero_result_queries']],
            ['жаңысуроо'],
        )
        self.assertNotContains(resp, 'эскисуроо')

        self.assertEqual(ctx['total_logins'], 1)
        self.assertEqual(ctx['logins_this_week'], 1)
        self.assertEqual(ctx['logins_this_month'], 1)
        self.assertEqual(sum(ctx['chart_traffic_logins']), 1)
        self.assertEqual(ctx['top_login_users'][0]['user__username'], 'newteacher')

        self.assertEqual(ctx['total_downloads'], 1)
        self.assertEqual(ctx['unique_users'], 1)
        self.assertEqual(ctx['downloads_this_week'], 1)
        self.assertEqual(ctx['downloads_this_month'], 1)
        self.assertEqual(sum(ctx['chart_download_counts']), 1)
        self.assertEqual(sum(ctx['chart_folder_counts']), 1)
        self.assertEqual(list(ctx['recent_downloads']), [ResourceDownload.objects.get(user=teacher_new)])
        self.assertEqual(ctx['top_users'][0]['user__username'], 'newteacher')
        self.assertEqual(ctx['top_resources'][0].dl_count, 1)
        categories = {row['category']: row['total_downloads'] for row in ctx['category_stats']}
        self.assertEqual(categories['worksheet'], 1)

        # Face totals and the ranked pages come from PageReaction rows
        # in the window, not from the all-time PageReactionCount of 9.
        self.assertEqual(ctx['reaction_happy'], 1)
        self.assertEqual(ctx['reaction_ok'], 0)
        self.assertEqual(ctx['reaction_sad'], 1)
        self.assertEqual(ctx['reaction_top_happy'][0]['path'], '/reaction-new/')
        self.assertEqual(ctx['reaction_top_happy'][0]['happy_count'], 1)
        self.assertEqual(ctx['reaction_top_sad'][0]['path'], '/reaction-sad/')
        self.assertEqual(ctx['reaction_top_sad'][0]['sad_count'], 1)
        self.assertNotContains(resp, 'ЭскиЖакты')
        self.assertContains(resp, 'ЖаңыЖакты')

        self.assertEqual(SiteVisit.objects.count(), 2)
        self.assertEqual(ResourceDownload.objects.count(), 2)
        self.assertEqual(PageReaction.objects.count(), 3)
        self.assertEqual(PageReactionCount.objects.get(path='/reaction-old/').happy_count, 9)

    def test_clearing_since_restores_all_time_totals(self):
        now = timezone.now()
        self._visit('s-old', '/old-page/', now - timedelta(days=10))
        self._visit('s-new', '/new-page/', now - timedelta(hours=1))
        # Same browser on two days after the cutoff, and another browser
        # only before it. Clearing must count the older browser again.
        self._visit('s-return', '/a/', now - timedelta(days=4))
        self._visit('s-return', '/b/', now - timedelta(days=1))
        self._visit('s-once', '/c/', now - timedelta(days=2, hours=1))
        self._visit('s-old-return', '/d/', now - timedelta(days=20))
        self._visit('s-old-return', '/e/', now - timedelta(days=15))

        AnalyticsWindow.set_since(now - timedelta(days=6))
        limited = self.client.get(self.url)
        self.assertEqual(limited.context['total_visits'], 4)
        self.assertEqual(limited.context['returning_visitors'], 1)
        self.assertEqual(limited.context['total_sessions_tracked'], 3)
        self.assertContains(limited, 'баштап эсептелүүдө')

        cleared = self.client.post(self.url, {'action': 'clear'})
        self.assertRedirects(cleared, self.url)
        self.assertIsNone(AnalyticsWindow.stored_since())

        resp = self.client.get(self.url)
        self.assertEqual(resp.context['total_visits'], 7)
        self.assertEqual(resp.context['returning_visitors'], 2)
        self.assertEqual(resp.context['new_visitors'], 3)
        self.assertEqual(resp.context['stats_since_banner'], '')
        self.assertNotContains(resp, 'баштап эсептелүүдө')
        self.assertEqual(SiteVisit.objects.count(), 7)

    def test_windows_and_session_length_start_at_the_later_bound(self):
        now = timezone.now()
        early = now - timedelta(days=5)
        late = now - timedelta(days=1)
        self._visit('early', '/early/', early)
        self._visit('late', '/late/', late)
        # 20 minutes before the cutoff, 10 minutes after it.
        burst = now - timedelta(days=10)
        self._visit('old-burst', '/1/', burst)
        self._visit('old-burst', '/2/', burst + timedelta(minutes=20))
        self._visit('new-burst', '/3/', late)
        self._visit('new-burst', '/4/', late + timedelta(minutes=10))

        teacher = _user('week@example.com', 'weekteacher')
        resource = self._resource()
        for when in (early, late):
            download = ResourceDownload.objects.create(resource=resource, user=teacher)
            _stamp(ResourceDownload, download.pk, downloaded_at=when)
            login = LoginEvent.objects.create(user=teacher)
            _stamp(LoginEvent, login.pk, logged_in_at=when)

        open_window = self.client.get(self.url)
        self.assertEqual(open_window.context['visits_this_week'], 4)
        self.assertEqual(open_window.context['avg_session_minutes'], 15.0)

        AnalyticsWindow.set_since(now - timedelta(days=3))
        resp = self.client.get(self.url)
        self.assertEqual(resp.context['total_visits'], 3)
        self.assertEqual(resp.context['visits_this_week'], 3)
        self.assertEqual(resp.context['visits_this_month'], 3)
        self.assertEqual(resp.context['unique_visitors_this_week'], 2)
        self.assertEqual(sum(resp.context['chart_traffic_visits']), 3)
        self.assertEqual(resp.context['downloads_this_week'], 1)
        self.assertEqual(resp.context['downloads_this_month'], 1)
        self.assertEqual(sum(resp.context['chart_download_counts']), 1)
        self.assertEqual(resp.context['logins_this_week'], 1)
        self.assertEqual(resp.context['logins_this_month'], 1)
        self.assertEqual(sum(resp.context['chart_traffic_logins']), 1)
        self.assertEqual(resp.context['avg_session_minutes'], 10.0)
        self.assertEqual(resp.context['engaged_sessions'], 1)
        self.assertEqual(SiteVisit.objects.count(), 6)

    def test_policy_watch_ignores_the_cutoff(self):
        now = timezone.now()
        teacher = _user('share@example.com', 'sharer')
        resource = self._resource()
        for ip in ('203.0.113.10', '203.0.113.11'):
            row = ResourceDownload.objects.create(
                resource=resource, user=teacher, ip_address=ip,
            )
            _stamp(ResourceDownload, row.pk, downloaded_at=now - timedelta(days=10))

        AnalyticsWindow.set_since(now - timedelta(days=1))
        resp = self.client.get(self.url)
        self.assertEqual(resp.context['total_downloads'], 0)
        flagged = [
            row['user__username']
            for row in resp.context['flagged_same_file_multi_ip']
        ]
        self.assertIn('sharer', flagged)
        self.assertEqual(ResourceDownload.objects.count(), 2)

    def test_only_a_superuser_can_set_or_clear_the_cutoff(self):
        page = self.client.get(self.url)
        self.assertContains(page, 'Бүгүндөн баштап эсептөө')
        self.assertContains(page, 'Баардык убакытта')
        self.assertContains(
            page,
            'Статистика ушул мөмөттөн баштап эсептелет. Эски жазуулар өчпөйт.',
        )
        self.assertContains(page, 'csrfmiddlewaretoken')
        self.assertContains(page, 'name="since"')

        self.client.force_login(self.staff)
        staff_page = self.client.get(self.url)
        self.assertEqual(staff_page.status_code, 200)
        self.assertNotContains(staff_page, 'Бүгүндөн баштап эсептөө')
        self.assertNotContains(staff_page, 'Баардык убакытта')
        self.assertContains(staff_page, 'name="since"')

        denied = self.client.post(self.url, {'action': 'since_now'})
        self.assertEqual(denied.status_code, 403)
        self.assertIsNone(AnalyticsWindow.stored_since())
        denied_clear = self.client.post(self.url, {'action': 'clear'})
        self.assertEqual(denied_clear.status_code, 403)

        outsider = _user('teacher@example.com', 'teacher')
        self.client.force_login(outsider)
        self.assertRedirects(
            self.client.post(self.url, {'action': 'since_now'}),
            f"{reverse('login')}?next={self.url}",
        )
        self.assertIsNone(AnalyticsWindow.stored_since())

        self.client.force_login(self.superuser)
        before = timezone.now()
        saved = self.client.post(self.url, {'action': 'since_now'})
        after = timezone.now()
        self.assertRedirects(saved, self.url)
        stored = AnalyticsWindow.stored_since()
        self.assertGreaterEqual(stored, before)
        self.assertLessEqual(stored, after)

        self.client.force_login(self.staff)
        self.assertEqual(self.client.post(self.url, {'action': 'clear'}).status_code, 403)
        self.assertEqual(AnalyticsWindow.stored_since(), stored)

        self.client.force_login(self.superuser)
        self.assertRedirects(self.client.post(self.url, {'action': 'clear'}), self.url)
        self.assertIsNone(AnalyticsWindow.stored_since())

    def test_since_query_previews_a_day_without_saving(self):
        now = timezone.now()
        self._visit('today', '/today/', now)
        preview = self.client.get(self.url, {'since': '2099-01-01'})
        self.assertEqual(preview.context['total_visits'], 0)
        self.assertContains(
            preview,
            'Статистика 1-январь 2099, 00:00 баштап эсептелүүдө',
        )
        self.assertContains(preview, 'Бул көрүнүш сакталган жок')
        self.assertIsNone(AnalyticsWindow.stored_since())

        ignored = self.client.get(self.url, {'since': 'not-a-date'})
        self.assertEqual(ignored.context['total_visits'], 1)
        self.assertEqual(ignored.context['stats_since_banner'], '')

        AnalyticsWindow.set_since(now - timedelta(days=1))
        preview = self.client.get(self.url, {'since': '2099-01-01'})
        self.assertEqual(preview.context['total_visits'], 0)
        self.assertEqual(
            AnalyticsWindow.stored_since(),
            now - timedelta(days=1),
        )
        stored_view = self.client.get(self.url)
        self.assertEqual(stored_view.context['total_visits'], 1)
        self.assertFalse(stored_view.context['stats_since_temporary'])

    def test_banner_uses_kyrgyz_months_in_the_active_timezone(self):
        instant = datetime(2026, 11, 4, 5, 0, tzinfo=dt_timezone.utc)
        # TIME_ZONE is UTC, so the same instant reads 05:00 until the
        # active timezone is Asia/Bishkek (UTC+6), where it is 11:00.
        self.assertEqual(
            format_stats_since(instant),
            'Статистика 4-ноябрь 2026, 05:00 баштап эсептелүүдө',
        )
        with timezone.override('Asia/Bishkek'):
            self.assertEqual(
                format_stats_since(instant),
                'Статистика 4-ноябрь 2026, 11:00 баштап эсептелүүдө',
            )
            AnalyticsWindow.set_since(instant)
            resp = self.client.get(self.url)
        self.assertContains(resp, 'Статистика 4-ноябрь 2026, 11:00 баштап эсептелүүдө')
        self.assertEqual(AnalyticsWindow.stored_since(), instant)
