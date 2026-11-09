from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.resources import ip_info
from apps.resources.models import (
    ButtonClick, LoginEvent, Resource, ResourceDownload, SearchQuery, SiteVisit,
)


class IpInfoTests(TestCase):
    def test_country_of_a_kyrgyz_address(self):
        self.assertEqual(ip_info.country('212.112.100.1'), ('KG', 'Кыргызстан'))
        self.assertEqual(ip_info.country_label('212.112.100.1'), 'KG · Кыргызстан')

    def test_unknown_addresses_show_a_dash(self):
        for ip in (None, '', '127.0.0.1', '10.1.2.3', 'not-an-ip'):
            self.assertEqual(ip_info.country_label(ip), '-')

    def test_robots_by_address_and_by_user_agent(self):
        self.assertTrue(ip_info.is_robot('66.249.66.100'))
        self.assertTrue(ip_info.is_robot('1.2.3.4', 'Mozilla/5.0 (compatible; Googlebot/2.1)'))
        self.assertTrue(ip_info.is_robot('1.2.3.4', 'python-requests/2.32'))
        self.assertFalse(ip_info.is_robot('212.112.100.1', 'Mozilla/5.0 (Windows NT 10.0) Chrome/130'))
        self.assertFalse(ip_info.is_robot(None, ''))


class AdminCountryColumnTests(TestCase):
    def setUp(self):
        admin = get_user_model().objects.create_superuser(
            email='admin@example.com', username='admin', password='Pass-12345',
        )
        self.client.force_login(admin)
        resource = Resource.objects.create(
            title='Иш барак', category='worksheet', is_active=True,
            file=SimpleUploadedFile('ish-barak.pdf', b'%PDF-1.4'),
        )
        self.human = ResourceDownload.objects.create(
            resource=resource, ip_address='212.112.100.1',
            user_agent='Mozilla/5.0 (Windows NT 10.0) Chrome/130',
        )
        self.robot = ResourceDownload.objects.create(
            resource=resource, ip_address='66.249.66.100',
            user_agent='Mozilla/5.0 (compatible; Googlebot/2.1)',
        )

    def _changelist(self, model, query=''):
        url = reverse(f'admin:personal_{model}_changelist') + query
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    def test_downloads_show_country_and_who(self):
        page = self._changelist('resourcedownload')
        self.assertIn('KG · Кыргызстан', page)
        self.assertIn('US · АКШ', page)
        self.assertIn('Робот', page)
        self.assertIn('Адам (каттоосуз)', page)

    def test_downloads_can_hide_robots(self):
        humans = self._changelist('resourcedownload', '?kind=human')
        self.assertIn('212.112.100.1', humans)
        self.assertNotIn('66.249.66.100', humans)
        robots = self._changelist('resourcedownload', '?kind=robot')
        self.assertIn('66.249.66.100', robots)
        self.assertNotIn('212.112.100.1', robots)

    def test_other_logs_show_the_country(self):
        SiteVisit.objects.create(path='/', ip_address='212.112.100.1')
        self.assertIn('KG · Кыргызстан', self._changelist('sitevisit'))
        for model in (ButtonClick, SearchQuery, LoginEvent):
            self.assertIn('country', site._registry[model].list_display)
