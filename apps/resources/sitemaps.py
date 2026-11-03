"""Public sitemap: lesson routes plus topic pages from the database.

Absolute URLs are built by Django's sitemap view from the request host
(RequestSite). django.contrib.sites is not installed. A Site row would
publish example.com in every <loc> until somebody edited it in admin,
and it would ignore a custom domain until that edit happened.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import URLResolver, get_resolver
from django.urls.resolvers import RoutePattern

from apps.resources.models import SubSubtopic, Subtopic, Topic

# Not curriculum pages. robots.txt also disallows login, register, and
# downloads. The rest are account flows, staff tools, or write-only endpoints.
EXCLUDED_PATHS = {
    '/login/',
    '/logout/',
    '/register/',
    '/register/check-email/',
    '/registration-success/',
    '/account/',
    '/activate/resend/',
    '/password_change/',
    '/password_change/done/',
    '/password_reset/',
    '/password_reset/done/',
    '/reset/done/',
    '/dashboard/',
    '/analytics/',
    '/track-click/',
    '/subscribe/',
    '/search/suggest/',
    '/tarsia-builder/export/',
    # These are the crawler files themselves, not pages to index.
    '/robots.txt',
    '/sitemap.xml',
    # The topic menu, fetched after the first screen. The links
    # themselves are on /topics/ and in this sitemap.
    '/menu/',
    # A write-only face counter, not a page.
    '/page-reaction/',
}

EXCLUDED_PREFIXES = (
    '/resources/download/',
    '/activate/',
    '/reset/',
    '/media/',
)


def _public_location(route):
    """The path Django actually matches. Do not invent a trailing slash.

    Lesson routes already end in ``/``. ``robots.txt`` and ``sitemap.xml``
    do not, and ``/robots.txt/`` is not a URL.
    """
    if route in ('', '/'):
        return '/'
    if not route.startswith('/'):
        route = '/' + route
    return route


def _excluded(path):
    if path in EXCLUDED_PATHS:
        return True
    return any(path.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def iter_public_static_paths():
    """Argument-free public routes, in URLconf order, without duplicates."""
    seen = set()
    for path in _walk(get_resolver(), ''):
        if path in seen or _excluded(path):
            continue
        seen.add(path)
        yield path


def _walk(resolver, prefix):
    for entry in resolver.url_patterns:
        if isinstance(entry, URLResolver):
            # Admin's own namespace, including a non-default ADMIN_URL_PATH.
            if entry.namespace == 'admin':
                continue
            yield from _walk(entry, prefix + str(entry.pattern))
            continue
        # /media/ and the DEBUG static() helper are regex routes.
        if not isinstance(entry.pattern, RoutePattern):
            continue
        if entry.name in ('robots_txt', 'sitemap'):
            continue
        route = prefix + str(entry.pattern)
        if any(token in route for token in ('<', '(', '^', ' ')):
            continue
        yield _public_location(route)


class _NonEmptySitemap(Sitemap):
    """Skip an empty section.

    Django's sitemap view turns EmptyPage into a 404 for the whole
    /sitemap.xml file. A database with no topics yet must still publish
    the static lesson pages.
    """

    def get_urls(self, page=1, site=None, protocol=None):
        items = self.items()
        if hasattr(items, 'exists'):
            empty = not items.exists()
        else:
            empty = not items
        if empty:
            return []
        return super().get_urls(page=page, site=site, protocol=protocol)


class StaticPageSitemap(_NonEmptySitemap):
    changefreq = 'weekly'

    def items(self):
        return list(iter_public_static_paths())

    def location(self, item):
        return item

    def priority(self, item):
        if item in ('/', '/home/'):
            return 1.0
        return 0.6


class TopicSitemap(_NonEmptySitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Topic.objects.order_by('slug')


class SubtopicSitemap(_NonEmptySitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Subtopic.objects.select_related('topic').order_by(
            'topic__slug', 'slug',
        )


class SubSubtopicSitemap(_NonEmptySitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return SubSubtopic.objects.select_related('subtopic__topic').order_by(
            'subtopic__topic__slug', 'subtopic__slug', 'slug',
        )


SITEMAPS = {
    'static': StaticPageSitemap,
    'topics': TopicSitemap,
    'subtopics': SubtopicSitemap,
    'subsubtopics': SubSubtopicSitemap,
}
