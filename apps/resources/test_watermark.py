"""The MathKG advert stamped on every downloaded PDF."""

import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pymupdf
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.resources import watermark
from apps.resources.free_download import choose_free_resource
from apps.resources.models import PageFreeDownload, Resource


def _pdf(width=842, height=595, pages=2, text='Worksheet 1'):
    doc = pymupdf.open()
    for _ in range(pages):
        page = doc.new_page(width=width, height=height)
        page.insert_text((40, 60), text, fontsize=14)
    return doc.tobytes()


def _texts(data):
    doc = pymupdf.open(stream=data, filetype='pdf')
    return [page.get_text() for page in doc], [tuple(page.rect) for page in doc]


@override_settings(SITE_URL='https://mathkg.com')
class StampTests(TestCase):
    def test_every_page_keeps_its_size_and_gets_the_advert(self):
        texts, rects = _texts(watermark.stamp_pdf(_pdf(pages=3)))
        self.assertEqual(rects, [(0, 0, 842, 595)] * 3)
        for text in texts:
            self.assertIn('Worksheet 1', text)
            self.assertIn('mathkg.com', text)
            self.assertIn('даяр сабактар', text)

    def test_each_copy_on_an_a5_or_a6_sheet_gets_its_own_band(self):
        for layout, copies in (('a5', 2), ('a6', 4)):
            texts, _ = _texts(watermark.stamp_pdf(_pdf(pages=1), layout))
            self.assertEqual(texts[0].count('mathkg.com'), copies, layout)

    def test_layout_comes_from_the_file_name(self):
        self.assertEqual(watermark.layout_for('x-ish-barak-a5.pdf'), 'a5')
        self.assertEqual(watermark.layout_for('resources/files/x-a6.pdf'), 'a6')
        self.assertEqual(watermark.layout_for('x-ish-barak.pdf'), 'single')

    def test_the_link_and_qr_point_at_the_site(self):
        doc = pymupdf.open(stream=watermark.stamp_pdf(_pdf(pages=1)), filetype='pdf')
        self.assertEqual([link['uri'] for link in doc[0].get_links()], ['https://mathkg.com/'])


@override_settings(SITE_URL='https://mathkg.com')
class StampedDownloadTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, True)
        cache = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, cache, True)
        for patcher in (
            override_settings(MEDIA_ROOT=self.media),
            mock.patch.object(watermark, 'CACHE_DIR', Path(cache) / 'stamped'),
        ):
            patcher.enable() if hasattr(patcher, 'enable') else patcher.start()
            self.addCleanup(patcher.disable if hasattr(patcher, 'disable') else patcher.stop)

    def _free(self, name, contents):
        resource = Resource.objects.create(
            title=name, category='worksheet', is_active=True,
            file=SimpleUploadedFile(name, contents),
        )
        choose_free_resource('four_basic_operations', [resource])
        PageFreeDownload.objects.filter(page_key='four_basic_operations').update(
            resource=resource, pinned=True,
        )
        return resource

    def _get(self, resource):
        response = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(response.status_code, 200)
        return response, b''.join(response.streaming_content)

    def test_a_pdf_download_is_stamped_and_cached(self):
        resource = self._free('4-klass-ish-barak.pdf', _pdf(pages=1))
        response, body = self._get(resource)
        self.assertIn('4-klass-ish-barak', response['Content-Disposition'])
        self.assertIn('mathkg.com', _texts(body)[0][0])
        self.assertEqual(len(list(watermark.CACHE_DIR.iterdir())), 1)
        _, again = self._get(resource)
        self.assertEqual(again, body)

    def test_other_files_and_broken_pdfs_are_served_unchanged(self):
        deck = self._free('sabak.pptx', b'pptx-bytes')
        self.assertEqual(self._get(deck)[1], b'pptx-bytes')
        broken = self._free('bad.pdf', b'not a pdf')
        with self.assertLogs('apps.resources.watermark', 'ERROR'):
            self.assertEqual(self._get(broken)[1], b'not a pdf')

    def test_a_signed_in_teachers_copy_names_them(self):
        from datetime import timedelta

        from django.utils import timezone

        from apps.resources.test_assessment import _user

        teacher = _user(
            'aigul.asanova@gmail.com', 'aigul',
            subscription_end=timezone.localdate() + timedelta(days=30),
        )
        self.client.force_login(teacher)
        resource = self._free('5-klass-ish-barak-a6.pdf', _pdf(pages=1))
        _, body = self._get(resource)
        text = _texts(body)[0][0]
        self.assertEqual(text.count('Жүктөгөн: aigul (ai***@gmail.com)'), 4)
        self.assertNotIn('aigul.asanova@gmail.com', text)
        self.assertIn(f'{timezone.localdate():%d.%m.%Y}', text)

        self.client.logout()
        _, anonymous = self._get(resource)
        self.assertNotIn('Жүктөгөн', _texts(anonymous)[0][0])


class OwnerLineTests(TestCase):
    def test_email_is_masked(self):
        self.assertEqual(watermark.mask_email('aigul.asanova@gmail.com'), 'ai***@gmail.com')
        self.assertEqual(watermark.mask_email(''), '')
