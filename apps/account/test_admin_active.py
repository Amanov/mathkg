from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

Account = get_user_model()


class AccountAdminActiveColumnTests(TestCase):
    def setUp(self):
        self.admin = Account.objects.create_superuser(
            email='admin-active@example.com',
            username='adminactive',
            password='SuperSecret123!',
        )
        self.client.force_login(self.admin)
        self.pending = Account.objects.create_user(
            email='pending-active@example.com',
            username='pendingactive',
            password='SuperSecret123!',
        )
        self.pending.is_active = False
        self.pending.save(update_fields=['is_active'])
        self.live = Account.objects.create_user(
            email='live-active@example.com',
            username='liveactive',
            password='SuperSecret123!',
        )
        self.live.is_active = True
        self.live.save(update_fields=['is_active'])

    def test_changelist_shows_active_column_and_kyrgyz_filter(self):
        url = reverse('admin:account_account_changelist')
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Активдүү')
        self.assertContains(page, 'Активдүү эмес')
        self.assertContains(page, 'Тандалгандарды активдештирүү')

        inactive = self.client.get(url, {'is_active': 'no'})
        self.assertContains(inactive, 'pending-active@example.com')
        self.assertNotContains(inactive, 'live-active@example.com')

        active = self.client.get(url, {'is_active': 'yes'})
        self.assertContains(active, 'live-active@example.com')
        self.assertNotContains(active, 'pending-active@example.com')

    def test_bulk_action_activates_selected_accounts(self):
        url = reverse('admin:account_account_changelist')
        response = self.client.post(url, {
            'action': 'activate_selected_accounts',
            '_selected_action': [str(self.pending.pk)],
        })
        self.assertEqual(response.status_code, 302)
        self.pending.refresh_from_db()
        self.assertTrue(self.pending.is_active)
        self.live.refresh_from_db()
        self.assertTrue(self.live.is_active)
