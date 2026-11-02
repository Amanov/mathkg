"""Send Django mail through Brevo's transactional HTTP API.

Railway blocks outbound SMTP, so a normal SMTP backend hangs until the
worker is killed and the registration request returns 500. This backend
POSTs to https://api.brevo.com/v3/smtp/email with a 10-second timeout.
A missing key, a network error, or a Brevo error is logged and swallowed:
sign-up, password reset, and admin notifications must still finish.
"""

import json
import logging
from email.utils import parseaddr
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'
BREVO_TIMEOUT_SECONDS = 10
DEFAULT_SENDER = 'MathKG <mathematicskgz@gmail.com>'


def _address(value):
    name, email = parseaddr(value or '')
    email = (email or (value or '')).strip()
    if not email:
        return None
    item = {'email': email}
    if name:
        item['name'] = name
    return item


def _sender():
    parsed = _address(getattr(settings, 'BREVO_SENDER', '') or DEFAULT_SENDER)
    if parsed is None:
        parsed = _address(DEFAULT_SENDER)
    if 'name' not in parsed:
        parsed['name'] = 'MathKG'
    return parsed


class BrevoEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        api_key = getattr(settings, 'BREVO_API_KEY', '') or ''
        if not api_key:
            logger.error('BREVO_API_KEY is not set; email was not sent.')
            return 0
        sent = 0
        for message in email_messages:
            if self._send(message, api_key):
                sent += 1
        return sent

    def _payload(self, message):
        payload = {
            'sender': _sender(),
            'to': [item for item in (_address(addr) for addr in message.to) if item],
            'subject': message.subject,
            'textContent': message.body,
        }
        cc = [item for item in (_address(addr) for addr in message.cc) if item]
        bcc = [item for item in (_address(addr) for addr in message.bcc) if item]
        if cc:
            payload['cc'] = cc
        if bcc:
            payload['bcc'] = bcc
        for content, mimetype in getattr(message, 'alternatives', None) or []:
            if mimetype == 'text/html':
                payload['htmlContent'] = content
                break
        return payload

    def _send(self, message, api_key):
        recipients = ', '.join(message.to)
        try:
            payload = self._payload(message)
            if not payload['to']:
                logger.error('Brevo email to %s has no recipient.', recipients)
                return False
            request = Request(
                BREVO_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'accept': 'application/json',
                    'content-type': 'application/json',
                    'api-key': api_key,
                },
                method='POST',
            )
            with urlopen(request, timeout=BREVO_TIMEOUT_SECONDS) as response:
                response.read()
            return True
        except Exception:
            logger.exception('Failed to send email via Brevo to %s', recipients)
            return False
