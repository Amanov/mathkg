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
            if page['slug'] == 'bar-to-x':
                self.assertNotIn('topic-path', html)
                self.assertIn('mk-zoom.css', html)
                self.assertIn('mk-zoom.js', html)
                self.assertIn('class="mk-zoom"', html)
                self.assertIn('Тилкеден x ке: түшүндүрмө', html)
            else:
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

    def test_bar_to_x_keeps_the_footer_link_and_the_lesson_deck(self):
        algebra = MenuItem.objects.create(title='Алгебра', order=0)
        intro = MenuItem.objects.create(title='Киришүү', parent=algebra, order=0)
        MenuItem.objects.create(title='Тилкеден x ке', parent=intro, order=0, url_name='bar_to_x')
        MenuItem.objects.create(
            title='Аныктамалар', parent=intro, order=1, url_name='algebra_intro_definitions',
        )
        html = self.client.get(reverse('bar_to_x')).content.decode()
        self.assertNotIn('topic-path', html)
        self.assertLess(
            html.index('Тилкеден x ке: түшүндүрмө'),
            html.index('Арифметикадан алгебрага'),
        )
        self.assertIn('related-topics', html)
        self.assertIn('Кийинки тема', html)
        self.assertIn('Аныктамалар', html)
        self.assertNotIn('Мурунку тема', html)

        other = self.client.get(reverse('balance_method')).content.decode()
        self.assertIn('topic-path', other)

        import importlib
        import zipfile
        import re
        from django.db import migrations as dj_migrations

        migration = importlib.import_module('apps.resources.migrations.0052_bar_to_x_lesson')
        self.assertEqual(
            migration.Migration.dependencies,
            [('personal', '0050_refresh_kyrgyz_text')],
        )
        self.assertEqual(len(migration.Migration.operations), 1)
        operation = migration.Migration.operations[0]
        self.assertIsInstance(operation, dj_migrations.RunPython)
        self.assertIs(operation.code, migration.forward)

        resource = Resource.objects.get(title='bar-to-x-sabak.pptx')
        self.assertEqual(resource.category, 'presentation')
        self.assertTrue(resource.is_active)
        from apps.resources.models import PageFreeDownload
        free = PageFreeDownload.objects.get(page_key='bar_to_x')
        locked = Resource.objects.filter(
            title__in=[
                'bar-to-x-sabak.pptx',
                'bar-to-x-ArifmetikadanAlgebraga.pptx',
            ],
        ).exclude(pk=free.resource_id).first()
        self.assertIsNotNone(locked)
        response = self.client.get(reverse('download_resource', args=[locked.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

        user = Account.objects.create_user(
            email='barto@example.com',
            username='barto',
            password='SuperSecret123!',
        )
        user.is_active = True
        user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        user.subscription_end = timezone.now().date() + timedelta(days=30)
        user.save(update_fields=['is_active', 'current_plan', 'subscription_end'])
        self.client.login(email='barto@example.com', password='SuperSecret123!')
        response = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(response.status_code, 200)
        body = b''.join(response.streaming_content)
        self.assertTrue(body.startswith(b'PK'), body[:8])

        archive = zipfile.ZipFile(BUNDLED_DIR / 'bar-to-x-sabak.pptx')
        texts = []
        italic = 0
        for name in archive.namelist():
            if not re.match(r'ppt/slides/slide\d+\.xml$', name):
                continue
            xml = archive.read(name).decode('utf-8')
            texts.extend(re.findall(r'<a:t[^>]*>([^<]*)</a:t>', xml))
            italic += xml.count('i="1"')
        blob = '\n'.join(texts)
        self.assertIn('MathKG · Математика кыргызча', blob)
        self.assertIn('mathematicskgz@gmail.com', blob)
        self.assertIn('Окуучу', blob)
        self.assertIn('70 000', blob)
        self.assertIn('1,5', blob)
        self.assertIn('Жеңил', blob)
        self.assertIn('Орто', blob)
        self.assertIn('Оор', blob)
        self.assertIn('Аныктамалар', blob)
        self.assertGreater(italic, 0)
        for foreign in ('және', 'үшін', 'оқушы', 'студент', 'теңдеу', 'мұғалім', 'жеңіл'):
            self.assertNotIn(foreign, blob)
