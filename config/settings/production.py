from .base import *

DEBUG = True

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


# settings.py
# Use basic storage instead of compressed storage during build
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # Disable or change to basic:
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'