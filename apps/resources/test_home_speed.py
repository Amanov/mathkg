"""The first screen does not carry the whole topic menu."""
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from PIL import Image, ImageChops

from apps.resources.models import MenuItem

HOME_ILLUSTRATIONS = (
    'intro',
    'presentations',
    'worksheets',
    'activities',
    'teacher-led',
    'exam',
    'revision',
)


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
        self.assertIn('width="1068"', html)
        self.assertIn('height="851"', html)
        self.assertIn('intro.webp', html)
        self.assertIn('loading="lazy"', html)

    def test_home_illustrations_fill_their_frame(self):
        html = self.client.get(reverse('home')).content.decode()
        folder = settings.BASE_DIR / 'static' / 'img' / 'home'
        for name in HOME_ILLUSTRATIONS:
            png = Image.open(folder / f'{name}.png').convert('RGB')
            webp = Image.open(folder / f'{name}.webp')
            self.assertEqual(webp.size, png.size)
            self.assertIn(f'img/home/{name}.webp', html)
            self.assertIn(f'width="{png.width}"', html)
            self.assertIn(f'height="{png.height}"', html)
            diff = ImageChops.difference(
                png, Image.new('RGB', png.size, (255, 255, 255))
            ).convert('L')
            mask = diff.point(lambda p: 255 if p > 8 else 0)
            self.assertEqual(mask.getbbox(), (0, 0, png.width, png.height))

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
