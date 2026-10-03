from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.account.models import Account
from apps.resources.models import NewsPost, Resource


class PagesTests(TestCase):

    def test_news_list_orders_newest_first(self):
        older = NewsPost.objects.create(
            title='Эски жаңылык',
            body='Эски.',
            published_date=date(2026, 9, 16),
        )
        newer = NewsPost.objects.create(
            title='Жаңы жаңылык',
            body='Жаңы.',
            published_date=date(2026, 9, 22),
        )
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])
        self.assertEqual(posts, [newer, older])

    def test_news_post_formatted_date_is_kyrgyz(self):
        post = NewsPost.objects.create(
            title='Тест',
            body='Тест.',
            published_date=date(2026, 9, 22),
        )
        self.assertEqual(post.formatted_date(), '22-сентябрь, 2026-жыл')

    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)


@override_settings(MEDIA_ROOT='/tmp/mathkg-test-media')
class SubtractingOneDigitPageTests(TestCase):
    """/subtracting-1-digit/ uses the same card partial as Төрт амал.

    Files are matched by Resource.title, not by topic. Until a row exists
    the card shows "Not found: <filename>" to a logged-in user.
    """

    SECTIONS = [
        'Даяр иш барактар',
        'Сабак учурундагы иш-чаралар',
        'Мугалим жетектеген иш-чаралар',
        'Көрсөтмө куралдар',
    ]
    CARDS = [
        ('Ылдам эсеп', 'Кемитүү торчосу · 3 деңгээлде', 'kemituu-1orun-yldam-esep.png'),
        ('Катаны тап', None, 'kemituu-1orun-katany-tap.png'),
        ('Чоң санды түз', 'Орун наркы боюнча жуп оюн', 'kemituu-1orun-chong-san.png'),
        ('Тарсия курак', None, 'kemituu-1orun-tarsia-kurak.png'),
        ('Бинго', None, 'kemituu-1orun-bingo.png'),
        ('Катар үч', 'Эки команда · 4 × 4 торчо', 'kemituu-1orun-katar-uch.png'),
        ('Ондук чарчылар', 'Бирдик · ондон бир · жүздөн бир', 'kemituu-1orun-onduk-charchylar.png'),
        ('Орун наркы таблицасы', None, 'kemituu-1orun-orun-narky-tablitsasy.png'),
    ]

    def setUp(self):
        self.user = Account.objects.create_user(
            email='teacher@example.com',
            username='teacher',
            password='SuperSecret123!',
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

    def _page(self, login=False):
        if login:
            self.client.force_login(self.user)
        return self.client.get(reverse('subtracting_1_digit'))

    def test_anonymous_visitor_sees_four_sections_eight_cards_and_register_prompt(self):
        response = self._page()
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('Кемитүү — 1 орундуу сандар', html)
        self.assertNotIn('Бул бөлүм үчүн материалдар даярдалууда.', html)
        for header in self.SECTIONS:
            self.assertIn(header, html)
        self.assertLess(
            html.index(self.SECTIONS[0]),
            html.index(self.SECTIONS[1]),
        )
        self.assertLess(
            html.index(self.SECTIONS[1]),
            html.index(self.SECTIONS[2]),
        )
        self.assertLess(
            html.index(self.SECTIONS[2]),
            html.index(self.SECTIONS[3]),
        )
        for title, subtitle, image in self.CARDS:
            self.assertIn(title, html)
            self.assertIn(f'/static/img/{image}', html)
            self.assertIn(f'alt="{title}"', html)
            if subtitle:
                self.assertIn(subtitle, html)
        self.assertIn('Файлды жүктөп алуу үчүн сайтка катталышыныз керек', html)
        self.assertIn(reverse('register'), html)
        self.assertNotIn('Not found:', html)
        self.assertNotIn('/resources/download/', html)

    def test_logged_in_user_sees_not_found_until_resources_exist(self):
        response = self._page(login=True)
        html = response.content.decode()
        self.assertIn('Not found: kemituu-1orun-yldam-esep.pptx', html)
        self.assertIn('Not found: kemituu-1orun-yldam-esep.xlsx', html)
        self.assertIn('Not found: kemituu-1orun-orun-narky-tablitsasy-kichine.pdf', html)
        self.assertEqual(html.count('Not found:'), 20)
        self.assertNotIn('Файлды жүктөп алуу үчүн сайтка катталышыныз керек', html)

    def test_buttons_use_title_lookup_and_show_variant_labels(self):
        # Stored file name deliberately differs from Title: the page keys
        # on Title, the same way Төрт амал does.
        xlsx_bytes = b'PK\x03\x04dummy-xlsx-bytes'
        xlsx = Resource.objects.create(
            title='kemituu-1orun-yldam-esep.xlsx',
            file=SimpleUploadedFile('stored-name-not-the-title.xlsx', xlsx_bytes),
            category='worksheet',
            learning_goal='fluency',
            activity_type='answer_grid',
            difficulty='medium',
            is_active=True,
        )
        Resource.objects.create(
            title='kemituu-1orun-yldam-esep.pptx',
            file=SimpleUploadedFile('kemituu-1orun-yldam-esep.pptx', b'ppt'),
            category='presentation',
            is_active=True,
        )
        Resource.objects.create(
            title='kemituu-1orun-yldam-esep-A4.pdf',
            file=SimpleUploadedFile('kemituu-1orun-yldam-esep-A4.pdf', b'pdf'),
            category='worksheet',
            is_active=True,
        )
        Resource.objects.create(
            title='kemituu-1orun-katany-tap-A5.pdf',
            file=SimpleUploadedFile('kemituu-1orun-katany-tap-A5.pdf', b'pdf'),
            category='worksheet',
            is_active=False,
        )

        response = self._page(login=True)
        html = response.content.decode()
        download = reverse('download_resource', args=[xlsx.pk])
        self.assertIn(f'href="{download}">EXC</a>', html)
        self.assertIn('>.PDF</a> A4<br>', html)
        self.assertIn('Not found: kemituu-1orun-katany-tap-A5.pdf', html)
        self.assertNotIn('href="' + reverse('download_resource', args=[
            Resource.objects.get(title='kemituu-1orun-katany-tap-A5.pdf').pk
        ]) + '"', html)

        fetched = self.client.get(download)
        self.assertEqual(fetched.status_code, 200)
        disposition = fetched['Content-Disposition']
        self.assertIn('attachment', disposition)
        self.assertIn('.xlsx', disposition)
        self.assertEqual(b''.join(fetched.streaming_content), xlsx_bytes)
        self.assertEqual(
            fetched['Content-Type'].split(';')[0],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_neighbouring_pages_keep_their_own_cards(self):
        self.client.force_login(self.user)
        Resource.objects.create(
            title='4-amal-sandyk-bashkatyrma.pptx',
            file=SimpleUploadedFile('4-amal-sandyk-bashkatyrma.pptx', b'ppt'),
            category='presentation',
        )
        pdf = Resource.objects.create(
            title='4-Amal-katanytapTarsiaA4.pdf',
            file=SimpleUploadedFile('4-Amal-katanytapTarsiaA4.pdf', b'pdf'),
            category='worksheet',
        )

        four = self.client.get(reverse('four_basic_operations'))
        self.assertEqual(four.status_code, 200)
        html = four.content.decode()
        self.assertIn('Төрт амал', html)
        self.assertIn('Not found: 4-amal-sandyk-bashkatyrmaA6.pptx', html)
        self.assertIn(
            f'href="{reverse("download_resource", args=[pdf.pk])}">',
            html,
        )
        self.assertIn('.PDF', html)
        self.assertNotIn('</a> A4', html)
        self.assertNotIn('Ылдам эсеп', html)

        adding = self.client.get(reverse('adding_subtracting_1_digit'))
        self.assertEqual(adding.status_code, 200)
        self.assertIn('Бул бөлүм үчүн материалдар даярдалууда.', adding.content.decode())

        koshuu = self.client.get(reverse('koshuu_1_digit'))
        self.assertEqual(koshuu.status_code, 200)
        self.assertIn('Кошуу — 1 орундуу сандар', koshuu.content.decode())
        self.assertIn('Not found: koshuu-story-launch.pptx', koshuu.content.decode())
