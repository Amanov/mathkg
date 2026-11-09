"""Class pages (/1-klass/ ... /11-klass/), the footer row, and the sitemap."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.resources.models import Resource, Topic

SITEMAP_HOST = {'HTTP_HOST': 'mathkg.com', 'secure': True}


class GradePageTests(TestCase):
    def test_a_class_page_lists_its_topics_by_section(self):
        response = self.client.get('/4-klass/')
        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        self.assertIn('4-класс математика: презентациялар жана иш барактар', page)
        self.assertIn('/multiplying-dividing-10-100-1000/', page)
        self.assertIn('search-category-heading">Сандар<', page)
        self.assertIn('href="/5-klass/"', page)
        self.assertIn('aria-current="page"', page)

    def test_the_head_is_kyrgyz_with_russian_only_in_hidden_words(self):
        page = self.client.get('/7-klass/').content.decode()
        self.assertIn(
            '<title>7-класс математика: презентация, иш барак, тапшырмалар | MathKG</title>',
            page,
        )
        self.assertIn('математика 7 класс, презентация 7 класс, рабочие листы 7 класс', page)
        self.assertIn('/7-klass/"', page)
        self.assertIn('"alternateName":"Математика 7 класс"', page)
        self.assertIn('"educationalLevel":"7-класс"', page)

    def test_unknown_classes_are_not_found(self):
        for path in ('/0-klass/', '/12-klass/', '/99-klass/'):
            self.assertEqual(self.client.get(path).status_code, 404, path)

    def test_the_footer_links_every_class(self):
        page = self.client.get('/about/').content.decode()
        self.assertIn('Класстар:', page)
        for number in range(1, 12):
            self.assertIn(f'href="/{number}-klass/"', page)

    def test_the_footer_contacts_are_links(self):
        page = self.client.get('/about/').content.decode()
        self.assertIn('href="mailto:mathematicskgz@gmail.com"', page)
        self.assertIn('class="footer-contact-item" href="https://mathkg.com/"', page)


class SitemapTests(TestCase):
    def test_class_pages_are_listed_and_home_is_not(self):
        body = self.client.get('/sitemap.xml', **SITEMAP_HOST).content.decode()
        self.assertIn('https://mathkg.com/1-klass/', body)
        self.assertIn('https://mathkg.com/11-klass/', body)
        self.assertNotIn('https://mathkg.com/12-klass/', body)
        self.assertNotIn('https://mathkg.com/home/', body)
        self.assertIn('<loc>https://mathkg.com/</loc>', body)

    def test_a_topic_with_a_file_gets_lastmod(self):
        topic = Topic.objects.create(title='Сынак тема', slug='synak-tema')
        Resource.objects.create(
            title='Иш барак', category='worksheet', is_active=True, topic=topic,
            file=SimpleUploadedFile('ish-barak.pdf', b'%PDF-1.4'),
        )
        body = self.client.get('/sitemap.xml', **SITEMAP_HOST).content.decode()
        start = body.index('/resources/topic/synak-tema/</loc>')
        entry = body[start:body.index('</url>', start)]
        self.assertIn('<lastmod>', entry)

    def test_a_topic_without_files_has_no_lastmod(self):
        Topic.objects.create(title='Бош тема', slug='bosh-tema')
        body = self.client.get('/sitemap.xml', **SITEMAP_HOST).content.decode()
        start = body.index('/resources/topic/bosh-tema/</loc>')
        entry = body[start:body.index('</url>', start)]
        self.assertNotIn('<lastmod>', entry)
