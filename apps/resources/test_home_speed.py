"""The first screen does not carry the whole topic menu."""
from django.test import TestCase
from django.urls import reverse

from apps.resources.models import MenuItem


class HomeMenuWeightTests(TestCase):
    def setUp(self):
        root = MenuItem.objects.create(title='Сандар', order=1)
        child = MenuItem.objects.create(title='Кошуу', parent=root, order=1)
        MenuItem.objects.create(title='Ондуктарды кошуу', parent=child, order=1)

    def test_home_keeps_the_top_row_and_leaves_children_out(self):
        html = self.client.get(reverse('home')).content.decode()
        self.assertIn('Сандар', html)
        self.assertIn('id="siteCategoryMenu"', html)
        self.assertNotIn('Ондуктарды кошуу', html)
        self.assertIn('width="1440"', html)
        self.assertIn('intro.webp', html)
        self.assertIn('loading="lazy"', html)

    def test_menu_fragment_has_the_links_and_can_be_cached(self):
        response = self.client.get(reverse('menu_fragment'))
        html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ондуктарды кошуу', html)
        self.assertIn('Кошуу', html)
        self.assertIn('public', response['Cache-Control'])
        self.assertEqual(response['X-Robots-Tag'], 'noindex')
        self.assertNotIn('sessionid', response.cookies)

    def test_home_html_is_gzipped_when_the_browser_asks(self):
        response = self.client.get(
            reverse('home'),
            HTTP_ACCEPT_ENCODING='gzip',
        )
        self.assertEqual(response['Content-Encoding'], 'gzip')
