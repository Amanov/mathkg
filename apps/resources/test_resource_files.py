import shutil
import tempfile
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.resources.free_download import choose_free_resource
from apps.resources.models import PageFreeDownload, Resource
from apps.resources.resource_files import repair_four_basic_free_file


def _files(media):
    path = Path(media) / 'resources' / 'files'
    path.mkdir(parents=True, exist_ok=True)
    return path


class ResourceFileFallbackTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, True)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)
        self.client.logout()

    def _resource(self, title, stored_name, contents=b'original'):
        resource = Resource.objects.create(
            title=title,
            category='presentation',
            is_active=True,
            file=SimpleUploadedFile('placeholder.bin', contents),
        )
        resource.file.name = stored_name
        resource.save(update_fields=['file'])
        return resource

    def _pin(self, resource):
        choose_free_resource('four_basic_operations', [resource])
        PageFreeDownload.objects.filter(page_key='four_basic_operations').update(
            resource=resource, pinned=True,
        )

    def test_missing_stored_path_serves_the_file_named_by_the_title(self):
        resource = self._resource(
            'amaldar_tartibi_ozun_tuz_v2.pptx',
            'resources/files/missing.pptx',
        )
        _files(self.media).joinpath('amaldar_tartibi_ozun_tuz_v2.pptx').write_bytes(b'v2-bytes')
        self._pin(resource)

        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b''.join(resp.streaming_content), b'v2-bytes')
        resource.refresh_from_db()
        self.assertEqual(resource.file.name, 'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx')
        self.assertEqual(resp['Content-Disposition'].count('amaldar_tartibi_ozun_tuz_v2.pptx'), 1)

    def test_a_single_collision_suffix_is_served(self):
        resource = self._resource(
            'amaldar_tartibi_ozun_tuz_v2.pptx',
            'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx',
        )
        _files(self.media).joinpath(
            'amaldar_tartibi_ozun_tuz_v2_Abcdef1.pptx',
        ).write_bytes(b'suffixed')
        self._pin(resource)

        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b''.join(resp.streaming_content), b'suffixed')
        resource.refresh_from_db()
        self.assertEqual(
            resource.file.name,
            'resources/files/amaldar_tartibi_ozun_tuz_v2_Abcdef1.pptx',
        )

    def test_two_collision_suffixes_are_not_guessed(self):
        resource = self._resource(
            'unrelated.pptx',
            'resources/files/unrelated.pptx',
        )
        folder = _files(self.media)
        folder.joinpath('unrelated_Abcdef1.pptx').write_bytes(b'one')
        folder.joinpath('unrelated_Zyxwvu2.pptx').write_bytes(b'two')
        self._pin(resource)

        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/account/', resp.url)
        resource.refresh_from_db()
        self.assertEqual(resource.file.name, 'resources/files/unrelated.pptx')

    def test_missing_volume_file_is_served_from_the_bundled_deck(self):
        from apps.resources.resource_files import BUNDLED_DIR
        bundled = (BUNDLED_DIR / 'amaldar_tartibi_ozun_tuz_v2.pptx').read_bytes()
        resource = self._resource(
            'amaldar_tartibi_ozun_tuz.pptx',
            'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx',
        )
        self._pin(resource)

        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b''.join(resp.streaming_content), bundled)
        self.assertTrue(
            (_files(self.media) / 'amaldar_tartibi_ozun_tuz_v2.pptx').read_bytes() == bundled
        )

    def test_repair_pins_the_v2_row_and_leaves_the_current_free_file_alone(self):
        from django.apps import apps
        level = self._resource(
            '4-amal-JenilOrtoOor.pptx',
            'resources/files/4-amal-JenilOrtoOor.pptx',
        )
        lesson = self._resource(
            'amaldar_tartibi_ozun_tuz.pptx',
            'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx',
        )
        self._pin(level)
        repair_four_basic_free_file(apps)
        level.refresh_from_db()
        lesson.refresh_from_db()
        free = PageFreeDownload.objects.get(page_key='four_basic_operations')
        self.assertEqual(level.title, '4-amal-JenilOrtoOor.pptx')
        self.assertEqual(lesson.title, 'amaldar_tartibi_ozun_tuz_v2.pptx')
        self.assertEqual(lesson.file.name, 'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx')
        self.assertTrue((_files(self.media) / 'amaldar_tartibi_ozun_tuz_v2.pptx').is_file())
        self.assertEqual(free.resource_id, lesson.pk)
        self.assertTrue(free.pinned)
