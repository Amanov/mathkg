from django.conf import settings
from django.http import HttpResponsePermanentRedirect

from config.absolute_url import canonical_hostname


def request_hostname(request):
    """Hostname only, lowercased, without a port or a trailing dot.

    ``get_host()`` enforces ``ALLOWED_HOSTS`` and raises ``DisallowedHost``
    for anything else (the 400 mathkg.com used to return).
    """
    host = request.get_host()
    if host.startswith('[') and ']' in host:
        host = host[1:host.index(']')]
    else:
        host = host.split(':', 1)[0]
    return host.lower().rstrip('.')


class CanonicalHostMiddleware:
    """301 ``www`` and the old Railway host to ``SITE_URL``.

    Railway terminates TLS and forwards plain HTTP with
    ``X-Forwarded-Proto: https``. This middleware does not look at the
    scheme. ``SecurityMiddleware`` already redirects HTTP to HTTPS using
    ``SECURE_PROXY_SSL_HEADER``. A second scheme check that ignored that
    header would redirect every proxied request and loop.

    The target is always ``SITE_URL`` (https://mathkg.com by default),
    never the host that just arrived, and a host equal to that target
    is left alone. ``healthcheck.railway.app`` is not in
    ``CANONICAL_REDIRECT_HOSTS``. nixpacks.json has no healthcheck path,
    and there is no railway.toml or railway.json, so Railway is not
    probing a path today. When a probe is configured it uses that
    hostname and requires a 2xx response, which a 301 would fail.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request_hostname(request)
        target = canonical_hostname()
        redirect_hosts = {
            item.lower().rstrip('.')
            for item in settings.CANONICAL_REDIRECT_HOSTS
        }
        if host in redirect_hosts and host != target:
            location = settings.SITE_URL.strip().rstrip('/') + request.get_full_path()
            return HttpResponsePermanentRedirect(location)
        return self.get_response(request)
