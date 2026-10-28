import importlib
import io
import json
import zipfile
from pathlib import Path

from django.db import migrations
from django.test import SimpleTestCase

from apps.resources.deck_text import rewrite_pptx, sha256_bytes
from apps.resources.kyrgyz_text import (
    NBSP,
    SENTENCE_REWRITES,
    _FOREIGN,
    _PROVEN,
    apply_kyrgyz_runs,
    collect_proven,
)


def _joined(texts):
    updated, _counts = apply_kyrgyz_runs(texts)
    return ''.join(updated), updated


class KyrgyzRunTests(SimpleTestCase):
    def test_phrase_split_across_runs(self):
        joined, runs = _joined(['Баар', 'дык у', 'чун рахмат'])
        self.assertEqual(joined, 'Бардык үчүн рахмат')
        self.assertEqual(len(runs), 3)
        self.assertEqual(apply_kyrgyz_runs(runs)[0], runs)

    def test_safe_pairs_and_draw_only(self):
        samples = {
            'кайсы жана клей жок': 'кайчы жана клей жок',
            'даярдаоган': 'даярдалган',
            'жазып корсото алышат': 'жазып көрсөтө алышат',
            'өз дептерге': 'өз дептерине',
            'өз топторго': 'өз топторуна',
            'Cумманы толтур': 'Сумманы толтур',
            '3 × dдан': '3 × ддан',
            'ат салышатю': 'ат салышат.',
            'канча жолу көбөйтүүбүз керек?': 'канча жолу көбөйтөбүз?',
            'канча жолу бөлүшүбүз керек?': 'канча жолу бөлөбүз?',
            'Торт амал': 'Төрт амал',
            'Эгер бул тен болсо': 'Эгер бул тең болсо',
            '5тен сана': '5тен сана',
            '7:15тен 8:00гө': '7:15тен 8:00гө',
            'тендеме': 'тендеме',
            'билдирет': 'билдирет',
            'кирет': 'кирет',
            'Жейилген бөлүгү': 'Желген бөлүгү',
            '3ү жейилди': '3ү желди',
            'Устунку картаны караныз': 'Үстүнкү картаны караңыз',
            'Арзан дукөндөн': 'Арзан дүкөндөн',
            'көбурөөк': 'көбүрөөк',
            'бөлчөгу': 'бөлчөгү',
            'Кондум баракчасы': 'Көндүм баракчасы',
            'кемитүүдон': 'кемитүүдөн',
            'коебуз': 'коёбуз',
            'бурч чоңоет': 'бурч чоңоёт',
            'Баарыңызга ырахмат!': 'Баарыңызга рахмат!',
            'Ар кандай пикир ыраазычылык билдиребиз.':
                'Ар кандай пикир үчүн ыраазычылык билдиребиз.',
            'ордуна , окуучулар': 'ордуна, окуучулар',
            'Бинго ,жооптору': 'Бинго,жооптору',
        }
        for old, new in samples.items():
            self.assertEqual(_joined([old])[0], new, old)

    def test_numbers_keep_decimal_commas_and_fix_thousands(self):
        self.assertEqual(_joined(['0,768'])[0], '0,768')
        self.assertEqual(_joined(['2,349 ≈ ? (жүздөн бирге)'])[0], '2,349 ≈ ? (жүздөн бирге)')
        self.assertEqual(_joined(['1,1;  1,01;  1,11;  1,001'])[0], '1,1;  1,01;  1,11;  1,001')
        self.assertEqual(_joined(['70 × 1000 = 70,000'])[0], f'70 × 1000 = 70{NBSP}000')
        self.assertEqual(_joined(['0.07 × 10,000'])[0], f'0,07 × 10{NBSP}000')
        self.assertEqual(_joined(['51,052.91'])[0], f'51{NBSP}052,91')
        self.assertEqual(_joined(['0.5'])[0], '0,5')
        self.assertEqual(
            _joined(['(9.1–9.11, № 243–262)'])[0],
            '(9.1–9.11, № 243–262)',
        )
        self.assertEqual(
            _joined(['2011-стандарт 3.2 (убакыттын чен бирдиктери)'])[0],
            '2011-стандарт 3.2 (убакыттын чен бирдиктери)',
        )
        self.assertEqual(_joined(['саатына 8.50$'])[0], 'саатына 8,50$')
        self.assertEqual(_joined(['6.5 саат'])[0], '6,5 саат')
        self.assertEqual(_joined(['33 000 ÷ 12 = 2,750 сом'])[0], f'33 000 ÷ 12 = 2{NBSP}750 сом')
        self.assertEqual(
            _joined(['48821 – 9999 депозит = 38,822 сом'])[0],
            f'48821 – 9999 депозит = 38{NBSP}822 сом',
        )
        self.assertIn(
            f'47{NBSP}713',
            _joined(['47,713 + 7% пайыз= 51,052.91'])[0],
        )
        money = [
            'Жалпы төлөм = 24 × 1664 = 39,936',
            'Пайыз = 39,936  – 33,281  = 6,655',
            'Насыя = 35500  – 2219 = 33,281 сом',
        ]
        token = _PROVEN.set(collect_proven(money))
        try:
            self.assertIn(f'39{NBSP}936', _joined([money[1]])[0])
            self.assertIn(f'33{NBSP}281', _joined([money[1]])[0])
            self.assertIn(f'6{NBSP}655', _joined([money[1]])[0])
        finally:
            _PROVEN.reset(token)

    def test_iret_and_student_case(self):
        self.assertEqual(_joined(['иреттөө'])[0], 'ирээттөө')
        self.assertEqual(_joined(['Иретте'])[0], 'Ирээтте')
        self.assertEqual(_joined(['иретинде'])[0], 'ирээтинде')
        self.assertEqual(_joined(['иреттеңиз'])[0], 'ирээттеңиз')
        self.assertEqual(_joined(['иреттээлген'])[0], 'ирээттелген')
        self.assertEqual(_joined(['Студенттерге'])[0], 'Окуучуларга')
        self.assertEqual(_joined(['студенттер'])[0], 'окуучулар')
        self.assertEqual(_joined(['студенттен'])[0], 'окуучудан')
        self.assertEqual(_joined(['студентке'])[0], 'окуучуга')
        self.assertEqual(_joined(['Полли ар бир студентке '])[0], 'Полли ар бир окуучуга ')

    def test_rewrites_stay_short_and_kyrgyz(self):
        for old, new in SENTENCE_REWRITES.items():
            self.assertLessEqual(len(new), len(old) + 12, old[:40])
            self.assertIsNone(_FOREIGN.search(new), new)
            self.assertNotIn('студент', new.lower())
            self.assertEqual(_joined([old])[0], new)

    def test_package_keeps_chart_and_is_stable(self):
        slide = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:sp><p:txBody>
    <a:p><a:r><a:t>0.5</a:t></a:r><a:r><a:t> жана </a:t></a:r><a:r><a:t>70,000</a:t></a:r></a:p>
    <a:p><a:r><a:t>билдирет</a:t></a:r></a:p>
  </p:txBody></p:sp></p:spTree></p:cSld>
