import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from django.core.mail import send_mail
from django.test import SimpleTestCase, override_settings

from apps.account.email_backends import BREVO_API_URL


@override_settings(
    EMAIL_BACKEND='apps.account.email_backends.BrevoEmailBackend',
    BREVO_API_KEY='test-key',
    BREVO_SENDER='MathKG <mathematicskgz@gmail.com>',
)
class BrevoEmailBackendTests(SimpleTestCase):
    def test_posts_json_to_brevo_with_a_ten_second_timeout(self):
        response = MagicMock()
        response.read.return_value = b'{"messageId":"abc"}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with patch('apps.account.email_backends.urlopen', return_value=response) as urlopen:
            sent = send_mail(
                'Тема',
                'Текст',
                'other@example.com',
                ['to@example.com'],
            )

        self.assertEqual(sent, 1)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, BREVO_API_URL)
        self.assertEqual(urlopen.call_args.kwargs['timeout'], 10)
        self.assertEqual(request.get_header('Api-key'), 'test-key')
        body = json.loads(request.data.decode())
        self.assertEqual(body['sender'], {
            'name': 'MathKG',
            'email': 'mathematicskgz@gmail.com',
        })
        self.assertEqual(body['to'], [{'email': 'to@example.com'}])
        self.assertEqual(body['subject'], 'Тема')
        self.assertEqual(body['textContent'], 'Текст')
        self.assertNotIn('other@example.com', request.data.decode())

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
