import importlib

import pymupdf
from django.db import migrations
from django.test import SimpleTestCase

from apps.resources.kyrgyz_text import NBSP
from apps.resources.pack_pdf import correct_text, rewrite_pdf, sha256_bytes


class PackPdfTextTests(SimpleTestCase):
    def test_header_keeps_the_topic_and_the_maze_label(self):
        samples = {
            '5-класс ›': ('', 'left'),
            '5-класс › Бурчтар': ('Бурчтар', 'right'),
            '4–5-класс › Амалдардын тартиби': ('Амалдардын тартиби', 'right'),
            '6-класс › Көбөйтүүчүлөр, ЭЧЖБ (§9)': ('Көбөйтүүчүлөр, ЭЧЖБ (§9)', 'right'),
            'БАШТАдан МАРЕге чейин бар.': ('БАШТАдан МАРАга чейин бар.', 'left'),
            '→ МАРЕ': ('→ МАРА', 'left'),
            'Жейилгени?': ('Желгени?', 'left'),
            'жейилди?': ('желди?', 'left'),
            'Адегенде иретте:': ('Адегенде ирээтте:', 'left'),
            'билдирет': ('билдирет', 'left'),
            'кирет': ('кирет', 'left'),
            f'70 × 1000 = 10,000': (f'70 × 1000 = 10{NBSP}000', 'left'),
            '0,768': ('0,768', 'left'),
            '4,3 × 100 = 4,300': ('4,3 × 100 = 4,300', 'left'),
            '2011-стандарт 3.2 (убакыт)': ('2011-стандарт 3.2 (убакыт)', 'left'),
            '(9.1–9.11, № 243–262)': ('(9.1–9.11, № 243–262)', 'left'),
            '7:15тен': ('7:15тен', 'left'),
            '2 °Cга муздайт': ('2 °Сга муздайт', 'left'),
            'Тумарчаны 4 оңго жылдырып, учун башка жакка каратуу': (
                'Тумарчаны 4 оңго жылдырып, учун башка жакка каратуу',
                'left',
            ),
            'окуучунун': ('окуучунун', 'left'),
            'Студенттерге': ('Окуучуларга', 'left'),
            'дукөндөн': ('дүкөндөн', 'left'),
        }
        for old, (new, align) in samples.items():
            updated, _counts, got = correct_text(old)
            self.assertEqual(updated, new, old)
            self.assertEqual(got, align, old)

    def test_rewrite_keeps_the_line_and_is_stable(self):
        font = 'apps/resources/generators/fonts/Inter-Regular.ttf'
        doc = pymupdf.open()
        page = doc.new_page(width=400, height=200)
        page.draw_line((20, 20), (380, 180), color=(0.2, 0.3, 0.4), width=2)
        page.insert_text((40, 40), '5-класс › Бурчтар', fontsize=12, fontfile=font, fontname='inter')
        page.insert_text((40, 80), '→ МАРЕ', fontsize=12, fontfile=font, fontname='inter')
        page.insert_text((40, 120), 'учун', fontsize=12, fontfile=font, fontname='inter')
        original = doc.tobytes()
        doc.close()
        before = pymupdf.open(stream=original, filetype='pdf')
        drawings = len(before[0].get_drawings())
        before.close()

        rewritten, counts = rewrite_pdf(original)
        self.assertGreater(counts['breadcrumb'], 0)
        self.assertGreater(counts['mare'], 0)
        self.assertEqual(counts['breadcrumb'] + counts['mare'], sum(counts.values()))
        opened = pymupdf.open(stream=rewritten, filetype='pdf')
        text = opened[0].get_text()
        self.assertIn('Бурчтар', text)
        self.assertNotIn('класс', text)
        self.assertIn('МАРА', text)
        self.assertNotIn('МАРЕ', text)
        self.assertIn('учун', text)
        self.assertEqual(len(opened[0].get_drawings()), drawings)
        opened.close()

        second, second_counts = rewrite_pdf(rewritten)
        self.assertEqual(second, rewritten)
        self.assertEqual(sum(second_counts.values()), 0)
        self.assertNotEqual(sha256_bytes(rewritten), sha256_bytes(original))


class PackPdfMigrationTests(SimpleTestCase):
    def test_migration_is_data_only(self):
        migration = importlib.import_module('apps.resources.migrations.0051_refresh_pack_pdf')
        self.assertEqual(migration.Migration.dependencies, [('personal', '0050_refresh_kyrgyz_text')])
        self.assertTrue(migration.Migration.atomic)
        self.assertEqual(len(migration.Migration.operations), 1)
        operation = migration.Migration.operations[0]
        self.assertIsInstance(operation, migrations.RunPython)
        self.assertIs(operation.code, migration.forward)
        self.assertIs(operation.reverse_code, migration.backward)
        for item in migration.Migration.operations:
            self.assertNotIsInstance(item, migrations.AlterField)
            self.assertNotIsInstance(item, migrations.AddConstraint)

    def test_committed_bytes_match_the_new_hash(self):
        from pathlib import Path
        import json
        path = Path(__file__).resolve().parent / 'data' / 'pack_pdf_manifest.json'
        manifest = json.loads(path.read_text(encoding='utf-8'))
        finish = json.loads((path.parent / 'finish_word_manifest.json').read_text(encoding='utf-8'))
        self.assertGreater(len(manifest), 0)
        root = Path(__file__).resolve().parents[2]
        for relative, entry in manifest.items():
            self.assertEqual(entry['fixes'], ['kyrgyz'])
            self.assertNotEqual(entry['old'], entry['new'])
            bundled = root / 'apps' / 'resources' / 'bundled_files' / Path(relative).name
            media = root / 'media' / relative
            self.assertTrue(bundled.is_file(), relative)
            digest = sha256_bytes(bundled.read_bytes())
            # 0053 rewrites the maze label again. Its old hash is this new hash.
            if relative in finish:
                self.assertEqual(finish[relative]['old'], entry['new'], relative)
                self.assertEqual(digest, finish[relative]['new'], relative)
            else:
                self.assertEqual(digest, entry['new'], relative)
            if media.is_file():
                self.assertEqual(sha256_bytes(media.read_bytes()), digest, relative)
