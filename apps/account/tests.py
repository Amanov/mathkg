import re
import tempfile
from datetime import timedelta
from io import StringIO

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.resources.models import Resource, ResourceDownload

from .models import Account, SubscriptionRequest


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
        expected = self.user.date_joined.date() + timedelta(days=30)
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