</p:sld>
"""
        chart = '<c:v>0.5</c:v><c:v>70,000</c:v>'
        core = (
            '<?xml version="1.0"?><cp:coreProperties xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties">'
            '<dc:title>иреттөө</dc:title></cp:coreProperties>'
        )
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('ppt/slides/slide1.xml', slide.encode())
            archive.writestr('ppt/charts/chart1.xml', chart.encode())
            archive.writestr('ppt/media/image1.png', b'\x89PNG')
            archive.writestr('docProps/core.xml', core.encode())
        rewritten, counts = rewrite_pptx(buffer.getvalue(), kyrgyz=True)
        self.assertGreater(counts['kyrgyz'], 0)
        with zipfile.ZipFile(io.BytesIO(rewritten)) as archive:
            xml = archive.read('ppt/slides/slide1.xml').decode()
            self.assertIn(f'70{NBSP}000', xml)
            self.assertIn('0,5', xml)
            self.assertIn('билдирет', xml)
            self.assertEqual(archive.read('ppt/charts/chart1.xml').decode(), chart)
            self.assertEqual(archive.read('ppt/media/image1.png'), b'\x89PNG')
            self.assertIn('иреттөө', archive.read('docProps/core.xml').decode())
            self.assertEqual(archive.namelist(), [
                'ppt/slides/slide1.xml', 'ppt/charts/chart1.xml',
                'ppt/media/image1.png', 'docProps/core.xml',
            ])
        second, second_counts = rewrite_pptx(rewritten, kyrgyz=True)
        self.assertEqual(second, rewritten)
        self.assertEqual(second_counts['kyrgyz'], 0)


class KyrgyzManifestTests(SimpleTestCase):
    def test_committed_bytes_match_the_new_hash(self):
        path = Path(__file__).resolve().parent / 'data' / 'deck_kyrgyz_manifest.json'
        manifest = json.loads(path.read_text(encoding='utf-8'))
        self.assertGreater(len(manifest), 0)
        root = Path(__file__).resolve().parents[2]
        for relative, entry in manifest.items():
            self.assertEqual(entry['fixes'], ['kyrgyz'])
            self.assertNotEqual(entry['old'], entry['new'])
            copies = []
            media = root / 'media' / relative
            bundled = root / 'apps' / 'resources' / 'bundled_files' / Path(relative).name
            if media.is_file():
                copies.append(media)
            if bundled.is_file():
                copies.append(bundled)
            if not copies:
                # media/ is gitignored. A bundled copy is checked when present.
                continue
            for copy in copies:
                self.assertEqual(sha256_bytes(copy.read_bytes()), entry['new'], relative)


class KyrgyzMigrationTests(SimpleTestCase):
    def test_migration_is_data_only(self):
        migration = importlib.import_module('apps.resources.migrations.0050_refresh_kyrgyz_text')
        self.assertEqual(migration.Migration.dependencies, [('personal', '0049_refresh_deck_text')])
        self.assertTrue(migration.Migration.atomic)
        self.assertEqual(len(migration.Migration.operations), 1)
        operation = migration.Migration.operations[0]
        self.assertIsInstance(operation, migrations.RunPython)
        self.assertIs(operation.code, migration.forward)
        self.assertIs(operation.reverse_code, migration.backward)
        for item in migration.Migration.operations:
            self.assertNotIsInstance(item, migrations.AlterField)
            self.assertNotIsInstance(item, migrations.AddConstraint)
