import importlib
import io
import shutil
import tempfile
import zipfile
from pathlib import Path

from django.db import migrations
from django.test import SimpleTestCase, override_settings

from apps.resources.deck_text import (
    ENGLISH_REPLACEMENTS,
    TYPO_NEW,
    TYPO_OLD,
    edit_runs,
    load_manifest,
    refresh_media,
    refresh_one,
    rewrite_pptx,
    sha256_bytes,
)


def _pptx(parts):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as archive:
        for name, payload in parts.items():
            if name.startswith('ppt/media/'):
                archive.writestr(name, payload, compress_type=zipfile.ZIP_STORED)
            else:
                archive.writestr(name, payload)
    return buffer.getvalue()


_SLIDE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:sp><p:txBody>
      <a:p><a:r><a:t>{typo}</a:t></a:r></a:p>
      <a:p><a:r><a:t>Тур</a:t></a:r><a:r><a:t>дуу пикирлер </a:t></a:r><a:r><a:t>учун ыраазычылык</a:t></a:r></a:p>
      <a:p><a:r><a:t>Answer</a:t></a:r><a:r><a:t>6-класс ›</a:t></a:r></a:p>
      <a:p><a:r><a:t>1-класс › 10 ичинде кошуу</a:t></a:r></a:p>
      <a:p><a:r><a:t>1-кадамдуу теңдемелер  ·  7–8-класс</a:t></a:r></a:p>
      <a:p><a:r><a:t>Аралаш кайталоо - 5-6-класс</a:t></a:r></a:p>
      <a:p><a:r><a:t>6-класс · Математика</a:t></a:r></a:p>
      <a:p><a:r><a:t>5-класстын китеби</a:t></a:r></a:p>
      <a:p><a:r><a:t>6-класс тегерек гүлзар жасайт.</a:t></a:r></a:p>
      <a:p><a:r><a:t>Китеп: 6-класс: «Пайыз»; Cambridge Stage 6. Даярдык.</a:t></a:r></a:p>
      <a:p><a:r><a:t>2-класс (Cambridge 2): фигуралар</a:t></a:r></a:p>
      <a:p><a:r><a:t>катыш (Cambridge Stage 6, улуттук B)</a:t></a:r></a:p>
      <a:p><a:r><a:t>12 + 7 = 19</a:t></a:r></a:p>
      <a:p><a:r><a:t>Click to edit Master title style</a:t></a:r></a:p>
      <a:p><a:r><a:t>Jander</a:t></a:r></a:p>
      <a:p><a:r><a:t>Answer &amp; next</a:t></a:r></a:p>
    </p:txBody></p:sp>
  </p:spTree></p:cSld>
