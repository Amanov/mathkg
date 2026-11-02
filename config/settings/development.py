import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'mathkg-production.up.railway.app',
    'localhost',
    '127.0.0.1',
]
# base.py turns on Brevo when BREVO_API_KEY is set. Keep that. Otherwise
# print mail locally even if EMAIL_HOST is present, so a laptop does not
# try SMTP.
if not os.environ.get('BREVO_API_KEY'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'