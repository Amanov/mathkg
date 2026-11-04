import os

from .base import *

DEBUG = True

# Same public hosts as production, without the ``.railway.app`` wildcard.
# base.py already sets this list; keep it here so a local override of
# base.py cannot drop mathkg.com from the development server.
ALLOWED_HOSTS = [
    *PUBLIC_HOSTS,
    'localhost',
    '127.0.0.1',
]
# base.py turns on Brevo when BREVO_API_KEY is set. Keep that. Otherwise
# print mail locally even if EMAIL_HOST is present, so a laptop does not
# try SMTP.
if not os.environ.get('BREVO_API_KEY'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'