</p:sld>
"""

_CHART = '<c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:v>5-класс</c:v><c:v>42</c:v></c:chart>'
_CORE = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<cp:coreProperties xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties">'
    f'<dc:title>{TYPO_OLD}</dc:title></cp:coreProperties>'
)


def _sample():
    return _pptx({
        'ppt/slides/slide1.xml': _SLIDE.format(typo=TYPO_OLD + ' ыраазычылык билдиребиз.').encode('utf-8'),
        'ppt/charts/chart1.xml': _CHART.encode('utf-8'),
        'ppt/media/image1.png': b'\x89PNG-fake-bytes',
        'docProps/core.xml': _CORE.encode('utf-8'),
    })


def _texts(data):
    found = []
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        xml = archive.read('ppt/slides/slide1.xml').decode('utf-8')
    for match in __import__('re').finditer(r'<a:t>(.*?)</a:t>', xml):
        found.append(match.group(1))
    return found


class DeckTextEditTests(SimpleTestCase):
    def test_phrase_split_across_runs_keeps_the_tail(self):
        updated, counts = edit_runs(
            ['Тур', 'дуу пикирлер ', 'учун ыраазычылык'],
            typo=True,
        )
        self.assertEqual(updated, [TYPO_NEW, '', ' ыраазычылык'])
        self.assertEqual(counts['typo'], 1)
        again, again_counts = edit_runs(updated, typo=True)
        self.assertEqual(again, updated)
        self.assertEqual(again_counts['typo'], 0)

    def test_package_edits_text_only(self):
        original = _sample()
        rewritten, counts = rewrite_pptx(original, typo=True, grade=True, english=True)
        self.assertGreater(counts['typo'], 0)
        self.assertGreater(counts['grade'], 0)
        self.assertEqual(counts['english'], 1)
        texts = _texts(rewritten)
        self.assertIn(TYPO_NEW + ' ыраазычылык билдиребиз.', texts)
        self.assertIn(TYPO_NEW, texts)
        self.assertIn(' ыраазычылык', texts)
        self.assertIn('Жооп', texts)
        self.assertNotIn('Answer', texts)
        self.assertIn('10 ичинде кошуу', texts)
        self.assertIn('1-кадамдуу теңдемелер', texts)
        self.assertIn('Аралаш кайталоо', texts)
        self.assertNotIn('6-класс ›', texts)
        self.assertNotIn('6-класс · Математика', texts)
        self.assertIn('5-класстын китеби', texts)
        self.assertIn('6-класс тегерек гүлзар жасайт.', texts)
        self.assertIn('Китеп: 6-класс: «Пайыз». Даярдык.', texts)
        self.assertNotIn('Cambridge Stage 6', ''.join(texts))
        self.assertIn(
            'Китеп: 6-класс: «Статистика» (маалымат).',
            edit_runs(
                ['Китеп: 6-класс: «Статистика»; Cambridge Primary 6 (маалымат).'],
                grade=True,
            )[0],
        )
        self.assertIn('2-класс: фигуралар', texts)
        self.assertIn('катыш (улуттук B)', texts)
        self.assertIn('12 + 7 = 19', texts)
        self.assertIn('Click to edit Master title style', texts)
        self.assertIn('Jander', texts)
        self.assertIn('Answer &amp; next', texts)
        with zipfile.ZipFile(io.BytesIO(original)) as old, zipfile.ZipFile(io.BytesIO(rewritten)) as new:
            self.assertEqual(old.namelist(), new.namelist())
            self.assertEqual(old.read('ppt/media/image1.png'), new.read('ppt/media/image1.png'))
            self.assertEqual(old.read('ppt/charts/chart1.xml'), new.read('ppt/charts/chart1.xml'))
            self.assertIn(TYPO_NEW, new.read('docProps/core.xml').decode('utf-8'))
        second, second_counts = rewrite_pptx(rewritten, typo=True, grade=True, english=True)
        self.assertEqual(second, rewritten)
        self.assertEqual(second_counts, {'typo': 0, 'grade': 0, 'english': 0})

    def test_flags_limit_which_fix_runs(self):
        original = _sample()
        rewritten, counts = rewrite_pptx(original, typo=True)
        self.assertEqual(counts['english'], 0)
        self.assertEqual(counts['grade'], 0)
        self.assertIn('Answer', _texts(rewritten))
        self.assertIn('6-класс ›', _texts(rewritten))
        self.assertNotIn(TYPO_OLD, ''.join(_texts(rewritten)))

    def test_english_map_is_the_approved_ui_only(self):
        self.assertEqual(ENGLISH_REPLACEMENTS['Answer'], 'Жооп')
        self.assertEqual(ENGLISH_REPLACEMENTS['START'], 'Башта')
        self.assertEqual(ENGLISH_REPLACEMENTS['Questions?'], 'Суроолор?')
        for source, target in ENGLISH_REPLACEMENTS.items():
            self.assertTrue(any(ord(char) > 127 for char in target), target)
            self.assertNotIn(source, target)


class DeckRefreshTests(SimpleTestCase):
    def test_refresh_writes_only_the_old_hash(self):
        original = _sample()
        rewritten, _counts = rewrite_pptx(original, typo=True, grade=True, english=True)
        entry = {
            'old': sha256_bytes(original),
            'new': sha256_bytes(rewritten),
            'fixes': ['typo', 'grade', 'english'],
        }
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        path = root / 'resources' / 'files' / 'sample.pptx'
        path.parent.mkdir(parents=True)
        path.write_bytes(original)

        self.assertEqual(refresh_one(path, entry), 'updated')
        self.assertEqual(path.read_bytes(), rewritten)
        self.assertEqual(refresh_one(path, entry), 'already')

        path.write_bytes(b'PK-admin-edit')
        self.assertEqual(refresh_one(path, entry), 'foreign')
        self.assertEqual(path.read_bytes(), b'PK-admin-edit')

        missing = root / 'resources' / 'files' / 'absent.pptx'
        self.assertEqual(refresh_one(missing, entry), 'missing')
        self.assertFalse(missing.exists())

        path.write_bytes(original)
        entry['new'] = '0' * 64
        self.assertEqual(refresh_one(path, entry), 'rejected')
        self.assertEqual(path.read_bytes(), original)

    def test_refresh_media_skips_files_that_are_not_on_disk(self):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        with override_settings():
            totals = refresh_media(root)
        self.assertGreater(totals['missing'], 0)
        self.assertEqual(totals['updated'], 0)
        self.assertEqual(list(root.rglob('*')), [])


class DeckManifestTests(SimpleTestCase):
    def test_migration_is_data_only(self):
        migration = importlib.import_module('apps.resources.migrations.0049_refresh_deck_text')
        self.assertEqual(migration.Migration.dependencies, [('personal', '0048_wave8_packs')])
        self.assertTrue(migration.Migration.atomic)
        self.assertEqual(len(migration.Migration.operations), 1)
        operation = migration.Migration.operations[0]
        self.assertIsInstance(operation, migrations.RunPython)
        self.assertIs(operation.code, migration.forward)
        self.assertIs(operation.reverse_code, migration.backward)

    def test_committed_decks_match_the_new_hash(self):
        manifest = load_manifest()
        root = Path(__file__).resolve().parents[2]
        fixes = {'typo': 0, 'grade': 0, 'english': 0}
        for entry in manifest.values():
            for name in entry['fixes']:
                fixes[name] += 1
        self.assertEqual(fixes['typo'], 618)
        self.assertEqual(fixes['grade'], 150)
        self.assertEqual(fixes['english'], 20)
        self.assertEqual(len(manifest), 770)
        for relative, entry in manifest.items():
            copies = []
            media = root / 'media' / relative
            bundled = root / 'apps' / 'resources' / 'bundled_files' / Path(relative).name
            if media.is_file():
                copies.append(media)
            if bundled.is_file():
                copies.append(bundled)
            self.assertTrue(copies, relative)
            for copy in copies:
                self.assertEqual(sha256_bytes(copy.read_bytes()), entry['new'], relative)
            self.assertNotEqual(entry['old'], entry['new'])
