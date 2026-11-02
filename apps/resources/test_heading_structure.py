"""Each public page has one h1. Home keeps the hero title and section headings."""
from html.parser import HTMLParser

from django.test import TestCase
from django.urls import reverse

from apps.resources.models import Subtopic, Topic


class _HeadingCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.by_tag = {'h1': [], 'h2': [], 'h3': []}
        self._tag = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag in self.by_tag and self._tag is None:
            self._tag = tag
            self._buf = []

    def handle_endtag(self, tag):
        if tag == self._tag:
            self.by_tag[tag].append(' '.join(''.join(self._buf).split()))
            self._tag = None

    def handle_data(self, data):
        if self._tag:
            self._buf.append(data)


def headings(html):
    parser = _HeadingCollector()
    parser.feed(html)
    return parser.by_tag


class SingleH1Tests(TestCase):
    def test_home_and_a_topic_page_have_exactly_one_h1(self):
        home = self.client.get(reverse('home'))
        self.assertEqual(home.status_code, 200)
        home_html = home.content.decode()
        home_headings = headings(home_html)

        self.assertEqual(
            home_headings['h1'],
            ['Математика мугалимдери үчүн даяр материалдар'],
        )
        self.assertIn(
            '<p class="hero-line">Мугалимдер үчүн заманбап математикалык ресурстар</p>',
            home_html,
        )
        for title in ('Презентациялар', 'Экзамен суроолору', 'Математика боюнча иш барактар'):
            self.assertIn(title, home_headings['h2'])
        self.assertNotIn('Жүз уккандан бир көргөн артык.', home_headings['h2'] + home_headings['h3'])
        self.assertNotIn('Кеңешип кескен бармак оорубайт', home_headings['h2'] + home_headings['h3'])
        self.assertIn('>Жүз уккандан бир көргөн артык.</p>', home_html)
        self.assertIn('>Кеңешип кескен бармак оорубайт</p>', home_html)
        self.assertTrue(all(text for text in home_headings['h2']))
        self.assertTrue(all(text for text in home_headings['h3']))
        self.assertNotIn('<h1', home_html.split('Математика мугалимдери үчүн даяр материалдар', 1)[1])
        self.assertIn('<a class="navbar-brand-mathkgz"', home_html)

        topic = Topic.objects.create(title='Геометрия', slug='geometry-headings')
        Subtopic.objects.create(title='Бурчтар', slug='angles-headings', topic=topic)
        page = self.client.get(
            reverse('subtopic_detail', args=['geometry-headings', 'angles-headings'])
        )
        self.assertEqual(page.status_code, 200)
        page_html = page.content.decode()
        page_headings = headings(page_html)
        self.assertEqual(page_headings['h1'], ['Геометрия'])
        self.assertIn('Бурчтар', page_headings['h2'])

        for url_name in (
            'about',
            'pricing',
            'news_list',
            'topics_tree',
            'resources',
            'search',
            'login',
            'register',
            'password_reset',
            'password_reset_complete',
        ):
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, url_name)
            found = headings(response.content.decode())['h1']
            self.assertEqual(len(found), 1, f'{url_name}: {found}')
