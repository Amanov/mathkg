"""Class pages, search and section pages never send a teacher to an empty page."""

from django.core.cache import cache
from django.test import TestCase

from apps.resources.grade_search import EMPTY_CACHE_KEY, empty_page_urls, pages_for_search
from apps.resources.models import MenuItem, Subtopic, Topic


class EmptyPagesTests(TestCase):
    def setUp(self):
        cache.delete(EMPTY_CACHE_KEY)

    def test_a_placeholder_page_without_a_pack_is_left_out(self):
        # Every menu page now has a pack, so check that no empty page reaches the search.
        empty = empty_page_urls()
        urls = {row['url'] for grade in range(1, 13) for row in pages_for_search(grade, '')}
        self.assertFalse(urls & empty)
        # /graphs-depth-time/ used to say «даярдалууда»; the filling-graphs pack fills it now.
        self.assertNotIn('/graphs-depth-time/', empty)
        # A page a pack fills stays.
        self.assertIn('/subtracting-1-digit/', urls)

    def test_a_database_topic_that_does_not_exist_is_left_out(self):
        self.assertIn('/resources/topic/number/directed-numbers/ordering/', empty_page_urls())


class SectionPageTests(TestCase):
    def test_an_empty_section_lists_its_topics(self):
        topic, _ = Topic.objects.get_or_create(slug='algebra', defaults={'title': 'Алгебра'})
        Subtopic.objects.get_or_create(
            slug='equations-linear', topic=topic, defaults={'title': 'Теңдемелер: сызыктуу'},
        )
        root = MenuItem.objects.create(title='Алгебра')
        section = MenuItem.objects.create(
            title='Теңдемелер: сызыктуу', parent=root,
            url_name='', topic=topic,
            subtopic=Subtopic.objects.filter(slug='equations-linear', topic=topic).first(),
        )
        MenuItem.objects.create(title='Кашаа менен', parent=section, url_name='algebra_intro_definitions')
        response = self.client.get('/resources/topic/algebra/equations-linear/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Бул бөлүмдөгү темалар')
        self.assertContains(response, 'Кашаа менен')
        self.assertNotContains(response, 'материалдар даярдалууда')
