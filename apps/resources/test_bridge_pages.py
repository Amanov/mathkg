"""The ten bridge topic pages and their files.

These routes are additive. They do not insert menu rows, and an existing
topic page keeps the markup it had before the routes existed.
"""

from datetime import timedelta

from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.account.models import Account, SubscriptionRequest
from apps.resources.bridge_pages import BUNDLED_DIR, iter_pages, referenced_filenames
from apps.resources.models import MenuItem, Resource

BRIDGE_URL_NAMES = [
    'san_kuramy',
    'on_kozonoktuu_ramka',
    'bar_model_part_whole',
    'bar_model_comparison',
    'word_problems_bar_model',
    'before_after',
    'bar_to_x',
    'balance_method',
    'algebra_tiles',
    'heuristics',
]


class BridgePageTests(TestCase):
    def test_every_bridge_page_renders_with_files_and_grade(self):
        names = referenced_filenames()
        self.assertGreaterEqual(len(names), 60)
        found = set(Resource.objects.filter(title__in=names, is_active=True).values_list('title', flat=True))
        self.assertEqual(found, set(names))
        for name in names:
            self.assertTrue((BUNDLED_DIR / name).is_file(), name)

        pages = iter_pages()
        self.assertEqual(len(pages), 10)
        for page in pages:
            response = self.client.get(reverse(page['url_name']))
            self.assertEqual(response.status_code, 200, page['slug'])
            html = response.content.decode()
            self.assertIn(page['title'], html)
            self.assertIn('Мугалимге', html)
            self.assertIn('model-switch', html)
            self.assertIn('topic-path', html)
            self.assertIn('Сингапур ыкмасы', html)
            self.assertIn('кл.', html)
            for section in page['sections']:
                for item in section['items']:
                    self.assertIn(item['title'], html)
                    self.assertIsNotNone(finders.find(item['image']), item['image'])
                    self.assertIn('/resources/download/', html)

        san = self.client.get(reverse('san_kuramy')).content.decode()
        self.assertIn('1–2 кл.', san)
        self.assertIn('/on-kozonoktuu-ramka/', san)
        self.assertIn('/integers-adding-1-2-digit/', san)
        self.assertIn('Эки түстүү фигуралар', san)

    def test_bridge_pages_do_not_add_menu_items(self):
        self.assertFalse(MenuItem.objects.filter(url_name__in=BRIDGE_URL_NAMES).exists())

    def test_an_existing_topic_page_has_no_bridge_nav(self):
        response = self.client.get(reverse('to_fractions'))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('Ондуктарды бөлчөккө айландыруу', html)
        self.assertNotIn('topic-path', html)
        self.assertNotIn('Сингапур ыкмасы', html)
        self.assertNotIn('bridge-topic.css', html)

    def test_a_bundled_worksheet_downloads(self):
        user = Account.objects.create_user(
            email='bridge@example.com',
            username='bridge',
            password='SuperSecret123!',
        )
        user.is_active = True
        user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        user.subscription_end = timezone.now().date() + timedelta(days=30)
        user.save(update_fields=['is_active', 'current_plan', 'subscription_end'])
        self.client.login(email='bridge@example.com', password='SuperSecret123!')

        resource = Resource.objects.get(title='san-kuramy-EkiTustuuFiguralar-A4.pdf')
        response = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(response.status_code, 200)
        body = b''.join(response.streaming_content)
        self.assertTrue(body.startswith(b'%PDF'), body[:20])

        deck = Resource.objects.get(title='san-kuramy-MagaKorsotSanKuramy.pptx')
        response = self.client.get(reverse('download_resource', args=[deck.pk]))
        self.assertEqual(response.status_code, 200)
        body = b''.join(response.streaming_content)
        self.assertTrue(body.startswith(b'PK'), body[:8])
