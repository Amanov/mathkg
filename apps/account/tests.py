import re
import tempfile
from datetime import date, datetime, timedelta, timezone as dt_timezone
from io import StringIO
from unittest.mock import patch

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.resources.models import Resource, ResourceDownload

from .models import Account, SubscriptionRequest, add_months, local_calendar_date


class RegistrationAndActivationTests(TestCase):
    def _register(self):
        return self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'SuperSecret123!',
            'password2': 'SuperSecret123!',
            'date_of_birth': '2000-01-01',
        })

    def test_registration_creates_inactive_user_and_sends_activation_email(self):
        self._register()
        user = Account.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/activate/', mail.outbox[0].body)

    def test_activation_link_activates_the_account(self):
        self._register()
        user = Account.objects.get(email='newuser@example.com')
        match = re.search(r'/activate/([^/]+)/([^/]+)/', mail.outbox[0].body)
        uidb64, token = match.group(1), match.group(2)

        self.client.get(f'/activate/{uidb64}/{token}/')

        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_invalid_activation_token_does_not_activate(self):
        self._register()
        user = Account.objects.get(email='newuser@example.com')
        match = re.search(r'/activate/([^/]+)/([^/]+)/', mail.outbox[0].body)
        uidb64 = match.group(1)

        self.client.get(f'/activate/{uidb64}/not-a-real-token/')

        user.refresh_from_db()
        self.assertFalse(user.is_active)


class LoginTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='existing@example.com', username='existing', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

    def test_login_with_correct_credentials_succeeds(self):
        # Regression test: AccountAuthenticationForm used to be a ModelForm
        # bound to Account, so Django ran Account.email's unique=True
        # validator on every login attempt - failing with "Account with
        # this Email already exists" for every real user, every time.
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'SuperSecret123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_with_wrong_password_fails_without_crashing(self):
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_inactive_user_cannot_log_in(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'SuperSecret123!',
        })
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_inactive_user_with_correct_password_sees_activation_message_not_wrong_password(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'SuperSecret123!',
        })
        self.assertContains(response, 'активдештирилген эмес')
        self.assertNotContains(response, 'туура эмес')

    def test_inactive_user_with_wrong_password_still_sees_generic_message(self):
        # An inactive account doesn't leak "your password would have been
        # right" to someone who doesn't actually know the password.
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        response = self.client.post(reverse('login'), {
            'email': 'existing@example.com',
            'password': 'wrong-password',
        })
        self.assertContains(response, 'туура эмес')
        self.assertNotContains(response, 'активдештирилген эмес')


class ResendActivationTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='pending@example.com', username='pending', password='SuperSecret123!'
        )
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])

    def test_resend_sends_a_fresh_activation_email_for_an_inactive_account(self):
        response = self.client.post(reverse('resend_activation'), {'email': 'pending@example.com'})
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/activate/', mail.outbox[0].body)

    def test_resend_shows_the_same_message_for_an_unknown_email(self):
        response = self.client.post(
            reverse('resend_activation'), {'email': 'nobody@example.com'}, follow=True,
        )
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, 'жиберилди')

    def test_resend_does_not_email_an_already_active_account(self):
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        response = self.client.post(
            reverse('resend_activation'), {'email': 'pending@example.com'}, follow=True,
        )
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, 'жиберилди')


class AccountUpdateTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='update@example.com', username='updateuser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.client.force_login(self.user)

    def test_get_renders_form_with_current_values(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['account_form'].instance, self.user)

    def test_post_actually_saves_changes(self):
        # Regression test: account_view used to have no POST handling at
        # all, so submitting this form was a silent no-op.
        response = self.client.post(reverse('account'), {
            'email': 'update@example.com',
            'username': 'renamed-user',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'renamed-user')

    def test_duplicate_email_is_rejected(self):
        Account.objects.create_user(
            email='taken@example.com', username='someoneelse', password='x'
        )
        response = self.client.post(reverse('account'), {
            'email': 'taken@example.com',
            'username': 'updateuser',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'update@example.com')


class SuperuserTests(TestCase):
    def test_create_superuser_is_active(self):
        # Regression test: create_superuser never set is_active=True, so a
        # freshly created superuser (is_active defaults to False on this
        # model) could not log in anywhere until manually fixed in the DB.
        admin = Account.objects.create_superuser(
            email='admin@example.com', username='admin', password='SuperSecret123!'
        )
        self.assertTrue(admin.is_active)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DownloadLimitTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='limits@example.com', username='limitsuser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

    def _make_resource(self, category, title='R'):
        return Resource.objects.create(
            title=title, category=category, is_active=True,
            file=SimpleUploadedFile(f'{title}.txt', b'data'),
        )

    def test_trial_user_has_3month_tier_limits(self):
        self.assertEqual(self.user.daily_download_limit('presentation'), 1)
        self.assertEqual(self.user.daily_download_limit('worksheet'), 1)
        self.assertEqual(self.user.daily_download_limit('activity'), 1)

    def test_three_month_plan_has_same_limits_as_trial(self):
        self.user.current_plan = SubscriptionRequest.PLAN_THREE_MONTHS
        self.assertEqual(self.user.daily_download_limit('presentation'), 1)

    def test_six_month_plan_allows_five_per_category(self):
        self.user.current_plan = SubscriptionRequest.PLAN_SIX_MONTHS
        self.assertEqual(self.user.daily_download_limit('presentation'), 5)
        self.assertEqual(self.user.daily_download_limit('worksheet'), 5)
        self.assertEqual(self.user.daily_download_limit('activity'), 5)

    def test_one_year_plan_is_unlimited(self):
        self.user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        self.assertIsNone(self.user.daily_download_limit('presentation'))
        self.assertIsNone(self.user.downloads_remaining_today('presentation'))

    def test_downloads_remaining_today_counts_todays_downloads(self):
        resource = self._make_resource('worksheet')
        ResourceDownload.objects.create(resource=resource, user=self.user)
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 0)

    def test_categories_are_tracked_independently(self):
        presentation = self._make_resource('presentation', 'P')
        ResourceDownload.objects.create(resource=presentation, user=self.user)
        self.assertEqual(self.user.downloads_remaining_today('presentation'), 0)
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 1)

    def test_redownloading_the_same_resource_only_counts_once(self):
        # Review finding: a retry or accidental double-click used to burn
        # a second slot of the daily quota for the exact same file.
        self.user.current_plan = SubscriptionRequest.PLAN_SIX_MONTHS
        resource = self._make_resource('worksheet')
        ResourceDownload.objects.create(resource=resource, user=self.user)
        ResourceDownload.objects.create(resource=resource, user=self.user)
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 4)

    def test_yesterdays_download_does_not_count_against_todays_limit(self):
        resource = self._make_resource('worksheet')
        download = ResourceDownload.objects.create(resource=resource, user=self.user)
        ResourceDownload.objects.filter(pk=download.pk).update(
            downloaded_at=timezone.now() - timedelta(days=1)
        )
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 1)

    def test_trial_days_defaults_to_seven_for_new_accounts(self):
        self.assertEqual(self.user.trial_days, 7)

    def test_subscription_end_date_uses_trial_days(self):
        self.user.trial_days = 30
        expected = local_calendar_date(self.user.date_joined) + timedelta(days=30)
        self.assertEqual(self.user.subscription_end_date, expected)

    def test_explicit_subscription_end_overrides_trial(self):
        self.user.subscription_end = timezone.now().date() - timedelta(days=1)
        self.assertEqual(self.user.subscription_end_date, self.user.subscription_end)


class SubscriptionRequestNotificationTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='payer@example.com', username='payer', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

    def test_creating_a_request_emails_the_admin(self):
        SubscriptionRequest.objects.create(user=self.user, plan=SubscriptionRequest.PLAN_SIX_MONTHS)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('payer@example.com', mail.outbox[0].body)
        from django.conf import settings
        self.assertEqual(mail.outbox[0].to, [settings.ADMIN_NOTIFICATION_EMAIL])

    def test_activating_an_existing_request_does_not_send_a_second_notification(self):
        request = SubscriptionRequest.objects.create(user=self.user, plan=SubscriptionRequest.PLAN_SIX_MONTHS)
        mail.outbox.clear()
        request.activate()
        self.assertEqual(len(mail.outbox), 0)


