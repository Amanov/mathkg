from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import reverse

from apps.resources.sitemaps import SITEMAPS

# Same rules as the file prepared for Google and Yandex. The Sitemap
# line is the only part that follows the host, so a custom domain does
# not leave robots.txt pointing at the Railway hostname.
ROBOTS_TEMPLATE = """\
User-agent: *
Allow: /
Disallow: /login/
Disallow: /register/
Disallow: /resources/download/

Sitemap: {sitemap}
"""


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse('sitemap'))
    body = ROBOTS_TEMPLATE.format(sitemap=sitemap_url)
    return HttpResponse(body, content_type='text/plain')


def sitemap_xml(request):
    """The built-in sitemap view, without its noindex header.

    Django adds ``X-Robots-Tag: noindex`` so the sitemap file is not
    listed as a web page. Yandex treats that header as "do not use this
    document", which would drop the sitemap the owner is about to submit.
    The body is an XML urlset, not an HTML page.
    """
    response = sitemap(request, SITEMAPS)
    response.headers.pop('X-Robots-Tag', None)
    return response
