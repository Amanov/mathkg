import importlib
import io
import json
import zipfile
from pathlib import Path

import pymupdf
from django.db import migrations
from django.test import SimpleTestCase
from PIL import Image, ImageChops, ImageStat

from apps.resources.finish_word import (
    replace_finish,
    rewrite_pdf,
    rewrite_pptx,
    sha256_bytes,
)
from apps.resources.previews import render_pdf_preview


class FinishWordTests(SimpleTestCase):
    def test_whole_word_only(self):
        samples = {
            '→ МАРА': '→ МААРА',
            'БАШТАдан МАРАга чейин': 'БАШТАдан МААРАга чейин',
            'МАРЕ': 'МААРА',
            'МАРЕге': 'МААРАга',
            'мара': 'маара',
            'Мара': 'Маара',
            'мараттык': 'мараттык',
            'МААРА': 'МААРА',
            'МААРАга': 'МААРАга',
        }
        for old, new in samples.items():
            updated, _counts = replace_finish(old)
            self.assertEqual(updated, new, old)
        _text, counts = replace_finish('→ МАРА жана МАРАга, калган МАРЕ.')
        self.assertEqual(counts['mara'], 1)
        self.assertEqual(counts['maraga'], 1)
        self.assertEqual(counts['mare'], 1)

    def test_pdf_label_grows_in_place_and_stays(self):
        font = 'apps/resources/generators/fonts/Inter-Regular.ttf'
        doc = pymupdf.open()
        page = doc.new_page(width=400, height=200)
        page.draw_line((20, 20), (380, 180), color=(0.2, 0.3, 0.4), width=2)
        page.insert_text((40, 80), '→ МАРА', fontsize=12, fontfile=font, fontname='inter')
        page.insert_text((40, 120), 'мараттык', fontsize=12, fontfile=font, fontname='inter')
        original = doc.tobytes()
        doc.close()
        before = pymupdf.open(stream=original, filetype='pdf')
        drawings = len(before[0].get_drawings())
        before.close()

        rewritten, counts = rewrite_pdf(original)
        self.assertEqual(counts['mara'], 1)
        self.assertEqual(sum(counts.values()), 1)
        opened = pymupdf.open(stream=rewritten, filetype='pdf')
        text = opened[0].get_text()
        self.assertIn('МААРА', text)
        self.assertNotIn('МАРА', text.replace('МААРА', ''))
        self.assertIn('мараттык', text)
        self.assertEqual(len(opened[0].get_drawings()), drawings)
        opened.close()
        second, second_counts = rewrite_pdf(rewritten)
        self.assertEqual(second, rewritten)
        self.assertEqual(sum(second_counts.values()), 0)

    def test_pptx_run_is_replaced(self):
        xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:sp><p:txBody><a:p><a:r><a:t>→ МАРА</a:t></a:r></a:p></p:txBody></p:sp>'
            '</p:sld>'
        )
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as archive:
            archive.writestr('ppt/slides/slide1.xml', xml)
            archive.writestr('[Content_Types].xml', '<Types/>')
        rewritten, counts = rewrite_pptx(buf.getvalue())
        self.assertEqual(counts['mara'], 1)
        with zipfile.ZipFile(io.BytesIO(rewritten)) as archive:
            self.assertIn('МААРА', archive.read('ppt/slides/slide1.xml').decode('utf-8'))
            self.assertEqual(archive.read('[Content_Types].xml'), b'<Types/>')


class FinishWordMigrationTests(SimpleTestCase):
    def test_migration_follows_0051_and_is_data_only(self):
        migration = importlib.import_module('apps.resources.migrations.0053_refresh_finish_word')
        self.assertEqual(
            migration.Migration.dependencies,
            [('personal', '0051_refresh_pack_pdf')],
        )
        self.assertTrue(migration.Migration.atomic)
        self.assertEqual(len(migration.Migration.operations), 1)
        operation = migration.Migration.operations[0]
        self.assertIsInstance(operation, migrations.RunPython)
        self.assertIs(operation.code, migration.forward)
        for item in migration.Migration.operations:
            self.assertNotIsInstance(item, migrations.AlterField)
            self.assertNotIsInstance(item, migrations.AddConstraint)

    def test_committed_pdfs_match_the_new_hash(self):
        path = Path(__file__).resolve().parent / 'data' / 'finish_word_manifest.json'
        manifest = json.loads(path.read_text(encoding='utf-8'))
        self.assertGreater(len(manifest), 0)
        root = Path(__file__).resolve().parents[2]
        for relative, entry in manifest.items():
            self.assertEqual(entry['fixes'], ['finish'])
            self.assertNotEqual(entry['old'], entry['new'])
            bundled = root / 'apps' / 'resources' / 'bundled_files' / Path(relative).name
            self.assertTrue(bundled.is_file(), relative)
            self.assertEqual(sha256_bytes(bundled.read_bytes()), entry['new'], relative)
            media = root / 'media' / relative
            if media.is_file():
                self.assertEqual(sha256_bytes(media.read_bytes()), entry['new'], relative)

    def test_maze_thumbnail_matches_the_pdf(self):
        root = Path(__file__).resolve().parents[2]
        pdf = root / 'apps/resources/bundled_files/6-klass-bolunuu-belgileri-labirint-v2.pdf'
        thumb = root / 'static/img/topic-pages/6-klass-bolunuu-belgileri-labirint-v2.webp'
        rendered = Image.open(io.BytesIO(render_pdf_preview(pdf.read_bytes())))
        saved = Image.open(thumb)
        self.assertEqual(rendered.size, saved.size)
        diff = ImageChops.difference(rendered, saved)
        mean = sum(ImageStat.Stat(diff).mean) / 3
        self.assertLess(mean, 2)


class OtherPreviewTests(SimpleTestCase):
    def test_unchanged_print_thumbnail_still_matches_page_one(self):
        root = Path(__file__).resolve().parents[2]
        pdf = root / 'apps/resources/bundled_files/koshuu-1-digit-print.pdf'
        thumb = root / 'static/img/topic-pages/koshuu-1-digit-print.webp'
        rendered = Image.open(io.BytesIO(render_pdf_preview(pdf.read_bytes()))).convert('RGB')
        saved = Image.open(thumb).convert('RGB')
        self.assertEqual(rendered.size, saved.size)
        diff = ImageChops.difference(rendered, saved)
        mean = sum(ImageStat.Stat(diff).mean) / 3
        # This sheet was not rewritten. The stored preview is the same page;
        # a fresh draw is not pixel-identical to the original export.
        self.assertLess(mean, 8)
