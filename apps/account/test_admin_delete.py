"""Admin deletion of Account must remove the row, or say that it stayed.

Production databases created before rest_framework.authtoken was
uninstalled still have authtoken_token.user_id -> account_account,
DEFERRABLE INITIALLY DEFERRED, ON DELETE NO ACTION. Django does not
know that model, so the delete confirmation page does not list the
token. The deferred check fails at COMMIT, after the admin has queued
"deleted successfully".
"""

import importlib

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from apps.account.admin import ACCOUNT_DELETE_BLOCKED

_drop_authtoken = importlib.import_module(
    'apps.account.migrations.0014_drop_orphan_authtoken'
)
DROP_AUTHTOKEN_TABLE = _drop_authtoken.DROP_AUTHTOKEN_TABLE
FORGET_AUTHTOKEN_MIGRATIONS = _drop_authtoken.FORGET_AUTHTOKEN_MIGRATIONS
from apps.account.models import PLAN_ONE_YEAR, SubscriptionRequest
from apps.resources.models import (
    ButtonClick,
    LoginEvent,
    Resource,
    ResourceDownload,
    SearchQuery,
    SiteVisit,
)

Account = get_user_model()


def _related(user):
    SubscriptionRequest.objects.create(
        user=user,
        plan=PLAN_ONE_YEAR,
        status=SubscriptionRequest.STATUS_CONFIRMED,
    )
    resource = Resource.objects.create(
        title='delete-me.pptx',
        file='resources/files/delete-me.pptx',
        category='presentation',
        is_active=True,
    )
    download = ResourceDownload.objects.create(resource=resource, user=user)
    LoginEvent.objects.create(user=user)
    SiteVisit.objects.create(user=user, path='/home/', session_key='abc')
    ButtonClick.objects.create(user=user, label='x', path='/home/')
    SearchQuery.objects.create(user=user, query='кошуу', results_count=1)
    return download


def _create_deferred_fk(table):
    with connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        cursor.execute(
            f'CREATE TABLE {table} ('
            'id integer NOT NULL PRIMARY KEY, '
            'user_id bigint NOT NULL REFERENCES account_account (id) '
            'DEFERRABLE INITIALLY DEFERRED'
            ')'
        )


