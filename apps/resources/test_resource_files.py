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

    def test_two_collision_suffixes_stay_unavailable(self):
        resource = self._resource(
            'amaldar_tartibi_ozun_tuz_v2.pptx',
            'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx',
        )
        folder = _files(self.media)
        folder.joinpath('amaldar_tartibi_ozun_tuz_v2_Abcdef1.pptx').write_bytes(b'one')
        folder.joinpath('amaldar_tartibi_ozun_tuz_v2_Zyxwvu2.pptx').write_bytes(b'two')
        self._pin(resource)

        resp = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/account/', resp.url)
        resource.refresh_from_db()
        self.assertEqual(resource.file.name, 'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx')

    def test_repair_points_the_free_row_at_an_existing_file_and_leaves_a_missing_one(self):
        from django.apps import apps
        present = self._resource('old-name.pptx', 'resources/files/old-name.pptx')
        absent = self._resource('other.pptx', 'resources/files/other.pptx')
        _files(self.media).joinpath('amaldar_tartibi_ozun_tuz_v2.pptx').write_bytes(b'there')
        self._pin(present)
        changed = repair_four_basic_free_file(apps)
        present.refresh_from_db()
        self.assertEqual(present.title, 'amaldar_tartibi_ozun_tuz_v2.pptx')
        self.assertEqual(present.file.name, 'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx')
        self.assertEqual(changed, ['title', 'file'])

        PageFreeDownload.objects.filter(page_key='four_basic_operations').update(resource=absent)
        absent_changed = repair_four_basic_free_file(apps)
        absent.refresh_from_db()
        self.assertEqual(absent_changed, [])
        self.assertEqual(absent.title, 'other.pptx')
        self.assertEqual(absent.file.name, 'resources/files/other.pptx')

    def test_repair_does_not_take_a_title_another_row_already_has(self):
        from django.apps import apps
        holder = self._resource(
            'amaldar_tartibi_ozun_tuz_v2.pptx',
            'resources/files/amaldar_tartibi_ozun_tuz_v2.pptx',
            b'kept',
        )
        # The bytes for the holder's stored name were never written; write them.
        _files(self.media).joinpath('amaldar_tartibi_ozun_tuz_v2.pptx').write_bytes(b'kept')
        other = self._resource('4-amal-1234.pptx', 'resources/files/4-amal-1234.pptx')
        self._pin(other)
        changed = repair_four_basic_free_file(apps)
        other.refresh_from_db()
        holder.refresh_from_db()
        self.assertEqual(changed, [])
        self.assertEqual(other.title, '4-amal-1234.pptx')
        self.assertEqual(holder.title, 'amaldar_tartibi_ozun_tuz_v2.pptx')
