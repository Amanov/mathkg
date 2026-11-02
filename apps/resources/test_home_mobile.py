from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class HomeMobileAndSignupEntryTests(TestCase):
    def test_home_keeps_one_viewport_and_the_mobile_rules(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('name="viewport" content="width=device-width, initial-scale=1"', html)
        self.assertNotIn('initial-scale=1.0', html)
        self.assertIn('body{ margin:0 !important; }', html)
        self.assertIn('html,body{ overflow-x:hidden; }', html)
        self.assertIn('.p-5{ padding:1rem !important; }', html)
        self.assertIn('.illustration-card{ padding:0; }', html)
        self.assertIn('h2,h3{ font-size:1.35rem; }', html)
        self.assertIn('h2 span[style*="48px"], h3 span[style*="48px"]{ font-size:1.75rem !important; }', html)

    def test_signup_button_and_free_trial_card_go_to_register(self):
        home = self.client.get(reverse('home'))
        register = reverse('register')
        self.assertContains(
            home,
            f'href="{register}"',
        )
        self.assertContains(home, '7 күн акысыз баштоо')
        self.assertNotContains(home, 'data-bs-target="#subscribeModal" data-track="Катталуу')

        login = self.client.get(reverse('login'))
        self.assertContains(login, f'href="{register}"')
        self.assertNotContains(login, 'data-bs-target="#subscribeModal"')

    def test_zoom_ignores_coarse_pointers(self):
        css = (settings.BASE_DIR / 'static' / 'css' / 'mk-zoom.css').read_text()
        script = (settings.BASE_DIR / 'static' / 'js' / 'mk-zoom.js').read_text()
        self.assertIn('@media (hover: hover) and (pointer: fine)', css)
        self.assertNotIn('@media (hover: hover) {', css)
        self.assertIn('"(hover: hover) and (pointer: fine)"', script)
        self.assertNotIn('"(hover: hover)"', script)