class AccountAdminDeleteTests(TestCase):
    def setUp(self):
        self.admin = Account.objects.create_superuser(
            email='admin-delete@example.com',
            username='admindelete',
            password='SuperSecret123!',
        )
        self.client.force_login(self.admin)
        self.user = Account.objects.create_user(
            email='member-delete@example.com',
            username='memberdelete',
            password='SuperSecret123!',
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.download = _related(self.user)

    def test_confirmation_lists_the_paid_subscription_request(self):
        url = reverse('admin:account_account_delete', args=[self.user.pk])
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Жазылуу суранычы')
        self.assertContains(page, '1 жыл - 4999 сом')
        self.assertContains(page, 'Төлөндү')

    def test_change_delete_view_removes_the_user(self):
        url = reverse('admin:account_account_delete', args=[self.user.pk])
        response = self.client.post(url, {'post': 'yes'})
        self.assertEqual(response.status_code, 302, getattr(response, 'content', b'')[:800])
        self.assertFalse(Account.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(SubscriptionRequest.objects.filter(user_id=self.user.pk).exists())
        self.assertFalse(LoginEvent.objects.filter(user_id=self.user.pk).exists())
        self.download.refresh_from_db()
        self.assertIsNone(self.download.user_id)
        self.assertTrue(ResourceDownload.objects.filter(pk=self.download.pk).exists())

    def test_bulk_delete_action_removes_the_user(self):
        url = reverse('admin:account_account_changelist')
        response = self.client.post(url, {
            'action': 'delete_selected',
            '_selected_action': [str(self.user.pk)],
            'post': 'yes',
        })
        self.assertLess(response.status_code, 500, getattr(response, 'content', b'')[:800])
        self.assertFalse(Account.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(SubscriptionRequest.objects.filter(user_id=self.user.pk).exists())
        follow = self.client.get(url)
        self.assertContains(follow, 'Successfully deleted')


class OrphanAuthTokenDeleteTests(TransactionTestCase):
    """The real commit must succeed when the leftover token table is present."""

    def setUp(self):
        _create_deferred_fk('authtoken_token')
        self.admin = Account.objects.create_superuser(
            email='admin-token@example.com',
            username='admintoken',
            password='SuperSecret123!',
        )
        self.client.force_login(self.admin)
        self.user = Account.objects.create_user(
            email='test9@gmail.com',
            username='test9',
            password='SuperSecret123!',
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        _related(self.user)
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO authtoken_token (id, user_id) VALUES (1, %s)',
                [self.user.pk],
            )

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS authtoken_token')

    def test_delete_view_removes_account_that_still_has_an_api_token(self):
        url = reverse('admin:account_account_delete', args=[self.user.pk])
        page = self.client.get(url)
        self.assertContains(page, 'Төлөндү')
        self.assertNotContains(page, 'authtoken')
        response = self.client.post(url, {'post': 'yes'})
        self.assertEqual(response.status_code, 302, getattr(response, 'content', b'')[:1500])
        self.assertFalse(Account.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(SubscriptionRequest.objects.filter(user_id=self.user.pk).exists())
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM authtoken_token')
            self.assertEqual(cursor.fetchone()[0], 0)
        follow = self.client.get(response.url)
        self.assertContains(follow, 'was deleted successfully')

    def test_bulk_delete_removes_account_that_still_has_an_api_token(self):
        url = reverse('admin:account_account_changelist')
        response = self.client.post(url, {
            'action': 'delete_selected',
            '_selected_action': [str(self.user.pk)],
            'post': 'yes',
        })
        self.assertLess(response.status_code, 500, getattr(response, 'content', b'')[:1500])
        self.assertFalse(Account.objects.filter(pk=self.user.pk).exists())
        follow = self.client.get(url)
        self.assertContains(follow, 'Successfully deleted')


class DeferredConstraintFailureTests(TransactionTestCase):
    """An unknown deferred foreign key must not report success."""

    def setUp(self):
        _create_deferred_fk('orphan_account_fk')
        self.admin = Account.objects.create_superuser(
            email='admin-orphan@example.com',
            username='adminorphan',
            password='SuperSecret123!',
        )
        self.client.force_login(self.admin)
        self.user = Account.objects.create_user(
            email='orphan@example.com',
            username='orphanuser',
            password='SuperSecret123!',
        )
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO orphan_account_fk (id, user_id) VALUES (1, %s)',
                [self.user.pk],
            )

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS orphan_account_fk')

    def test_failed_commit_does_not_store_a_success_message(self):
        url = reverse('admin:account_account_delete', args=[self.user.pk])
        response = self.client.post(url, {'post': 'yes'})
        self.assertEqual(response.status_code, 302, getattr(response, 'content', b'')[:800])
        self.assertTrue(Account.objects.filter(pk=self.user.pk).exists())
        follow = self.client.get(response.url)
        self.assertContains(follow, ACCOUNT_DELETE_BLOCKED)
        self.assertNotContains(follow, 'was deleted successfully')
        self.assertNotContains(follow, 'Successfully deleted')

    def test_bulk_delete_reports_the_block_without_claiming_success(self):
        url = reverse('admin:account_account_changelist')
        response = self.client.post(url, {
            'action': 'delete_selected',
            '_selected_action': [str(self.user.pk)],
            'post': 'yes',
        })
        self.assertLess(response.status_code, 500, getattr(response, 'content', b'')[:800])
        self.assertTrue(Account.objects.filter(pk=self.user.pk).exists())
        follow = self.client.get(url)
        self.assertContains(follow, ACCOUNT_DELETE_BLOCKED)
        self.assertNotContains(follow, 'Successfully deleted')
        self.assertNotContains(follow, 'was deleted successfully')


class DropOrphanAuthtokenMigrationTests(TransactionTestCase):
    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS authtoken_token')
            cursor.execute(FORGET_AUTHTOKEN_MIGRATIONS)

    def test_sql_drops_the_table_and_forgets_the_app(self):
        user = Account.objects.create_user(
            email='token-migration@example.com',
            username='tokenmigration',
            password='SuperSecret123!',
        )
        _create_deferred_fk('authtoken_token')
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO authtoken_token (id, user_id) VALUES (1, %s)',
                [user.pk],
            )
            cursor.execute(
                'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)',
                ['authtoken', '0001_initial', timezone.now()],
            )
            cursor.execute(DROP_AUTHTOKEN_TABLE)
            cursor.execute(FORGET_AUTHTOKEN_MIGRATIONS)
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'authtoken_token'"
            )
            self.assertIsNone(cursor.fetchone())
            cursor.execute(
                "SELECT COUNT(*) FROM django_migrations WHERE app = 'authtoken'"
            )
            self.assertEqual(cursor.fetchone()[0], 0)
            # Idempotent: a database that never had the table still migrates.
            cursor.execute(DROP_AUTHTOKEN_TABLE)
            cursor.execute(FORGET_AUTHTOKEN_MIGRATIONS)
