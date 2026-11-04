"""Canonical host: mathkg.com answers, the old hosts 301, sitemap uses it.

Railway terminates TLS, so a request that the browser made over HTTPS
arrives at gunicorn as HTTP plus ``X-Forwarded-Proto: https``. The host
redirect must not also upgrade the scheme by looking at the socket,
or that proxy header is ignored and the redirect never settles.
"""
from django.http import HttpResponse
from django.middleware.security import SecurityMiddleware
from django.test import RequestFactory, TestCase, override_settings

from config.middleware import CanonicalHostMiddleware

OLD_HOST = 'mathkg-production.up.railway.app'
APEX = 'mathkg.com'


@override_settings(
    SECURE_SSL_REDIRECT=True,
    SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
)
class CanonicalHostTests(TestCase):
    def test_railway_host_redirects_and_keeps_path_and_query(self):
        response = self.client.get(
            '/about/?q=1&b=2',
            HTTP_HOST=OLD_HOST,
            HTTP_X_FORWARDED_PROTO='https',
            secure=False,
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            'https://mathkg.com/about/?q=1&b=2',
        )

    def test_www_redirects_to_the_apex(self):
        response = self.client.post(
            '/topics/',
            HTTP_HOST='www.mathkg.com',
            HTTP_X_FORWARDED_PROTO='https',
            secure=False,
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://mathkg.com/topics/')

    def test_mathkg_com_serves_the_home_page(self):
        response = self.client.get(
            '/',
            HTTP_HOST=APEX,
            HTTP_X_FORWARDED_PROTO='https',
            secure=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response['Content-Type'])
        self.assertContains(response, 'MathKG')

    def test_sitemap_uses_mathkg_com(self):
        redirected = self.client.get(
            '/sitemap.xml',
            HTTP_HOST=OLD_HOST,
            secure=True,
        )
        self.assertEqual(redirected.status_code, 301)
        self.assertEqual(redirected['Location'], 'https://mathkg.com/sitemap.xml')

        response = self.client.get(
            '/sitemap.xml',
            HTTP_HOST=APEX,
            HTTP_X_FORWARDED_PROTO='https',
            secure=False,
        )
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('https://mathkg.com/', body)
        self.assertNotIn('railway.app', body)
        self.assertNotIn('www.mathkg.com', body)

    def test_healthcheck_host_is_not_redirected(self):
        # nixpacks.json sets no healthcheck path, and there is no
        # railway.toml. Railway's probe, once a path is configured, uses
        # this Host and must get a 2xx rather than a 301.
        response = self.client.get(
            '/',
            HTTP_HOST='healthcheck.railway.app',
            HTTP_X_FORWARDED_PROTO='https',
            secure=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Location', response)

    def test_proxy_https_does_not_loop_on_the_apex(self):
        """SecurityMiddleware is built inside the override so it sees the flag.

        The test client reuses the process middleware, which read
        SECURE_SSL_REDIRECT at startup (false in development).
        """
        seen = {}

        def get_response(request):
            seen['secure'] = request.is_secure()
            return HttpResponse('ok')

        middleware = CanonicalHostMiddleware(SecurityMiddleware(get_response))
        factory = RequestFactory()

        apex = factory.get(
            '/about/?q=1',
            HTTP_HOST=APEX,
            HTTP_X_FORWARDED_PROTO='https',
        )
        response = middleware(apex)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(seen['secure'])

        www = factory.get(
            '/about/?q=1',
            HTTP_HOST='www.mathkg.com',
            HTTP_X_FORWARDED_PROTO='https',
        )
        response = middleware(www)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://mathkg.com/about/?q=1')

        insecure_apex = factory.get('/about/', HTTP_HOST=APEX)
        response = middleware(insecure_apex)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://mathkg.com/about/')
