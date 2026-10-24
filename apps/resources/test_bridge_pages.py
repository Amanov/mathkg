"""The ten bridge topic pages, their files, and the learning-path nav."""

from datetime import timedelta
from pathlib import Path

from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.account.models import Account, SubscriptionRequest
from apps.resources.bridge_pages import BUNDLED_DIR, iter_pages, referenced_filenames
from apps.resources.bridge_menu import apply_bridge_menu
from apps.resources.models import MenuItem, Resource, TopicContinuum


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
            row = TopicContinuum.objects.get(href=f"/{page['slug']}/")
            self.assertIn(row.grade_band, html)
            self.assertTrue(row.grade_band.endswith('кл.'))
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

    def test_menu_insert_is_idempotent_and_keeps_existing_items(self):
        before = MenuItem.objects.count()
        apply_bridge_menu(MenuItem)
        self.assertEqual(MenuItem.objects.count(), before)
        self.assertTrue(MenuItem.objects.filter(
            url_name='san_kuramy', parent__title='Сан сезими',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='on_kozonoktuu_ramka', parent__title='Сан сезими',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='bar_model_part_whole', parent__title='Тилке модели',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='word_problems_bar_model', parent__title='Турмуштук маселелер',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='before_after',
            parent__title='Өзгөртүп түзүү',
            parent__parent__title='Катыш',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='bar_to_x',
            parent__title='Киришүү',
            parent__parent__title='Алгебра',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='balance_method',
            parent__title='Теңдемелер: сызыктуу',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='algebra_tiles',
            parent__title='Өзгөртүп түзүү',
            parent__parent__title='Алгебра',
        ).exists())
        self.assertTrue(MenuItem.objects.filter(
            url_name='heuristics', parent__isnull=True,
        ).exists())

    def test_existing_topic_page_still_renders(self):
        response = self.client.get(reverse('to_fractions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ондуктарды бөлчөккө айландыруу')
