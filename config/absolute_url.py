"""Absolute public URLs for the canonical site.

``django.contrib.sites`` is not installed. A Site row would publish
example.com until someone edited it, and a later ``SITE_URL`` change
would not update that row. Settings are the source of truth instead.
"""
from urllib.parse import urlsplit

from django.conf import settings


def site_origin():
    """``https://mathkg.com`` with no trailing slash. Scheme is required."""
    return settings.SITE_URL.strip().rstrip('/')


def canonical_scheme():
    return urlsplit(site_origin()).scheme or 'https'


def canonical_netloc():
    """Host, plus a port when ``SITE_URL`` has one."""
    return urlsplit(site_origin()).netloc


def canonical_hostname():
    host = urlsplit(site_origin()).hostname or 'mathkg.com'
    return host.lower().rstrip('.')


def absolute_url(path=''):
    """Join ``SITE_URL`` and a path. An absolute URL keeps only its path and query."""
    origin = site_origin()
    if not path:
        return origin + '/'
    if path.startswith('http://') or path.startswith('https://'):
        parsed = urlsplit(path)
        path = parsed.path or '/'
        if parsed.query:
            path = f'{path}?{parsed.query}'
    elif not path.startswith('/'):
        path = '/' + path
    return origin + path
