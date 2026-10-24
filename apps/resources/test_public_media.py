import shutil
import tempfile
from datetime import timedelta
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.account.models import Account, SubscriptionRequest
from apps.resources.free_download import choose_free_resource
from apps.resources.models import PageFreeDownload, Resource


def _body(response):
    return b''.join(response.streaming_content)


class PublicMediaTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, True)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)

    def _write(self, relative, body):
        path = Path(self.media) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        return path

    def test_paid_resource_file_is_not_public(self):
        self._write('resources/files/secret.pptx', b'paid-bytes')
        response = self.client.get('/media/resources/files/secret.pptx')
        self.assertEqual(response.status_code, 404)
        self.assertTrue((Path(self.media) / 'resources/files/secret.pptx').exists())

    def test_other_private_upload_dirs_are_not_public(self):
        self._write('resources/old.pptx', b'old')
        self._write('downloads/secret.pdf', b'secret')
        self.assertEqual(self.client.get('/media/resources/old.pptx').status_code, 404)
        self.assertEqual(self.client.get('/media/downloads/secret.pdf').status_code, 404)

    def test_thumbnail_and_payment_qr_are_public(self):
        self._write('resources/images/thumb.png', b'png-bytes')
        self._write('payment_qr/qr.png', b'qr-bytes')
        thumb = self.client.get('/media/resources/images/thumb.png')
        qr = self.client.get('/media/payment_qr/qr.png')
        self.assertEqual(thumb.status_code, 200)
        self.assertEqual(_body(thumb), b'png-bytes')
        self.assertEqual(qr.status_code, 200)
        self.assertEqual(_body(qr), b'qr-bytes')

    def test_path_traversal_out_of_the_allowlist_is_rejected(self):
        self._write('resources/files/secret.pptx', b'paid-bytes')
        paths = [
            '/media/resources/images/../../resources/files/secret.pptx',
            '/media/resources/images/../files/secret.pptx',
            '/media/payment_qr/../../resources/files/secret.pptx',
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)

    @override_settings(DEBUG=False)
    def test_allowlist_holds_when_debug_is_off(self):
        self._write('resources/files/secret.pptx', b'paid-bytes')
        self._write('resources/images/thumb.png', b'png-bytes')
        self.assertEqual(
            self.client.get(
                '/media/resources/files/secret.pptx',
                HTTP_HOST='127.0.0.1',
            ).status_code,
            404,
        )
        thumb = self.client.get(
            '/media/resources/images/thumb.png',
            HTTP_HOST='127.0.0.1',
        )
        self.assertEqual(thumb.status_code, 200)
        self.assertEqual(_body(thumb), b'png-bytes')


class DownloadRouteTests(TestCase):
    """Closing /media/resources/files/ must not change who can download."""

    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, True)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)
        self.free = Resource.objects.create(
            title='FreeFile',
            category='presentation',
            is_active=True,
            file=SimpleUploadedFile('free.pptx', b'free-bytes'),
        )
        self.paid = Resource.objects.create(
            title='PaidFile',
            category='presentation',
            is_active=True,
            file=SimpleUploadedFile('paid.pptx', b'paid-bytes'),
        )
        choose_free_resource('paywall-page', [self.free])
        PageFreeDownload.objects.filter(page_key='paywall-page').update(
            resource=self.free, pinned=True,
        )

    def test_logged_out_free_download_works_and_the_media_url_does_not(self):
        media = self.client.get('/media/' + self.free.file.name)
        self.assertEqual(media.status_code, 404)
        response = self.client.get(reverse('download_resource', args=[self.free.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertEqual(_body(response), b'free-bytes')

    def test_subscriber_download_works_and_the_media_url_does_not(self):
        user = Account.objects.create_user(
            email='subscriber@example.com',
            username='subscriber',
            password='SuperSecret123!',
        )
        user.is_active = True
        user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        user.subscription_end = timezone.now().date() + timedelta(days=30)
        user.save(update_fields=['is_active', 'current_plan', 'subscription_end'])
        self.client.login(email='subscriber@example.com', password='SuperSecret123!')

        media = self.client.get('/media/' + self.paid.file.name)
        self.assertEqual(media.status_code, 404)
        response = self.client.get(reverse('download_resource', args=[self.paid.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertEqual(_body(response), b'paid-bytes')

    def test_logged_out_paid_download_still_requires_login(self):
        response = self.client.get(reverse('download_resource', args=[self.paid.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
