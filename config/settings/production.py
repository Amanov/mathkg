import os

import dj_database_url
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

# This app was persisting its SQLite database only by committing
# db.sqlite3 to git and redeploying it each time - once that file was
# rightly untracked (it held live password hashes), every fresh
# container got a brand-new empty database, since Railway's container
# filesystem isn't persisted across deploys by default. Volumes aren't
# available on the Trial plan, so use Railway's Postgres plugin
# instead (DATABASE_URL is set automatically once it's attached).
# Falls back to ephemeral SQLite so this doesn't hard-crash if
# DATABASE_URL isn't set yet.
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get('SQLITE_PATH', str(BASE_DIR / 'db.sqlite3')),
        }
    }

