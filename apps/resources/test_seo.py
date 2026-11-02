"""robots.txt and sitemap.xml for crawlers.

The path list in test_data/crawled_public_paths.txt is the public crawl
of the live site (1061 URLs). lastmod values in that crawl were
placeholders, so this checks the URL set, not dates.
"""
import os
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from django.conf import settings
from django.test import TestCase

from apps.resources.models import SiteVisit, SubSubtopic, Subtopic, Topic

CRAWL_PATH = Path(__file__).resolve().parent / 'test_data' / 'crawled_public_paths.txt'
SITEMAP_NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
LIVE_HOST = 'mathkg-production.up.railway.app'


def crawled_paths():
    return [
        line.strip()
        for line in CRAWL_PATH.read_text().splitlines()
        if line.strip()
    ]


def seed_crawled_topics(paths):
    """Make sure every crawled topic page has a row.

    Migrations already insert part of the tree. get_or_create fills only
    the slugs the crawl has and the database does not.
    """
    topics = {}
    subtopics = {}
    for path in paths:
        if not path.startswith('/resources/topic/'):
            continue
        slugs = path.strip('/').split('/')[2:]
        topic = topics.get(slugs[0])
        if topic is None:
            topic, _created = Topic.objects.get_or_create(
                slug=slugs[0], defaults={'title': slugs[0]},
            )
            topics[slugs[0]] = topic
        if len(slugs) < 2:
            continue
        key = (slugs[0], slugs[1])
        subtopic = subtopics.get(key)
        if subtopic is None:
            subtopic, _created = Subtopic.objects.get_or_create(
                topic=topic, slug=slugs[1], defaults={'title': slugs[1]},
            )
            subtopics[key] = subtopic
        if len(slugs) == 3:
            SubSubtopic.objects.get_or_create(
                subtopic=subtopic, slug=slugs[2], defaults={'title': slugs[2]},
            )


def sitemap_paths(response):
    root = ET.fromstring(response.content)
    locs = []
    for loc in root.findall('sm:url/sm:loc', SITEMAP_NS):
        url = loc.text
        path = '/' + url.split('://', 1)[1].split('/', 1)[1]
        locs.append(path)
    return locs


class RobotsAndSitemapTests(TestCase):
    def test_robots_is_plain_text_and_follows_the_request_host(self):
        response = self.client.get(
            '/robots.txt', HTTP_HOST=LIVE_HOST, secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('text/plain'))
        self.assertEqual(
            response.content.decode(),
            'User-agent: *\n'
            'Allow: /\n'
            'Disallow: /login/\n'
            'Disallow: /register/\n'
            'Disallow: /resources/download/\n'
            '\n'
            f'Sitemap: https://{LIVE_HOST}/sitemap.xml\n',
        )

        local = self.client.get('/robots.txt', HTTP_HOST='localhost', secure=True)
        self.assertIn(
            'Sitemap: https://localhost/sitemap.xml',
            local.content.decode(),
        )
        self.assertNotIn(LIVE_HOST, local.content.decode())
        self.assertFalse(SiteVisit.objects.filter(path='/robots.txt').exists())

    def test_sitemap_is_xml_and_omits_private_urls(self):
        response = self.client.get(
            '/sitemap.xml', HTTP_HOST=LIVE_HOST, secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])
        # Django's stock sitemap view sends X-Robots-Tag: noindex. Yandex
        # will not use a document that header marks noindex.
        self.assertIsNone(response.get('X-Robots-Tag'))
        paths = sitemap_paths(response)
        self.assertIn('/about/', paths)
        self.assertIn('/home/', paths)
        self.assertIn('/', paths)
        body = response.content.decode()
        self.assertNotIn('/login/', body)
        self.assertNotIn('/register/', body)
        self.assertNotIn('/resources/download/', body)
        self.assertNotIn('/account/', body)
        self.assertNotIn('/dashboard/', body)
        self.assertNotIn(f'https://{LIVE_HOST}/robots.txt', body)
        self.assertNotIn(f'https://{LIVE_HOST}/sitemap.xml', body)
        self.assertTrue(body.startswith('<?xml'))
        self.assertIn(f'https://{LIVE_HOST}/about/', body)
        self.assertFalse(SiteVisit.objects.filter(path='/sitemap.xml').exists())

    def test_sitemap_covers_the_crawled_public_pages(self):
        crawled = crawled_paths()
        self.assertGreater(len(crawled), 1000)
        seed_crawled_topics(crawled)

        response = self.client.get(
            '/sitemap.xml', HTTP_HOST=LIVE_HOST, secure=True,
        )
        self.assertEqual(response.status_code, 200)
        generated = set(sitemap_paths(response))
        missing = sorted(set(crawled) - generated)
        extra = sorted(generated - set(crawled))
        self.assertEqual(
            missing,
            [],
            'Crawled public pages missing from the sitemap',
        )
        # Lesson routes the crawl never linked, plus one index page per
        # topic (/resources/topic/<topic>/). Kept well under the crawl.
        self.assertLess(
            len(extra),
            80,
            'Sitemap grew past the crawled public set:\n' + '\n'.join(extra),
        )
        self.assertGreater(len(generated), 1000)
        self.assertIn('/resources/topic/algebra/equations-linear/', generated)
        self.assertIn(
            '/resources/topic/algebra/equations-linear/forming/',
            generated,
        )
        self.assertIn('/resources/topic/algebra/', generated)

    def test_production_settings_allow_the_live_host_without_sites(self):
        code = """
import os
os.environ["SECRET_KEY"] = "test-secret"
os.environ["DATABASE_URL"] = "sqlite:////tmp/mathkg-seo-settings.sqlite3"
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ["EXTRA_ALLOWED_HOSTS"] = "mathkg.kg"
os.environ["EXTRA_CSRF_TRUSTED_ORIGINS"] = "https://mathkg.kg"
import django
django.setup()
from django.conf import settings
checks = {
    "live host": "mathkg-production.up.railway.app" in settings.ALLOWED_HOSTS,
    "custom host": "mathkg.kg" in settings.ALLOWED_HOSTS,
    "custom origin": "https://mathkg.kg" in settings.CSRF_TRUSTED_ORIGINS,
    "sitemaps app": "django.contrib.sitemaps" in settings.INSTALLED_APPS,
    "sites app off": "django.contrib.sites" not in settings.INSTALLED_APPS,
    "static url": settings.STATIC_URL == "/static/",
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("failed: " + ", ".join(failed))
print("ok")
"""
        env = os.environ.copy()
        env["PYTHONPATH"] = str(settings.BASE_DIR)
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=settings.BASE_DIR,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            completed.stdout + completed.stderr,
        )
        self.assertIn("ok", completed.stdout)
