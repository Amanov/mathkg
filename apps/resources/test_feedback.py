"""Page faces, the written feedback form, and published teacher notes."""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from apps.resources.management.commands.seed_launch_news import NEWS_ITEMS
from apps.resources.models import (
    PageReaction,
    PageReactionCount,
    Subtopic,
    Topic,
    WrittenFeedback,
)
from apps.resources.test_heading_structure import headings

Account = get_user_model()


def _note(**kwargs):
    data = {
        'kind': WrittenFeedback.KIND_PRAISE,
        'message': 'Сабакка жакшы материал',
        'name': 'Айгерим',
        'email': 'secret@example.com',
        'about_page': '/about/',
    }
    data.update(kwargs)
    return WrittenFeedback.objects.create(**data)


class PageReactionTests(TestCase):
    def test_a_face_is_counted_once_for_the_same_visitor_and_page(self):
        url = reverse('page_reaction')
        first = self.client.post(url, {'path': '/', 'face': 'happy'})
        self.assertEqual(first.status_code, 302)
        self.assertEqual(PageReaction.objects.filter(path='/', face='happy').count(), 1)
        self.assertEqual(PageReactionCount.objects.get(path='/').happy_count, 1)

        second = self.client.post(url, {'path': '/', 'face': 'sad'})
        self.assertEqual(second.status_code, 302)
        self.assertEqual(PageReaction.objects.count(), 1)
        self.assertEqual(PageReactionCount.objects.get(path='/').happy_count, 1)
        self.assertEqual(PageReactionCount.objects.get(path='/').sad_count, 0)

        home = self.client.get('/')
        self.assertContains(home, 'Рахмат!')
        self.assertNotContains(home, 'name="face"')

        other = Client()
        other.post(url, {'path': '/', 'face': 'sad'})
        self.assertEqual(PageReaction.objects.count(), 2)
        self.assertEqual(PageReactionCount.objects.get(path='/').sad_count, 1)

        PageReaction.objects.filter(face='sad').delete()
        self.assertEqual(PageReactionCount.objects.get(path='/').sad_count, 0)
        self.assertEqual(PageReactionCount.objects.get(path='/').happy_count, 1)

    def test_post_without_csrf_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        home = client.get('/')
        self.assertContains(home, 'csrfmiddlewaretoken')
        denied = client.post(reverse('page_reaction'), {'path': '/', 'face': 'happy'})
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(PageReaction.objects.count(), 0)

        token = home.cookies['csrftoken'].value
        allowed = client.post(reverse('page_reaction'), {
            'path': '/',
            'face': 'happy',
            'csrfmiddlewaretoken': token,
        })
        self.assertEqual(allowed.status_code, 302)
        self.assertEqual(PageReaction.objects.filter(path='/').count(), 1)

    def test_a_topic_page_stores_its_material(self):
        topic = Topic.objects.create(title='Геометрия', slug='geometry-fb')
        subtopic = Subtopic.objects.create(title='Бурчтар', slug='angles-fb', topic=topic)
        path = reverse('subtopic_detail', args=['geometry-fb', 'angles-fb'])

        self.client.post(reverse('page_reaction'), {'path': path, 'face': 'ok'})

        row = PageReaction.objects.get()
        self.assertEqual(row.path, path)
        self.assertEqual(row.material, 'Бурчтар')
        self.assertEqual(row.topic, topic)
        self.assertEqual(row.subtopic, subtopic)
        self.assertEqual(PageReactionCount.objects.get(path=path).ok_count, 1)

        lesson = reverse('four_basic_operations')
        self.client.post(reverse('page_reaction'), {'path': lesson, 'face': 'sad'})
        lesson_row = PageReaction.objects.get(path=lesson)
        self.assertEqual(lesson_row.material, 'Төрт амал')

    def test_the_row_is_on_every_base_page_and_the_link_is_only_in_the_footer(self):
        html = self.client.get(reverse('home')).content.decode()
        before_footer, footer = html.split('<footer', 1)
        self.assertIn('Бул бет сизге жактыбы?', before_footer)
        self.assertIn('>Жакты<', before_footer)
        self.assertIn('>Жаман эмес<', before_footer)
        self.assertIn('>Жаккан жок<', before_footer)
        self.assertNotIn('<textarea', before_footer.split('class="page-reaction"', 1)[1])
        self.assertNotIn('Пикир калтыруу', before_footer)
        self.assertNotIn('/pikir/', before_footer)
        self.assertIn('Пикир калтыруу', footer)
        self.assertIn(reverse('feedback'), footer)
        self.assertIn(reverse('teacher_comments'), footer)
        self.assertIn('page-reaction.js', html)
        self.assertNotIn('Ондуктарды кошуу', html)

        for name in ('about', 'news_list', 'topics_tree', 'pricing'):
            page = self.client.get(reverse(name))
            self.assertContains(page, 'Бул бет сизге жактыбы?')


