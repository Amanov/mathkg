"""Searching a class returns the topic pages already tagged with that class."""

from django.core.cache import cache
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.resources.grade_search import (
    catalog,
    grades_from_label,
    pages_for_search,
    parse_grade_query,
)
from apps.resources.models import SearchQuery


class ParseGradeQueryTests(SimpleTestCase):
    def test_the_forms_teachers_type(self):
        forms = (
            '7-класс',
            '7 класс',
            '7класс',
            '7-кл',
            '7-кл.',
            'класс 7',
            'класс-7',
            'Класс 7',
            '7-grade',
            '7 grade',
            'grade 7',
            'Grade-7',
        )
        for text in forms:
            grade, remainder = parse_grade_query(text)
            self.assertEqual(grade, 7, text)
            self.assertEqual(remainder, '', text)

    def test_a_class_plus_words_keeps_the_words(self):
        self.assertEqual(parse_grade_query('7-класс тараза'), (7, 'тараза'))
        self.assertEqual(parse_grade_query('тараза 7-класс'), (7, 'тараза'))

    def test_a_bare_number_or_a_topic_is_not_a_class(self):
        self.assertEqual(parse_grade_query('7'), (None, '7'))
        self.assertEqual(parse_grade_query('алгебра'), (None, 'алгебра'))
        self.assertEqual(parse_grade_query('класс'), (None, 'класс'))

    def test_a_label_span_includes_every_class_inside_it(self):
        self.assertEqual(grades_from_label('7 кл.'), frozenset({7}))
        self.assertEqual(grades_from_label('7-класс'), frozenset({7}))
        self.assertEqual(grades_from_label('6–7 кл.'), frozenset({6, 7}))
        self.assertEqual(grades_from_label('7–9'), frozenset({7, 8, 9}))
        self.assertEqual(grades_from_label('1–5 кл.'), frozenset({1, 2, 3, 4, 5}))


class GradeCatalogTests(TestCase):
    def test_most_topic_pages_already_have_a_grade(self):
        pages = catalog()
        self.assertGreater(len(pages), 500)
        grade_7 = [page for page in pages if 7 in page['grades']]
        self.assertGreater(len(grade_7), 100)
        sections = {page['breadcrumb'][0] for page in grade_7}
        for name in ('Сандар', 'Пропорция', 'Алгебра', 'Геометрия', 'Дата'):
            self.assertIn(name, sections)

    def test_the_page_badge_wins_over_a_different_continuum_band(self):
        # /koshuu-1-digit/ renders the badge «4-класс». The continuum row
        # says 6 кл. and the menu audit says 5. Search follows the badge.
        urls = {page['url'] for page in pages_for_search(4, '')}
        self.assertIn('/koshuu-1-digit/', urls)
        self.assertNotIn('/koshuu-1-digit/', {page['url'] for page in pages_for_search(6, '')})
        self.assertNotIn('/koshuu-1-digit/', {page['url'] for page in pages_for_search(7, '')})

        # A pack page shows the pack span, not the continuum band.
        grade_4 = {page['url'] for page in pages_for_search(4, '')}
        grade_6 = {page['url'] for page in pages_for_search(6, '')}
        self.assertIn('/subtracting-1-digit/', grade_4)
        self.assertNotIn('/subtracting-1-digit/', grade_6)


class GradeSearchViewTests(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def _urls(self, response):
        found = {}
        for section, rows in response.context['grouped_topic_results']:
            found[section] = [row['url'] for row in rows]
        return found

    def test_searching_a_class_returns_that_grades_topics_by_section(self):
        response = self.client.get(reverse('search'), {'q': '7-класс'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['has_results'])
        self.assertContains(response, 'Эч нерсе табылган жок', count=0)
        groups = self._urls(response)
        self.assertIn('/compound-pressure-force-area/', groups['Сандар'])
        self.assertIn('/balance-method/', groups['Алгебра'])
        self.assertIn('/algebra-tiles/', groups['Алгебра'])
        self.assertIn('/statistika-ortocho/', groups['Дата'])
        self.assertNotIn('/koshuu-1-digit/', [url for rows in groups.values() for url in rows])
        self.assertContains(response, 'search-grade-chip is-active')
        self.assertContains(response, '7-класс')
        self.assertContains(response, '8-класс')
        logged = SearchQuery.objects.get()
        self.assertEqual(logged.query, '7-класс')
        self.assertGreater(logged.results_count, 0)

    def test_every_requested_spelling_finds_the_same_grade_7_page(self):
        forms = ('7 класс', '7класс', '7-кл', 'класс 7', '7-grade', 'grade 7')
        for text in forms:
            cache.clear()
            response = self.client.get(reverse('search'), {'q': text})
            groups = self._urls(response)
            self.assertIn(
                '/balance-method/',
                groups.get('Алгебра', []),
                text,
            )

    def test_a_span_matches_each_class_it_covers(self):
        grade_7 = self._urls(self.client.get(reverse('search'), {'q': '7-класс'}))
        cache.clear()
        grade_8 = self._urls(self.client.get(reverse('search'), {'q': '8-класс'}))
        cache.clear()
        grade_6 = self._urls(self.client.get(reverse('search'), {'q': '6-класс'}))
        self.assertIn('/algebra-tiles/', grade_7['Алгебра'])
        self.assertIn('/algebra-tiles/', grade_8['Алгебра'])
        self.assertNotIn('/algebra-tiles/', grade_6.get('Алгебра', []))

    def test_words_after_the_class_narrow_the_topics(self):
        response = self.client.get(reverse('search'), {'q': '7-класс Тараза'})
        groups = self._urls(response)
        self.assertEqual(groups['Алгебра'], ['/balance-method/'])
        self.assertNotIn('Сандар', groups)

    def test_a_chip_switches_class_and_the_placeholder_names_class(self):
        response = self.client.get(reverse('search'), {'q': '7-класс'})
        clear = response.context['grade_clear_href']
        chip_8 = next(chip for chip in response.context['grade_chips'] if chip['num'] == 8)
        switched = self.client.get(chip_8['href'])
        self.assertEqual(switched.context['active_grade'], 8)
        self.assertNotIn(
            '/recurring-decimals-ordering/',
            [url for rows in self._urls(switched).values() for url in rows],
        )
        self.assertIn('/algebra-tiles/', self._urls(switched)['Алгебра'])
        self.assertIn('search', clear)

        page = self.client.get(reverse('search'))
        self.assertContains(page, 'placeholder="Издөө: класс"')

    def test_suggest_offers_grade_topics_instead_of_an_empty_list(self):
        response = self.client.get(reverse('search_suggest'), {'q': '7-класс'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['results'])
        urls = [row['url'] for row in payload['results']]
        sections = {row['breadcrumb'][0] for row in payload['results'] if row['breadcrumb']}
        self.assertGreater(len(sections), 1)
        self.assertTrue(any(row.get('grade') for row in payload['results']))
        self.assertLessEqual(len(urls), 8)
        self.assertEqual(SearchQuery.objects.count(), 0)
