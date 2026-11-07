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
DEFAULT_SENDER = 'MathKG <no-reply@mathkg.com>'


def _address(value):
    name, email = parseaddr(value or '')
    email = (email or (value or '')).strip()
    if not email or '@' not in email:
        return None
    item = {'email': email}
    if name:
        item['name'] = name
    return item


def _sender_name():
    name = (getattr(settings, 'BREVO_SENDER_NAME', '') or 'MathKG').strip()
    return name or 'MathKG'


def _sender():
    # The verified From address is the setting, not message.from_email.
    # Brevo rejects a sender outside the authenticated domain, and a view
    # must not be able to point it at an arbitrary mailbox.
    for raw in (
        getattr(settings, 'DEFAULT_FROM_EMAIL', ''),
        getattr(settings, 'BREVO_SENDER', ''),
        DEFAULT_SENDER,
    ):
        parsed = _address(raw)
        if parsed:
            if 'name' not in parsed:
                parsed['name'] = _sender_name()
            return parsed
    return _address(DEFAULT_SENDER)


def default_reply_to_header():
    """Reply-To for mail a teacher might answer.

    no-reply@mathkg.com has no mailbox, so the header is the real inbox
    (``MathKG <inbox>`` unless DEFAULT_REPLY_TO_EMAIL already has a name).
    """
    raw = (getattr(settings, 'DEFAULT_REPLY_TO_EMAIL', '') or '').strip()
    parsed = _address(raw)
    if parsed is None:
        return ''
    if 'name' in parsed:
        return raw
    return f'{_sender_name()} <{parsed["email"]}>'


def default_reply_to_list():
    header = default_reply_to_header()
    return [header] if header else None


def _reply_to(message):
    # Brevo accepts one replyTo. An explicit message.reply_to (the
    # teacher, on an admin notice) wins over the site inbox.
    explicit = list(getattr(message, 'reply_to', None) or [])
    if explicit:
        for addr in explicit:
            parsed = _address(addr)
            if parsed:
                return parsed
        return None
    return _address(default_reply_to_header())


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
        reply_to = _reply_to(message)
        if reply_to:
            payload['replyTo'] = reply_to
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