class RepairSubscriptionsBackfillsCurrentPlanTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='backfill@example.com', username='backfilluser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        # .activate() is what realistically sets subscription_end/is_active
        # (and, after Task 1, current_plan) from a confirmed request. Null
        # current_plan back out afterward to simulate a payment that was
        # confirmed *before* current_plan existed as a field - exactly the
        # account repair_subscriptions needs to backfill.
        self.request = SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_ONE_YEAR,
            status=SubscriptionRequest.STATUS_PENDING,
        )
        self.request.activate()
        self.user.current_plan = None
        self.user.save(update_fields=['current_plan'])

    def test_dry_run_does_not_write(self):
        call_command('repair_subscriptions', stdout=StringIO())
        self.user.refresh_from_db()
        self.assertIsNone(self.user.current_plan)

    def test_apply_backfills_current_plan_from_last_confirmed_request(self):
        call_command('repair_subscriptions', '--apply', stdout=StringIO())
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_ONE_YEAR)

    def test_apply_uses_the_latest_of_multiple_confirmed_requests(self):
        SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
            status=SubscriptionRequest.STATUS_CONFIRMED,
            activated_at=timezone.now(),
        )
        call_command('repair_subscriptions', '--apply', stdout=StringIO())
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_THREE_MONTHS)

    def test_rerunning_apply_is_idempotent(self):
        call_command('repair_subscriptions', '--apply', stdout=StringIO())
        second_run_output = StringIO()
        call_command('repair_subscriptions', '--apply', stdout=second_run_output)
        self.assertIn('Fixed 0 of', second_run_output.getvalue())


class BackfillCurrentPlanMigrationTests(TestCase):
    """The repair_subscriptions command only backfills current_plan when
    someone runs it by hand in production - a review finding on this
    feature pointed out that leaves every pre-existing paying account
    capped at trial limits (1/day) from the moment this ships until that
    manual step happens. This data migration closes that gap by running
    the same backfill automatically as part of `manage.py migrate`."""

    def test_backfills_current_plan_from_latest_confirmed_request(self):
        from apps.account.migration_utils import backfill_current_plan as _backfill_current_plan

        user = Account.objects.create_user(
            email='migrate1@example.com', username='migrate1', password='SuperSecret123!'
        )
        SubscriptionRequest.objects.create(
            user=user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
            status=SubscriptionRequest.STATUS_CONFIRMED,
        )
        SubscriptionRequest.objects.create(
            user=user, plan=SubscriptionRequest.PLAN_ONE_YEAR,
            status=SubscriptionRequest.STATUS_CONFIRMED,
        )
        user.current_plan = None
        user.save(update_fields=['current_plan'])

        _backfill_current_plan(Account)

        user.refresh_from_db()
        self.assertEqual(user.current_plan, SubscriptionRequest.PLAN_ONE_YEAR)

    def test_does_not_touch_an_account_with_no_confirmed_request(self):
        from apps.account.migration_utils import backfill_current_plan as _backfill_current_plan

        user = Account.objects.create_user(
            email='migrate2@example.com', username='migrate2', password='SuperSecret123!'
        )
        SubscriptionRequest.objects.create(
            user=user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
            status=SubscriptionRequest.STATUS_PENDING,
        )

        _backfill_current_plan(Account)

        user.refresh_from_db()
        self.assertIsNone(user.current_plan)

    def test_does_not_overwrite_an_already_set_current_plan(self):
        from apps.account.migration_utils import backfill_current_plan as _backfill_current_plan

        user = Account.objects.create_user(
            email='migrate3@example.com', username='migrate3', password='SuperSecret123!'
        )
        SubscriptionRequest.objects.create(
            user=user, plan=SubscriptionRequest.PLAN_ONE_YEAR,
            status=SubscriptionRequest.STATUS_CONFIRMED,
        )
        user.current_plan = SubscriptionRequest.PLAN_THREE_MONTHS
        user.save(update_fields=['current_plan'])

        _backfill_current_plan(Account)

        user.refresh_from_db()
        self.assertEqual(user.current_plan, SubscriptionRequest.PLAN_THREE_MONTHS)


