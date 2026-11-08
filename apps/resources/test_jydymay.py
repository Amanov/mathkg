"""«Атышуу» was renamed to «Жыдымай» everywhere a teacher sees it."""

import importlib
import zipfile
from pathlib import Path

from django.apps import apps as django_apps
from django.test import SimpleTestCase, TestCase

from apps.resources.models import Resource

BUNDLED = Path(__file__).resolve().parent / 'bundled_files'
STATIC_IMG = Path(__file__).resolve().parents[2] / 'static'


class JydymayFilesTests(SimpleTestCase):
    def test_no_deck_or_thumbnail_keeps_the_old_name(self):
        self.assertFalse([p.name for p in BUNDLED.glob('*atyshuu*')])
        self.assertFalse([str(p) for p in STATIC_IMG.rglob('*atyshuu*')])

    def test_every_game_deck_says_jydymay(self):
        decks = sorted(BUNDLED.glob('*-oyun-jydymay*.pptx'))
        self.assertEqual(len(decks), 91)
        for deck in decks:
            with zipfile.ZipFile(deck) as archive:
                text = b''.join(
                    archive.read(name) for name in archive.namelist() if name.endswith('.xml')
                ).decode('utf-8')
            self.assertIn('Жыдымай', text, deck.name)
            self.assertNotIn('Атышуу', text, deck.name)


class JydymayMigrationTests(TestCase):
    def test_rows_point_at_the_new_files(self):
        migration = importlib.import_module('apps.resources.migrations.0082_rename_atyshuu_to_jydymay')
        Resource.objects.create(
            title='9-klass-x-oyun-atyshuu.pptx',
            file='resources/files/9-klass-x-oyun-atyshuu.pptx',
            category='activity', is_active=True,
        )
        migration.forward(django_apps, None)
        row = Resource.objects.get(title='9-klass-x-oyun-jydymay.pptx')
        self.assertEqual(row.file.name, 'resources/files/9-klass-x-oyun-jydymay.pptx')
        self.assertEqual(list(Resource.objects.filter(title__contains='atyshuu', is_active=True).values_list('title', 'file')), [])
