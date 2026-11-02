"""Titles, descriptions, canonical URLs, and structured data."""
import json
import re

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.resources.models import MenuItem, SubSubtopic, Subtopic, Topic
from apps.resources.seo import (
    DESCRIPTION_LIMIT,
    HOME_DESCRIPTION,
    HOME_TITLE,
    PAGES,
    topic_document_title,
    topic_meta_description,
)
from apps.resources.test_heading_structure import headings


def _meta(html, name):
    match = re.search(
        rf'<meta name="{name}" content="([^"]*)"',
        html,
    )
    return match.group(1) if match else ''


def _prop(html, name):
    match = re.search(
        rf'<meta property="{name}" content="([^"]*)"',
        html,
    )
    return match.group(1) if match else ''


def _jsonld(html):
    match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
    )
    if not match:
        return None
    return json.loads(match.group(1))


class SeoCopyTests(SimpleTestCase):
    def test_static_pages_have_distinct_titles_and_short_descriptions(self):
        titles = []
        descriptions = []
        for key, (title, description) in PAGES.items():
            self.assertIn('| MathKG', title, key)
            self.assertLessEqual(len(description), DESCRIPTION_LIMIT, key)
            self.assertGreaterEqual(len(description), 70, key)
            titles.append(title)
            descriptions.append(description)
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))
        self.assertLessEqual(len(HOME_DESCRIPTION), DESCRIPTION_LIMIT)
        self.assertGreaterEqual(len(HOME_DESCRIPTION), 80)

    def test_topic_title_keeps_grade_text_as_stored(self):
        title = topic_document_title('Ондуктарды кошуу', '4-класс')
        self.assertEqual(
            title,
            '4-класс — Ондуктарды кошуу: презентация, иш барак, тапшырмалар | MathKG',
        )
        ranged = topic_document_title('Сан курамы', '1–2 кл.')
        self.assertIn('1–2 кл. — Сан курамы:', ranged)
        plain = topic_document_title('Геометрия')
        self.assertTrue(plain.startswith('Геометрия: презентация'))
        description = topic_meta_description('Ондуктарды кошуу', '4-класс')
        self.assertLessEqual(len(description), DESCRIPTION_LIMIT)
        self.assertIn('презентация', description)
        self.assertIn('иш барак', description)


class PageSeoTests(TestCase):
    def test_home_head_and_one_h1(self):
        response = self.client.get(reverse('home'))
        html = response.content.decode()
        self.assertEqual(headings(html)['h1'], [
            'Математика мугалимдери үчүн даяр материалдар',
        ])
        self.assertIn(f'<title>{HOME_TITLE}</title>', html)
        self.assertEqual(_meta(html, 'description'), HOME_DESCRIPTION)
        self.assertIn('lang="ky"', html)
        self.assertIn('<link rel="canonical" href="http://testserver/">', html)
        self.assertEqual(_prop(html, 'og:title'), HOME_TITLE)
        self.assertEqual(_prop(html, 'og:description'), HOME_DESCRIPTION)
        self.assertEqual(_prop(html, 'og:locale'), 'ky_KG')
        self.assertEqual(_prop(html, 'og:url'), 'http://testserver/')
        self.assertTrue(_prop(html, 'og:image').endswith('/static/img/logo.jpg'))
        data = _jsonld(html)
        types = {node['@type'] for node in data['@graph']}
        self.assertEqual(types, {'Organization', 'WebSite'})
        self.assertEqual(data['@graph'][1]['inLanguage'], 'ky')
        self.assertNotIn('Something else here', html)
        self.assertNotIn('Gello somethin', html)
        self.assertIn('loading="lazy"', html)
        self.assertIn('src="/static/img/home/intro.png"', html)
        intro = html.split('img/home/intro.png', 1)[0][-80:]
        self.assertNotIn('loading="lazy"', intro)

        alias = self.client.get('/home/')
        self.assertIn(
            '<link rel="canonical" href="http://testserver/">',
            alias.content.decode(),
        )

    def test_topic_page_uses_grade_and_learning_resource(self):
        response = self.client.get(reverse('koshuu_1_digit'))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertEqual(len(headings(html)['h1']), 1)
        self.assertIn(
            '4-класс — Ондуктарды кошуу (1 ондук орун): '
            'презентация, иш барак, тапшырмалар | MathKG',
            html,
        )
        description = _meta(html, 'description')
        self.assertIn('4-класс', description)
        self.assertIn('иш барак', description)
        self.assertLessEqual(len(description), DESCRIPTION_LIMIT)
        data = _jsonld(html)
        self.assertEqual(data['@type'], 'LearningResource')
        self.assertEqual(data['inLanguage'], 'ky')
        self.assertEqual(data['educationalLevel'], '4-класс')
        self.assertIn('teacher', data['audience']['educationalRole'])

    def test_nested_topic_title_is_unique_and_public_pages_differ(self):
        topic = Topic.objects.create(title='Геометрия', slug='geometry-seo')
        sub = Subtopic.objects.create(title='Бурчтар', slug='angles-seo', topic=topic)
        SubSubtopic.objects.create(subtopic=sub, title='Аралаш', slug='mixed-seo')
        page = self.client.get(reverse(
            'subsubtopic_detail',
            args=['geometry-seo', 'angles-seo', 'mixed-seo'],
        ))
        html = page.content.decode()
        self.assertEqual(headings(html)['h1'], ['Геометрия'])
        self.assertIn(
            'Геометрия: Бурчтар: Аралаш: презентация, иш барак, тапшырмалар | MathKG',
            html,
        )
        self.assertEqual(_jsonld(html)['@type'], 'LearningResource')

        titles = set()
        for url_name in ('about', 'pricing', 'news_list', 'login', 'register', 'search'):
            body = self.client.get(reverse(url_name)).content.decode()
            title = re.search(r'<title>(.*?)</title>', body).group(1)
            self.assertIn('| MathKG', title, url_name)
            self.assertTrue(_meta(body, 'description'), url_name)
            self.assertEqual(_prop(body, 'og:locale'), 'ky_KG', url_name)
            self.assertIsNone(_jsonld(body))
            titles.add(title)
        self.assertEqual(len(titles), 6)

    def test_menu_markup_is_not_padded_with_blank_lines(self):
        parent = MenuItem.objects.create(title='Сандар', order=1)
        MenuItem.objects.create(
            title='Төрт амал', parent=parent, order=1, url_name='four_basic_operations',
        )
        html = self.client.get(reverse('home')).content.decode()
        nav = html.split('category-navbar', 1)[1].split('</nav>', 1)[0]
        self.assertIn('Төрт амал', nav)
        self.assertIn(
            '<li class="nav-item dropdown"><a href="#" class="mymenu dropdown-toggle"',
            nav,
        )
        self.assertIn('menu-grade">1–5 кл.</span>', nav)