class SubscriptionCalendarTests(TestCase):
    """Plan length, trial, and the account-page day count.

    The numbers below are the ones on the Test8 profile card
    (registered 18.09.2026, active through 18.03.2027, 143 days left
    on 26.10.2026, latest request a pending 3-month plan). A pending
    request does not produce that end date; a confirmed 6-month plan
    on the signup day, or two stacked 3-month plans, does.
    """

    def setUp(self):
        self.user = Account.objects.create_user(
            email='test8@example.com', username='Test8', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.date_joined = datetime(2026, 9, 18, 12, 0, tzinfo=dt_timezone.utc)
        self.user.save(update_fields=['is_active', 'date_joined'])
        self.client.force_login(self.user)

    def _activate(self, plan, on_date):
        request = SubscriptionRequest.objects.create(user=self.user, plan=plan)
        with patch('django.utils.timezone.localdate', return_value=on_date):
            request.activate()
        self.user.refresh_from_db()
        return request

    def test_add_months_uses_calendar_months_and_clamps_short_months(self):
        self.assertEqual(add_months(date(2026, 9, 18), 3), date(2026, 12, 18))
        self.assertEqual(add_months(date(2026, 9, 18), 6), date(2027, 3, 18))
        self.assertEqual(add_months(date(2026, 9, 18), 12), date(2027, 9, 18))
        self.assertEqual(add_months(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
        self.assertEqual(add_months(date(2026, 12, 18), 3), date(2027, 3, 18))

    def test_confirmed_six_month_plan_on_signup_day_ends_18_march_2027(self):
        self._activate(SubscriptionRequest.PLAN_SIX_MONTHS, date(2026, 9, 18))
        self.assertEqual(self.user.subscription_end, date(2027, 3, 18))
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_SIX_MONTHS)
        self.assertTrue(self.user.is_active)

    def test_confirmed_plan_does_not_stack_on_the_free_trial(self):
        # Grandfathered trial is 365 days from 18.09.2026, which would
        # land on 18.09.2027. Stacking 6 months on that was the old bug
        # (~18.03.2028). The paid plan replaces the trial instead.
        self.user.trial_days = 365
        self.user.subscription_end = None
        self.user.save(update_fields=['trial_days', 'subscription_end'])
        self._activate(SubscriptionRequest.PLAN_SIX_MONTHS, date(2026, 9, 18))
        self.assertEqual(self.user.subscription_end, date(2027, 3, 18))

    def test_three_month_plan_stacks_on_a_still_active_paid_period(self):
        self._activate(SubscriptionRequest.PLAN_THREE_MONTHS, date(2026, 9, 18))
        self.assertEqual(self.user.subscription_end, date(2026, 12, 18))
        self._activate(SubscriptionRequest.PLAN_THREE_MONTHS, date(2026, 10, 1))
        self.assertEqual(self.user.subscription_end, date(2027, 3, 18))

    def test_expired_paid_period_does_not_extend_the_new_plan(self):
        self.user.subscription_end = date(2026, 1, 1)
        self.user.save(update_fields=['subscription_end'])
        self._activate(SubscriptionRequest.PLAN_THREE_MONTHS, date(2026, 9, 18))
        self.assertEqual(self.user.subscription_end, date(2026, 12, 18))

    def test_activating_twice_does_not_grant_the_plan_twice(self):
        request = self._activate(SubscriptionRequest.PLAN_ONE_YEAR, date(2026, 9, 18))
        self.assertEqual(self.user.subscription_end, date(2027, 9, 18))
        request.activate()
        self.user.refresh_from_db()
        self.assertEqual(self.user.subscription_end, date(2027, 9, 18))

    def test_pending_request_does_not_extend_or_activate_access(self):
        self.user.is_active = False
        self.user.subscription_end = None
        self.user.current_plan = None
        self.user.save(update_fields=['is_active', 'subscription_end', 'current_plan'])
        SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
        )
        self.user.refresh_from_db()
        self.assertIsNone(self.user.subscription_end)
        self.assertIsNone(self.user.current_plan)
        self.assertFalse(self.user.is_active)
        self.assertEqual(
            self.user.subscription_end_date,
            date(2026, 9, 18) + timedelta(days=self.user.trial_days),
        )

    def test_pending_request_leaves_an_existing_end_date_alone(self):
        self.user.subscription_end = date(2027, 3, 18)
        self.user.current_plan = SubscriptionRequest.PLAN_SIX_MONTHS
        self.user.save(update_fields=['subscription_end', 'current_plan'])
        SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.subscription_end, date(2027, 3, 18))
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_SIX_MONTHS)

    def test_account_page_matches_the_test8_card_on_26_october_2026(self):
        self.user.subscription_end = date(2027, 3, 18)
        self.user.current_plan = SubscriptionRequest.PLAN_SIX_MONTHS
        self.user.save(update_fields=['subscription_end', 'current_plan'])
        SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
        )
        with patch('django.utils.timezone.localdate', return_value=date(2026, 10, 26)):
            response = self.client.get(reverse('account'))
        self.assertEqual(response.context['days_left'], 143)
        self.assertContains(response, '18.09.2026')
        self.assertContains(response, '18.03.2027')
        self.assertContains(response, '143 күн')
        self.assertContains(response, 'Активдүү')
        self.assertContains(response, '6 ай - 2999 сом')
        self.assertContains(response, '3 ай - 1499 сом')
        self.assertContains(response, 'Төлөм күтүлүүдө')
        self.assertContains(response, 'Ырасталмайынча мөөнөт өзгөрбөйт')
        self.assertNotContains(response, 'Мөөнөтү бүткөн')

    def test_end_date_itself_is_still_active_on_the_account_page(self):
        # Not the machine's wall-clock date: if the page still used
        # date.today(), days_left would not be 0.
        end = date(2031, 5, 4)
        self.user.subscription_end = end
        self.user.save(update_fields=['subscription_end'])
        with patch('django.utils.timezone.localdate', return_value=end):
            self.assertTrue(self.user.has_active_subscription)
            response = self.client.get(reverse('account'))
        self.assertEqual(response.context['days_left'], 0)
        self.assertContains(response, 'Активдүү')
        self.assertContains(response, 'Бүгүн аяктайт')
        self.assertContains(response, '0 күн')
        self.assertNotContains(response, 'Мөөнөтү бүткөн')
        self.assertNotContains(response, 'мурун аяктаган')

    def test_day_after_the_end_date_is_expired(self):
        self.user.subscription_end = date(2031, 5, 4)
        self.user.save(update_fields=['subscription_end'])
        with patch('django.utils.timezone.localdate', return_value=date(2031, 5, 5)):
            self.assertFalse(self.user.has_active_subscription)
            response = self.client.get(reverse('account'))
        self.assertEqual(response.context['days_left'], -1)
        self.assertContains(response, 'Мөөнөтү бүткөн')
        self.assertContains(response, '1 күн мурун аяктаган')
        self.assertNotContains(response, 'Активдүү')

    def test_days_left_follows_django_local_date_not_the_server_clock(self):
        self.user.subscription_end = date(2027, 3, 18)
        self.user.save(update_fields=['subscription_end'])
        with patch('django.utils.timezone.localdate', return_value=date(2026, 10, 27)):
            response = self.client.get(reverse('account'))
        # 18.03.2027 minus 27.10.2026. The screenshot's 143 is this same
        # subtraction for 26.10.2026; shifting "today" by one day must
        # shift the count, which date.today() would not do.
        self.assertEqual(response.context['days_left'], 142)

    def test_registration_date_and_trial_use_the_active_timezone(self):
        # 18.09.2026 19:30 UTC is still the 18th in UTC, and already
        # 19.09.2026 02:30 in Asia/Bangkok. The card and the trial must
        # agree on that local day. TIME_ZONE in settings is UTC, so this
        # only shows up when the active timezone is not UTC.
        self.user.date_joined = datetime(2026, 9, 18, 19, 30, tzinfo=dt_timezone.utc)
        self.user.subscription_end = None
        self.user.trial_days = 7
        self.user.save(update_fields=['date_joined', 'subscription_end', 'trial_days'])
        with timezone.override('Asia/Bangkok'):
            self.assertEqual(local_calendar_date(self.user.date_joined), date(2026, 9, 19))
            self.assertEqual(self.user.subscription_end_date, date(2026, 9, 26))
            response = self.client.get(reverse('account'))
        self.assertContains(response, '19.09.2026')
        self.assertNotContains(response, '18.09.2026')

    def test_creating_a_confirmed_request_in_admin_grants_access(self):
        admin = Account.objects.create_superuser(
            email='owner@example.com', username='owner', password='SuperSecret123!'
        )
        self.client.force_login(admin)
        response = self.client.post(reverse('admin:account_subscriptionrequest_add'), {
            'user': self.user.pk,
            'plan': SubscriptionRequest.PLAN_THREE_MONTHS,
            'status': SubscriptionRequest.STATUS_CONFIRMED,
            '_save': 'Save',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        request = SubscriptionRequest.objects.get(user=self.user)
        self.assertEqual(request.status, SubscriptionRequest.STATUS_CONFIRMED)
        self.assertIsNotNone(request.activated_at)
        self.assertEqual(
            self.user.subscription_end,
            add_months(timezone.localdate(), 3),
        )
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_THREE_MONTHS)
        self.assertTrue(self.user.is_active)
