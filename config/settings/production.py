import os

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

# Fail loudly rather than silently falling back to the dev-only key
# defined in base.py if the real secret isn't set on the host.
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured(
        'The SECRET_KEY environment variable must be set in production.'
    )

ALLOWED_HOSTS = [
    'mathkg-production.up.railway.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    'https://mathkg-production.up.railway.app',
    'https://*.up.railway.app',
]

# The app sits behind Railway's TLS-terminating proxy, so trust its
# forwarded-proto header and enforce HTTPS/secure cookies accordingly.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Start HSTS conservatively (1 hour) - raise once HTTPS is confirmed
# stable, since browsers cache this and a long value is hard to undo.
SECURE_HSTS_SECONDS = 3600

