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
# Fails loudly if neither is set, same as SECRET_KEY above - a silent
# fallback to ephemeral SQLite on the container's filesystem is exactly
# what destroyed production data before DATABASE_URL/Postgres was wired
# up, so this must never happen by accident again.
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600),
    }
elif os.environ.get('SQLITE_PATH'):
    # Explicit opt-in only: someone deliberately pointed this at a
    # path on a persistent volume, not the container's ephemeral disk.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ['SQLITE_PATH'],
        }
    }
else:
    raise ImproperlyConfigured(
        'No DATABASE_URL is set. Attach a persistent database (e.g. '
        "Railway's Postgres plugin), or set SQLITE_PATH to an explicit "
        'path on a persistent volume if SQLite is really intended.'
    )

# Persistent storage for uploaded media (the subscription QR code, and
# any future admin-uploaded resource files). Same root cause as the
# database above: Railway's Trial plan has no persistent Volume, so
# anything written to the container's own disk after a deploy vanishes
# on the next one. Optional and provider-agnostic (works with AWS S3,
# Cloudflare R2, Backblaze B2, or anything else that speaks the S3
# API) via AWS_S3_ENDPOINT_URL - only activates once all three
# credentials below are set, so this is a no-op until configured.
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

PERSISTENT_MEDIA_STORAGE_CONFIGURED = bool(
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME
)

if PERSISTENT_MEDIA_STORAGE_CONFIGURED:
    # Leave unset for real AWS S3; set to the provider's S3-compatible
    # endpoint otherwise (e.g. https://<account_id>.r2.cloudflarestorage.com
    # for Cloudflare R2).
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL') or None
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'auto')
    # Public URL host for reading files back (e.g. a bucket's own
    # pub-xxxx.r2.dev domain, or a custom domain in front of it) -
    # without this, django-storages builds URLs from the private API
    # endpoint above, which isn't necessarily the same host the bucket
    # is publicly reachable on.
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN') or None
    # R2/B2 don't support S3's ACL model the way AWS does - sending an
    # ACL on upload errors on some providers, so bucket-level public
    # access (configured once, on the provider's dashboard) replaces
    # per-object ACLs here.
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

