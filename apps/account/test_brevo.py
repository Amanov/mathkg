import json
import os
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.test import SimpleTestCase, override_settings

from apps.account.email_backends import BREVO_API_URL, DEFAULT_SENDER
from config.settings.base import sender_settings_from_env


class SenderSettingsTests(SimpleTestCase):
    def test_default_sender_is_the_authenticated_domain(self):
        resolved = sender_settings_from_env({})
        self.assertEqual(resolved['name'], 'MathKG')
        self.assertEqual(resolved['email'], 'no-reply@mathkg.com')
        self.assertEqual(resolved['header'], 'MathKG <no-reply@mathkg.com>')
        self.assertEqual(DEFAULT_SENDER, 'MathKG <no-reply@mathkg.com>')

    def test_address_and_name_env_compose_the_header(self):
        resolved = sender_settings_from_env({
            'BREVO_SENDER_NAME': '  Сабак  ',
            'BREVO_SENDER_EMAIL': ' lessons@mathkg.com ',
        })
        self.assertEqual(resolved['header'], 'Сабак <lessons@mathkg.com>')

    def test_default_from_email_overrides_the_composed_address(self):
        resolved = sender_settings_from_env({
            'BREVO_SENDER_EMAIL': 'lessons@mathkg.com',
            'DEFAULT_FROM_EMAIL': ' MathKG <custom@mathkg.com> ',
        })
        self.assertEqual(resolved['header'], 'MathKG <custom@mathkg.com>')
        self.assertEqual(resolved['email'], 'lessons@mathkg.com')

    def test_blank_pieces_fall_back_to_the_domain_default(self):
        resolved = sender_settings_from_env({
            'BREVO_SENDER_NAME': '   ',
            'BREVO_SENDER_EMAIL': '',
            'DEFAULT_FROM_EMAIL': '  ',
        })
        self.assertEqual(resolved['header'], 'MathKG <no-reply@mathkg.com>')

    def test_loaded_settings_follow_the_resolver(self):
        resolved = sender_settings_from_env(os.environ)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, resolved['header'])
        self.assertEqual(settings.BREVO_SENDER, resolved['header'])
        self.assertEqual(settings.BREVO_SENDER_EMAIL, resolved['email'])
        self.assertEqual(settings.BREVO_SENDER_NAME, resolved['name'])
        if not os.environ.get('DEFAULT_FROM_EMAIL') and not os.environ.get('BREVO_SENDER_EMAIL'):
            self.assertEqual(settings.DEFAULT_FROM_EMAIL, 'MathKG <no-reply@mathkg.com>')
            self.assertEqual(settings.BREVO_SENDER_EMAIL, 'no-reply@mathkg.com')
        if not os.environ.get('DEFAULT_REPLY_TO_EMAIL') and not os.environ.get('ADMIN_NOTIFICATION_EMAIL'):
            self.assertEqual(settings.DEFAULT_REPLY_TO_EMAIL, 'mathematicskgz@gmail.com')


@override_settings(
    EMAIL_BACKEND='apps.account.email_backends.BrevoEmailBackend',
    BREVO_API_KEY='test-key',
    DEFAULT_FROM_EMAIL='MathKG <no-reply@mathkg.com>',
    BREVO_SENDER_NAME='MathKG',
    DEFAULT_REPLY_TO_EMAIL='mathematicskgz@gmail.com',
)
class BrevoEmailBackendTests(SimpleTestCase):
    def _capture(self, send):
        response = MagicMock()
        response.read.return_value = b'{"messageId":"abc"}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        with patch('apps.account.email_backends.urlopen', return_value=response) as urlopen:
            sent = send()
        self.assertEqual(sent, 1)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, BREVO_API_URL)
        self.assertEqual(urlopen.call_args.kwargs['timeout'], 10)
        self.assertEqual(request.get_header('Api-key'), 'test-key')
        return request, json.loads(request.data.decode())

    def test_posts_json_to_brevo_with_the_domain_sender_and_reply_to(self):
        def send():
            return send_mail(
                'Тема',
                'Текст',
                'other@example.com',
                ['to@example.com'],
            )

        request, body = self._capture(send)
        self.assertEqual(body['sender'], {
            'name': 'MathKG',
            'email': 'no-reply@mathkg.com',
        })
        self.assertEqual(body['replyTo'], {
            'name': 'MathKG',
            'email': 'mathematicskgz@gmail.com',
        })
        self.assertEqual(body['to'], [{'email': 'to@example.com'}])
        self.assertEqual(body['subject'], 'Тема')
        self.assertEqual(body['textContent'], 'Текст')
        self.assertNotIn('other@example.com', request.data.decode())

    def test_bare_from_address_gets_the_sender_name(self):
        with override_settings(DEFAULT_FROM_EMAIL='no-reply@mathkg.com'):
            _, body = self._capture(
                lambda: send_mail('Тема', 'Текст', None, ['to@example.com'])
            )
        self.assertEqual(body['sender'], {
            'name': 'MathKG',
            'email': 'no-reply@mathkg.com',
        })

    def test_default_from_email_is_what_brevo_sends(self):
        with override_settings(DEFAULT_FROM_EMAIL='Сабак <lessons@mathkg.com>'):
            _, body = self._capture(
                lambda: send_mail('Тема', 'Текст', 'other@example.com', ['to@example.com'])
            )
        self.assertEqual(body['sender'], {
            'name': 'Сабак',
            'email': 'lessons@mathkg.com',
        })
        self.assertNotIn('other@example.com', json.dumps(body))

    def test_brevo_sender_is_used_when_default_from_email_is_empty(self):
        with override_settings(
            DEFAULT_FROM_EMAIL='',
            BREVO_SENDER='MathKG <legacy@mathkg.com>',
        ):
            _, body = self._capture(
                lambda: send_mail('Тема', 'Текст', None, ['to@example.com'])
            )
        self.assertEqual(body['sender']['email'], 'legacy@mathkg.com')

    def test_explicit_reply_to_replaces_the_inbox(self):
        def send():
            message = EmailMessage(
                'Жаңы жазылуу суранычы',
                'Текст',
                settings.DEFAULT_FROM_EMAIL,
                ['mathematicskgz@gmail.com'],
                reply_to=['teacher@example.com'],
            )
            return message.send(fail_silently=False)

        _, body = self._capture(send)
        self.assertEqual(body['replyTo'], {'email': 'teacher@example.com'})
        self.assertEqual(body['to'], [{'email': 'mathematicskgz@gmail.com'}])

    def test_missing_reply_to_setting_omits_the_field(self):
        with override_settings(DEFAULT_REPLY_TO_EMAIL=''):
            _, body = self._capture(
                lambda: send_mail('Тема', 'Текст', None, ['to@example.com'])
            )
        self.assertNotIn('replyTo', body)

    def test_http_failure_is_logged_and_does_not_raise(self):
        with patch('apps.account.email_backends.urlopen', side_effect=URLError('blocked')):
            with self.assertLogs('apps.account.email_backends', level='ERROR') as logs:
                sent = send_mail('Тема', 'Текст', None, ['to@example.com'])
        self.assertEqual(sent, 0)
        self.assertTrue(any('to@example.com' in line for line in logs.output))

    def test_missing_api_key_does_not_raise(self):
        with override_settings(BREVO_API_KEY=''):
            with patch('apps.account.email_backends.urlopen') as urlopen:
                with self.assertLogs('apps.account.email_backends', level='ERROR'):
                    sent = send_mail('Тема', 'Текст', None, ['to@example.com'])
        self.assertEqual(sent, 0)
        urlopen.assert_not_called()
