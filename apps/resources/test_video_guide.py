from django.test import TestCase
from django.urls import reverse


class VideoGuideTests(TestCase):
    def test_page_shows_the_video(self):
        response = self.client.get(reverse('video_guide'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'video/mathkg-onboarding.mp4')
        self.assertContains(response, 'preload="none"')

    def test_home_and_footer_link_to_it(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'class="home-video"')
        self.assertContains(response, reverse('video_guide'))

    def test_page_is_in_sitemap(self):
        response = self.client.get('/sitemap.xml')
        self.assertContains(response, '/video-koldonmo/')