class WrittenFeedbackTests(TestCase):
    def setUp(self):
        cache.clear()

    def _post(self, client=None, **extra):
        client = client or self.client
        data = {
            'kind': 'sunush',
            'message': 'Издөө тез болсо жакшы',
            'name': 'Нурзат',
            'email': 'nurzat@example.com',
            'about_page': '/search/',
            'mk_hp': '',
        }
        data.update(extra)
        return client.post(reverse('feedback'), data)

    def test_the_form_saves_and_the_page_has_one_h1(self):
        page = self.client.get(reverse('feedback'))
        self.assertEqual(page.status_code, 200)
        html = page.content.decode()
        self.assertEqual(headings(html)['h1'], ['Пикир калтыруу'])
        self.assertIn('Сунуш', html)
        self.assertIn('Мактоо', html)

        response = self._post()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(headings(response.content.decode())['h1'], ['Пикир калтыруу'])
        self.assertContains(response, 'Рахмат! Билдирүүңүз кабыл алынды.')

        saved = WrittenFeedback.objects.get()
        self.assertEqual(saved.kind, WrittenFeedback.KIND_SUGGESTION)
        self.assertEqual(saved.message, 'Издөө тез болсо жакшы')
        self.assertEqual(saved.name, 'Нурзат')
        self.assertEqual(saved.email, 'nurzat@example.com')
        self.assertEqual(saved.about_page, '/search/')
        self.assertFalse(saved.is_read)
        self.assertFalse(saved.show_on_site)

    def test_a_honeypot_post_is_not_saved(self):
        response = self._post(mk_hp='http://spam.example')
        self.assertContains(response, 'Рахмат! Билдирүүңүз кабыл алынды.')
        self.assertEqual(WrittenFeedback.objects.count(), 0)
        self.assertEqual(headings(response.content.decode())['h1'], ['Пикир калтыруу'])

    def test_the_rate_limit_stops_a_burst(self):
        for n in range(5):
            self._post(message=f'Билдирүү {n} жазылды')
        self.assertEqual(WrittenFeedback.objects.count(), 5)
        blocked = self._post(message='Бул алтынчы билдирүү')
        self.assertEqual(WrittenFeedback.objects.count(), 5)
        self.assertContains(blocked, 'өтө көп')

    def test_only_approved_notes_appear_and_the_email_stays_hidden(self):
        _note(message='Жашыруун мактоо', show_on_site=False)
        _note(message='Сабакка жакшы материал', name='Айгерим', show_on_site=True)
        _note(
            kind=WrittenFeedback.KIND_OPINION,
            message='Аты жок пикир',
            name='   ',
            email='other@example.com',
            show_on_site=True,
        )

        page = self.client.get(reverse('teacher_comments'))
        self.assertEqual(page.status_code, 200)
        html = page.content.decode()
        self.assertEqual(headings(html)['h1'], ['Мугалимдердин пикирлери'])
        self.assertIn('Сабакка жакшы материал', html)
        self.assertIn('Айгерим', html)
        self.assertIn('Аты жок пикир', html)
        self.assertIn('Мугалим', html)
        self.assertNotIn('Жашыруун мактоо', html)
        self.assertNotIn('secret@example.com', html)
        self.assertNotIn('other@example.com', html)
        self.assertNotIn('show_on_site', html)

    def test_admin_can_publish_filter_and_export(self):
        admin = Account.objects.create_superuser(
            email='isa@example.com',
            username='isa',
            password='SuperSecret123!',
        )
        self.client.force_login(admin)
        hidden = _note(message='Жашыруун мактоо', show_on_site=False)
        happy = PageReaction.objects.create(
            path='/', face=PageReaction.FACE_HAPPY, visitor_key='a' * 32,
        )
        PageReactionCount.objects.create(path='/', happy_count=1, sad_count=0)
        PageReaction.objects.create(
            path='/about/', face=PageReaction.FACE_SAD, visitor_key='b' * 32,
            material='MathKG жөнүндө',
        )
        PageReactionCount.objects.create(
            path='/about/', material='MathKG жөнүндө', sad_count=4, happy_count=0,
        )

        change = self.client.get(
            reverse('admin:personal_writtenfeedback_change', args=[hidden.pk])
        )
        self.assertContains(change, 'Show on site')
        self.assertContains(change, 'name="show_on_site"')

        self.client.post(
            reverse('admin:personal_writtenfeedback_changelist'),
            {
                'action': 'publish_feedback',
                'index': '0',
                '_selected_action': [str(hidden.pk)],
            },
        )
        hidden.refresh_from_db()
        self.assertTrue(hidden.show_on_site)

        exported = self.client.post(
            reverse('admin:personal_writtenfeedback_changelist'),
            {
                'action': 'export_feedback_csv',
                'index': '0',
                '_selected_action': [str(hidden.pk)],
            },
        )
        self.assertEqual(exported.status_code, 200)
        self.assertIn('text/csv', exported['Content-Type'])
        body = exported.content.decode('utf-8-sig')
        self.assertIn('secret@example.com', body)
        self.assertIn('Жашыруун мактоо', body)
        self.assertIn('Мактоо', body)

        reactions = self.client.get(reverse('admin:personal_pagereaction_changelist'))
        self.assertContains(reactions, '😊')
        self.assertContains(reactions, '🙁')

        ordered = list(PageReactionCount.objects.values_list('path', flat=True))
        self.assertEqual(ordered, ['/about/', '/'])
        counts = self.client.get(reverse('admin:personal_pagereactioncount_changelist'))
        self.assertContains(counts, '/about/')
        self.assertContains(counts, '4')
        self.assertEqual(happy.face, PageReaction.FACE_HAPPY)

        staff = Account.objects.create_user(
            email='staff-fb@example.com', username='stafffb', password='SuperSecret123!',
        )
        staff.is_staff = True
        staff.is_active = True
        staff.save(update_fields=['is_staff', 'is_active'])
        self.client.force_login(staff)
        dashboard = self.client.get(reverse('analytics_dashboard'))
        self.assertContains(dashboard, 'Page reactions')
        self.assertContains(dashboard, '😊 Жакты')
        self.assertContains(dashboard, 'Top pages by 🙁')
        self.assertContains(dashboard, 'MathKG жөнүндө')

    def test_news_mentions_the_feedback_page(self):
        match = [
            item for item in NEWS_ITEMS
            if item['title'] == 'Пикир калтыруу барагы ачылды'
        ]
        self.assertEqual(len(match), 1)
        self.assertEqual(match[0]['published_date'].isoformat(), '2026-11-03')
        self.assertIn('Пикир калтыруу', match[0]['body'])
