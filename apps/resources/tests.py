from datetime import date

from django.test import TestCase
from django.urls import reverse

from apps.resources.models import NewsPost


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
