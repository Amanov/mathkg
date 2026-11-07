"""Rebuild every MathKG maze worksheet so the correct route is not shared.

The statistics pair (worksheet, answer key, two-up sheet, slide deck) shares
one route. Every other PDF is its own maze. Legacy «БАШТА / АЯГЫ» snakes are
listed by ``inventory`` and are not this template.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pymupdf

from apps.resources.generators.maze_path import Placement, allowed_label_sides, assign_routes
from apps.resources.generators.maze_sheet import (
    answer_grid,
    load_structure,
    maze_key,
    rebuild_pdf,
    true_cells,
)

BUNDLED = Path(__file__).resolve().parents[1] / 'bundled_files'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def maze_pdfs(root: Path | None = None) -> list[Path]:
    folder = root or BUNDLED
    found = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        lowered = path.name.lower()
        if 'labirint' not in lowered:
            continue
        if path.suffix.lower() != '.pdf':
            continue
        if path.name.startswith('stat-Labirint-2bet'):
            continue
        found.append(path)
    return found


def _margins(page, grid):
    cells = [cell.rect for row in grid.cells for cell in row]
    left = min(rect.x0 for rect in cells)
    right = page.width - max(rect.x1 for rect in cells)
    top = min(rect.y0 for rect in cells)
    bottom = page.height - max(rect.y1 for rect in cells)
    return allowed_label_sides(left, right, top, bottom)


def specs_from_paths(paths: list[Path]):
    grouped: dict[str, tuple] = {}
    for path in paths:
        pages = load_structure(path)
        grid = answer_grid(pages)
        if grid is None:
            continue
        page = next(item for item in pages if grid in item.grids)
        key = maze_key(path.name)
        cells = tuple(true_cells(grid))
        allowed = _margins(page, grid)
        previous = grouped.get(key)
        current = (grid.rows, grid.cols, cells, allowed)
        if previous is None:
            grouped[key] = current
            continue
        if previous[:3] != current[:3]:
            raise ValueError(f'{path.name} does not match the other {key} sheet')
    return [(key, rows, cols, cells, allowed) for key, (rows, cols, cells, allowed) in grouped.items()]


def impose_koshuu(data: bytes) -> bytes:
    """The 2-up sheet is the worksheet turned sideways; the 4-up sheet is scaled."""
    source = pymupdf.open(stream=data, filetype='pdf')
    out = pymupdf.open()
    try:
        width, height = source[0].rect.width, source[0].rect.height
        for index in range(source.page_count):
            if index == 1:
                page = out.new_page(width=width, height=height)
                slot = width / 2
                for copy in range(2):
                    page.show_pdf_page(
                        pymupdf.Rect(copy * slot, 0, (copy + 1) * slot, height),
                        source, 0, rotate=90,
                    )
                continue
            if index == 2:
                page = out.new_page(width=width, height=height)
                half_w, half_h = width / 2, height / 2
                for row in range(2):
                    for col in range(2):
                        page.show_pdf_page(
                            pymupdf.Rect(col * half_w, row * half_h, (col + 1) * half_w, (row + 1) * half_h),
                            source, 0, rotate=0,
                        )
                continue
            out.insert_pdf(source, from_page=index, to_page=index)
        return out.tobytes(deflate=True, garbage=4)
    finally:
        out.close()
        source.close()


def two_up(worksheet: bytes) -> bytes:
    source = pymupdf.open(stream=worksheet, filetype='pdf')
    try:
        page = source[0]
        width, height = 595.276, 841.890
        margin = 16
        out = pymupdf.open()
        try:
            sheet = out.new_page(width=width, height=height)
            slot_h = (height - 3 * margin) / 2
            slot_w = width - 2 * margin
            scale = min(slot_w / page.rect.width, slot_h / page.rect.height)
            drawn_w = page.rect.width * scale
            drawn_h = page.rect.height * scale
            for index in range(2):
                x = (width - drawn_w) / 2
                y = margin + index * (slot_h + margin) + (slot_h - drawn_h) / 2
                sheet.show_pdf_page(pymupdf.Rect(x, y, x + drawn_w, y + drawn_h), source, 0)
            return out.tobytes(deflate=True, garbage=4)
        finally:
            out.close()
    finally:
        source.close()


def sync_stat_pptx(folder: Path | None = None):
    """Put the new statistics statements and route onto the slide deck."""
    from lxml import etree
    from pptx.oxml.ns import qn

    folder = folder or BUNDLED
    deck_path = folder / 'stat-Labirint.pptx'
    answer_path = folder / 'stat-Labirint-Jooptor-A4.pdf'
    if not deck_path.is_file() or not answer_path.is_file():
        return
    from apps.resources.generators.maze_sheet import painted_mask

    doc = pymupdf.open(answer_path)
    try:
        page = doc[0]
        mask = painted_mask(page)
        rows, cols, green = mask
        xs = [1.4, 195.6, 389.7, 583.9]
        ys = [42.1, 118.1, 194.2, 270.3, 346.3, 422.4]
        width, height = 194.2, 76.1
        data = page.get_text('dict')
        texts = []
        for y in ys:
            row_text = []
            for x in xs:
                rect = pymupdf.Rect(x, y, x + width, y + height)
                parts = []
                for block in data['blocks']:
                    if block.get('type') != 0:
                        continue
                    for line in block['lines']:
                        box = pymupdf.Rect(line['bbox'])
                        center = pymupdf.Point((box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)
                        if rect.contains(center):
                            parts.append(''.join(span['text'] for span in line['spans']))
                row_text.append(' '.join(part.strip() for part in parts if part.strip()))
            texts.append(row_text)
    finally:
        doc.close()

    from pptx import Presentation

    deck = Presentation(deck_path)
    for slide_index, slide in enumerate(deck.slides):
        answer = slide_index == 1
        table = next(shape.table for shape in slide.shapes if shape.has_table)
        # Content sits in rows 1..6; row 0 and row 7 are padding.
        for row in range(rows):
            for col in range(cols):
                cell = table.cell(row + 1, col)
                runs = cell._tc.xpath('.//a:t')
                if not runs:
                    continue
                runs[0].text = texts[row][col]
                for extra in runs[1:]:
                    extra.text = ''
                if not answer:
                    continue
                color = 'A9D18E' if (row, col) in green else 'FFFFFF'
                tc_pr = cell._tc.get_or_add_tcPr()
                for child in list(tc_pr):
                    if child.tag == qn('a:solidFill'):
                        tc_pr.remove(child)
                solid = etree.SubElement(tc_pr, qn('a:solidFill'))
                srgb = etree.SubElement(solid, qn('a:srgbClr'))
                srgb.set('val', color)
    deck.save(deck_path)


def rebuild_folder(root: Path | None = None) -> dict[str, Placement]:
    folder = root or BUNDLED
    paths = maze_pdfs(folder)
    specs = specs_from_paths(paths)
    placed = assign_routes(specs)
    originals = {path: path.read_bytes() for path in paths}
    written = {}
    for path, data in originals.items():
        key = maze_key(path.name)
        placement = placed.get(key)
        if placement is None:
            continue
        rewritten = rebuild_pdf(data, placement)
        if path.name.startswith('1-klass-koshuu'):
            rewritten = impose_koshuu(rewritten)
        path.write_bytes(rewritten)
        written[path.name] = (sha256_bytes(data), sha256_bytes(rewritten))
    pptx = folder / 'stat-Labirint.pptx'
    if pptx.is_file():
        previous = pptx.read_bytes()
        sync_stat_pptx(folder)
        written[pptx.name] = (sha256_bytes(previous), sha256_bytes(pptx.read_bytes()))
    worksheet = folder / 'stat-Labirint-A4.pdf'
    two = folder / 'stat-Labirint-2bet-A4.pdf'
    if worksheet.is_file() and two.is_file():
        previous = two.read_bytes()
        produced = two_up(worksheet.read_bytes())
        two.write_bytes(produced)
        written[two.name] = (sha256_bytes(previous), sha256_bytes(produced))
    manifest_path = folder.parent / 'data' / 'maze_path_manifest.json'
    manifest = {
        f'resources/files/{name}': {'old': old, 'new': new}
        for name, (old, new) in sorted(written.items())
    }
    manifest_path.write_text(
        __import__('json').dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    return placed
