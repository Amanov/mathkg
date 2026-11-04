"""Times shown to people follow Asia/Bishkek. The database stays UTC."""

import tempfile
from datetime import date, datetime, time, timedelta, timezone as dt_timezone
from unittest.mock import patch

from django.conf import settings
from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.account.admin import SubscriptionRequestAdmin
from apps.account.forms import RegistrationForm
from apps.account.models import Account, SubscriptionRequest
from apps.resources.models import NewsPost, Resource, ResourceDownload


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BishkekTimeTests(TestCase):
    def test_site_zone_is_bishkek_and_storage_stays_aware(self):
        self.assertEqual(settings.TIME_ZONE, 'Asia/Bishkek')
        self.assertTrue(settings.USE_TZ)

    def test_daily_download_counts_the_bishkek_day_not_the_utc_day(self):
        # 02:00 in Bishkek is 20:00 the previous UTC day. That download
        # is still "today" for the quota.
        user = Account.objects.create_user(
            email='quota@example.com', username='quota', password='SuperSecret123!',
        )
        user.is_active = True
        user.save(update_fields=['is_active'])
        local_today = timezone.localdate()
        two_am = timezone.make_aware(
            datetime.combine(local_today, time(2, 0)),
            timezone.get_current_timezone(),
        )
        self.assertEqual(
            two_am.astimezone(dt_timezone.utc).date(),
            local_today - timedelta(days=1),
        )
        resource = Resource.objects.create(
            title='quota.pdf', category='worksheet', is_active=True,
            file=SimpleUploadedFile('quota.pdf', b'data'),
        )
        download = ResourceDownload.objects.create(resource=resource, user=user)
        ResourceDownload.objects.filter(pk=download.pk).update(downloaded_at=two_am)
        self.assertEqual(user.downloads_remaining_today('worksheet'), 0)

    def test_admin_activation_time_is_shown_in_bishkek(self):
        user = Account.objects.create_user(
            email='paid@example.com', username='paid', password='SuperSecret123!',
        )
        request = SubscriptionRequest(
            user=user,
            plan=SubscriptionRequest.PLAN_THREE_MONTHS,
            status=SubscriptionRequest.STATUS_CONFIRMED,
            activated_at=datetime(2026, 11, 3, 20, 0, tzinfo=dt_timezone.utc),
        )
        column = SubscriptionRequestAdmin(SubscriptionRequest, admin.site)
        self.assertEqual(column.activation_status(request), '2026-11-04 02:00')

    def test_registration_form_uses_the_bishkek_today(self):
        # 2 January 2020 is in the past on the server clock, and in the
        # future if "today" is the patched local day. date.today() would
        # accept it.
        with patch('apps.account.forms.timezone.localdate', return_value=date(2020, 1, 1)):
            form = RegistrationForm(data={
                'email': 'new@example.com',
                'username': 'newteacher',
                'password1': 'SuperSecret123!',
                'password2': 'SuperSecret123!',
                'date_of_birth': '2020-01-02',
            })
            self.assertEqual(form.fields['date_of_birth'].widget.attrs['max'], '2020-01-01')
            self.assertFalse(form.is_valid())
        self.assertIn('Туулган күн келечекте болбошу керек.', form.errors['date_of_birth'])

    def test_account_page_shows_the_bishkek_registration_day(self):
        user = Account.objects.create_user(
            email='joined@example.com', username='joined', password='SuperSecret123!',
        )
        user.is_active = True
        user.date_joined = datetime(2026, 11, 3, 20, 0, tzinfo=dt_timezone.utc)
        user.subscription_end = date(2027, 1, 1)
        user.save(update_fields=['is_active', 'date_joined', 'subscription_end'])
        self.client.force_login(user)
        response = self.client.get(reverse('account'))
        self.assertContains(response, '04.11.2026')
        self.assertNotContains(response, '03.11.2026')

    def test_news_dates_stay_calendar_days(self):
        # published_date is a date, not a UTC timestamp, so Bishkek
        # midnight does not move the day the news page prints.
        post = NewsPost(
            title='Күн', body='Күн.', published_date=date(2026, 11, 4),
        )
        self.assertEqual(post.formatted_date(), '4-ноябрь, 2026-жыл')
