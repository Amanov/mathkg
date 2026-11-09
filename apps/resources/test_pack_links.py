"""Pack page copies, linked path, class links (data/pack_links.py)."""

from django.test import TestCase
from django.urls import resolve

from apps.resources.data import pack_links
from apps.resources.data.pack_pages import GROUPS, SLUG_PAGES, page_for


class PackLinkTests(TestCase):
    def test_every_main_page_resolves_and_shows_its_own_group(self):
        for group in GROUPS:
            key = group['spec']['page_key']
            main = pack_links.main_path(key)
            match = resolve(main)
            self.assertNotIn('redirect', match.func.__name__.lower(), main)
            if group['slugs']:
                self.assertEqual(SLUG_PAGES[main.strip('/')]['page_key'], key, main)

    def test_copy_names_the_main_page_as_canonical(self):
        main = self.client.get('/time-reading-clocks/').content.decode()
        copy = self.client.get('/time-calculations/').content.decode()
        canonical = '<link rel="canonical" href="https://mathkg.com/time-reading-clocks/">'
        self.assertIn(canonical, main)
        self.assertIn(canonical, copy)
        self.assertIn('/time-calculations/', pack_links.duplicate_paths())
        self.assertNotIn('/time-reading-clocks/', pack_links.duplicate_paths())

    def test_linked_path_and_breadcrumb_jsonld(self):
        html = self.client.get('/time-calculations/').content.decode()
        grade = page_for('time-calculations', '')['grade_number']
        self.assertIn(f'<a href="/{grade}-klass/">{grade}-класс</a>', html)
        self.assertIn('<a href="/time-reading-clocks/">Убакыт</a>', html)
        start = html.index('"BreadcrumbList"')
        self.assertIn('"position":4', html[start:start + 2000])

    def test_same_class_topics_link_other_packs_of_the_class(self):
        spec = page_for('time-calculations', 'Убакыт')
        urls = [topic['url'] for topic in spec['grade_topics']]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertNotIn('/time-reading-clocks/', urls)
        self.assertTrue(urls)
        html = self.client.get('/time-calculations/').content.decode()
        self.assertIn(f"{spec['grade_number']}-класстын башка темалары", html)

    def test_every_bank_theme_has_a_topic_page(self):
        from apps.resources.question_bank import bank_themes
        missing = [t['slug'] for t in bank_themes() if not pack_links.theme_url(t['slug'])]
        self.assertEqual(missing, [])

    def test_home_links_every_class_page(self):
        html = self.client.get('/').content.decode()
        self.assertIn('class="home-grades"', html)
        self.assertIn('href="/11-klass/"', html)
