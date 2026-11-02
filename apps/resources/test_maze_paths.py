"""Each maze has its own route, and the finish word is «МААРА»."""

import zipfile

import pymupdf
from django.test import SimpleTestCase

from apps.resources.generators.maze_build import maze_pdfs
from apps.resources.generators.maze_path import (
    SHARED_AVOID,
    assign_routes,
    format_kyrgyz_number,
    is_single_route,
)
from apps.resources.generators.maze_sheet import maze_key, painted_mask

BUNDLED_PARENT_SKIP = ('stat-Labirint-A4.pdf', 'stat-Labirint-2bet-A4.pdf')


def _visible_routes():
    found = {}
    for path in maze_pdfs():
        doc = pymupdf.open(path)
        try:
            best = None
            for page in doc:
                mask = painted_mask(page)
                if mask and (best is None or len(mask[2]) > len(best[2])):
                    best = mask
            if best is None:
                continue
            rows, cols, green = best
            found[maze_key(path.name)] = (path.name, rows, cols, green)
        finally:
            doc.close()
    return found


def _specs_from_visible(routes):
    specs = []
    for key, (_name, rows, cols, green) in sorted(routes.items()):
        allowed = ('top', 'bottom') if key in ('1-klass-koshuu-labirint-v4', 'stat-Labirint') else ('left', 'right')
        cells = tuple((index // cols, index % cols) for index in range(len(green)))
        specs.append((key, rows, cols, cells, allowed))
    return specs


class MazePathTests(SimpleTestCase):
    def test_every_maze_has_its_own_single_route(self):
        routes = _visible_routes()
        self.assertGreaterEqual(len(routes), 70)
        masks = []
        for key, (name, rows, cols, green) in routes.items():
            self.assertTrue(is_single_route(green, rows, cols), name)
            self.assertNotIn(green, SHARED_AVOID, name)
            self.assertGreaterEqual(len(green), 8, name)
            masks.append(green)
        self.assertEqual(len(masks), len(set(masks)))
        placed = assign_routes(_specs_from_visible(routes))
        for key, (_name, _rows, _cols, green) in routes.items():
            self.assertEqual(placed[key].path.mask, green, key)

    def test_the_same_seed_rebuilds_the_same_route(self):
        routes = _visible_routes()
        specs = _specs_from_visible(routes)
        first = assign_routes(specs)
        second = assign_routes(list(reversed(specs)))
        for key, placement in first.items():
            self.assertEqual(second[key].path.cells, placement.path.cells)

    def test_kyrgyz_number_formatting(self):
        self.assertEqual(format_kyrgyz_number(1000), '1 000')
        self.assertEqual(format_kyrgyz_number(12500), '12 500')
        self.assertEqual(format_kyrgyz_number(1.5), '1,5')
        self.assertEqual(format_kyrgyz_number(-2.25), '-2,25')

    def test_finish_word_is_maara_in_every_maze_file(self):
        root = maze_pdfs()[0].parent
        offenders = []
        for path in root.iterdir():
            if not path.is_file():
                continue
            lowered = path.name.lower()
            if 'labirint' not in lowered:
                continue
            if path.suffix.lower() == '.pdf':
                doc = pymupdf.open(path)
                try:
                    text = ''.join(page.get_text() for page in doc)
                finally:
                    doc.close()
            elif path.suffix.lower() == '.pptx':
                with zipfile.ZipFile(path) as archive:
                    text = ''.join(
                        archive.read(name).decode('utf-8', errors='ignore')
                        for name in archive.namelist()
                        if name.endswith('.xml')
                    )
            else:
                continue
            if 'МАРЕ' in text:
                offenders.append(path.name)
        self.assertEqual(offenders, [])

    def test_worksheet_and_answer_keep_the_same_statements(self):
        path = maze_pdfs()[0].parent / '6-klass-kvadrat-kub-daraja-labirint.pdf'
        doc = pymupdf.open(path)
        try:
            question = doc[0].get_text()
            answer = doc[1].get_text()
        finally:
            doc.close()
        for token in ('3² = 9', '10³ = 1 000', '∛27 = 3', 'МААРА'):
            self.assertIn(token, question)
            self.assertIn(token, answer)
        self.assertNotIn('МАРЕ', question)
        self.assertNotIn('МАРЕ', answer)
