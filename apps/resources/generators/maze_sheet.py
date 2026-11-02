"""Read a MathKG maze PDF and paint a new correct route on the same sheet.

The page chrome (header, footer, instructions, logo) stays. Cell statements
move onto the new route. Answer pages fill that route; worksheets leave every
cell white. «МАРЕ» on a label or in the instruction becomes «МААРА».
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from apps.resources.finish_word import replace_finish
from apps.resources.generators.maze_path import Placement

_FONTS = Path(__file__).resolve().parent / 'fonts'
_DEJAVU = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
_DEJAVU_BOLD = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')

_FONT_FILE = {
    'regular': _FONTS / 'Inter-Regular.ttf',
    'bold': _FONTS / 'Inter-Bold.ttf',
    'italic': _FONTS / 'Inter-Italic.ttf',
    'dejavu': _DEJAVU,
    'dejavu-bold': _DEJAVU_BOLD,
}

_START_LABEL = re.compile(r'^[←→↑↓\s]*(БАШТА|СТАРТ)!?[←→↑↓\s]*$')
_FINISH_LABEL = re.compile(r'^[←→↑↓\s]*(МААРА|МАРЕ|МАРА|ФИНИШ|АЯГЫ)!?[←→↑↓\s]*$')
_WORD = re.compile(r'(БАШТА|СТАРТ|МААРА|МАРЕ|МАРА|ФИНИШ|АЯГЫ)')

_DEFAULT_STROKE = (0.0, 0.478431, 0.352941)
_DEFAULT_GREEN = (0.709804, 0.886275, 0.827451)
_INK = (0.121, 0.141, 0.180)


@dataclass
class SpanRec:
    text: str
    dx: float
    dy: float
    size: float
    color: int
    font: str


@dataclass
class ImageRec:
    dx0: float
    dy0: float
    dx1: float
    dy1: float
    stream: bytes


@dataclass
class CellRec:
    rect: pymupdf.Rect
    green: bool
    spans: list[SpanRec] = field(default_factory=list)
    images: list[ImageRec] = field(default_factory=list)

    def text(self) -> str:
        return ' '.join(span.text for span in self.spans).strip()


@dataclass
class LabelRec:
    kind: str
    word: str
    bang: bool
    size: float
    color: int
    font: str
    rect: pymupdf.Rect


@dataclass
class GridRec:
    rows: int
    cols: int
    cells: list[list[CellRec]]
    stroke: tuple[float, float, float]
    stroke_width: float
    green_fill: tuple[float, float, float]
    labels: list[LabelRec]


@dataclass
class PageRec:
    index: int
    width: float
    height: float
    grids: list[GridRec]
    chrome_edits: list[tuple[pymupdf.Rect, str, float, int, str]]


def maze_key(filename: str) -> str:
    stem = Path(filename).stem
    if stem.startswith('stat-Labirint'):
        return 'stat-Labirint'
    return stem


def _rgb_int(color: int) -> tuple[float, float, float]:
    return ((color >> 16) & 255) / 255, ((color >> 8) & 255) / 255, (color & 255) / 255


def _is_green(fill) -> bool:
    if not fill:
        return False
    red, green, blue = fill[:3]
    return green > red + 0.08 and green > 0.45 and red < 0.92


def _cluster(values: list[float], gap: float) -> list[float]:
    if not values:
        return []
    ordered = sorted(values)
    groups = [[ordered[0]]]
    for value in ordered[1:]:
        if value - groups[-1][-1] > gap:
            groups.append([value])
        else:
            groups[-1].append(value)
    return [sum(group) / len(group) for group in groups]


def _split_axis(centers: list[float], typical_gap: float) -> list[list[float]]:
    """Split a row of cell centres where a gap is wider than the cell pitch."""
    if not centers:
        return []
    ordered = sorted(centers)
    if len(ordered) == 1:
        return [ordered]
    gaps = sorted(b - a for a, b in zip(ordered, ordered[1:]))
    pitch = gaps[max(0, len(gaps) // 3 - 1)]
    if 0 < typical_gap < pitch:
        pitch = typical_gap
    limit = max(pitch * 1.45, pitch + 18)
    blocks = [[ordered[0]]]
    for value in ordered[1:]:
        if value - blocks[-1][-1] > limit:
            blocks.append([value])
        else:
            blocks[-1].append(value)
    return blocks


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def _drawing_rects(page) -> list[tuple[pymupdf.Rect, bool, tuple, float]]:
    found = []
    for drawing in page.get_drawings():
        rect = drawing.get('rect')
        fill = drawing.get('fill')
        if rect is None or fill is None:
            continue
        if not (60 < rect.width < 260 and 32 < rect.height < 130):
            continue
        stroke = drawing.get('color') or _DEFAULT_STROKE
        width = float(drawing.get('width') or 1.5)
        found.append((pymupdf.Rect(rect), _is_green(fill), tuple(stroke[:3]), width))
    return found


def _grids_from_drawings(page) -> list[tuple[list[list[tuple]], tuple, float, tuple]]:
    """Return grids of (rect, green) plus stroke, width, green fill."""
    raw = _drawing_rects(page)
    if len(raw) < 8:
        return []
    width = _median([rect.width for rect, *_ in raw])
    height = _median([rect.height for rect, *_ in raw])
    xs = _cluster([rect.x0 for rect, *_ in raw], width * 0.45)
    ys = _cluster([rect.y0 for rect, *_ in raw], height * 0.45)
    x_blocks = _split_axis(xs, width)
    y_blocks = _split_axis(ys, height)
    greens = [fill for _rect, _green, _stroke, _width in []]
    green_fills = []
    strokes = []
    widths = []
    for rect, green, stroke, stroke_width in raw:
        strokes.append(stroke)
        widths.append(stroke_width)
        if green:
            # Recover the fill by sampling is unnecessary; store the known green later.
            green_fills.append(rect)
    stroke = strokes[0] if strokes else _DEFAULT_STROKE
    stroke_width = _median(widths) if widths else 1.5
    grids = []
    for x_block in x_blocks:
        for y_block in y_blocks:
            cols = len(x_block)
            rows = len(y_block)
            if rows < 3 or cols < 3:
                continue
            slots = []
            present = 0
            for row, y in enumerate(y_block):
                line = []
                for col, x in enumerate(x_block):
                    match = None
                    for rect, green, _stroke, _width in raw:
                        if abs(rect.x0 - x) < width * 0.4 and abs(rect.y0 - y) < height * 0.4:
                            match = (rect, green)
                            break
                    if match is None:
                        rect = pymupdf.Rect(x, y, x + width, y + height)
                        match = (rect, False)
                    else:
                        present += 1
                    line.append(match)
                slots.append(line)
            if present < rows * cols * 0.35:
                continue
            grids.append((slots, stroke, stroke_width, _DEFAULT_GREEN))
    return grids


def _short_lines(page):
    lines = []
    data = page.get_text('dict')
    for block in data['blocks']:
        if block.get('type') != 0:
            continue
        for line in block['lines']:
            text = ''.join(span['text'] for span in line['spans']).strip()
            if not text or len(text) > 48:
                continue
            if text.startswith((
                'БАШТАдан', 'Туура', 'текшер', 'Блум', 'MathKG', 'Аты',
                'Классы', 'Күнү', 'Ката', 'Тапшырма', 'Жооп', 'ЖООП',
                'Лабиринт', 'Математика', 'Бир ката', 'Эмне', 'Мисал',
            )):
                continue
            if _START_LABEL.match(text) or _FINISH_LABEL.match(text):
                continue
            if '=' not in text:
                continue
            box = pymupdf.Rect(line['bbox'])
            lines.append((box, text, line['spans']))
    return lines


def _grids_from_text(page) -> list[list[list[pymupdf.Rect]]]:
    lines = _short_lines(page)
    if len(lines) < 12:
        return []
    xs = _cluster([(box.x0 + box.x1) / 2 for box, *_ in lines], 36)
    ys = _cluster([(box.y0 + box.y1) / 2 for box, *_ in lines], 20)
    if len(xs) < 3 or len(ys) < 3:
        return []
    x_gap = _median([b - a for a, b in zip(xs, xs[1:])]) if len(xs) > 1 else 80
    y_gap = _median([b - a for a, b in zip(ys, ys[1:])]) if len(ys) > 1 else 40
    x_blocks = _split_axis(xs, x_gap)
    y_blocks = _split_axis(ys, y_gap)
    grids = []
    for x_block in x_blocks:
        for y_block in y_blocks:
            if len(x_block) < 3 or len(y_block) < 3:
                continue
            col_bounds = _bounds(x_block)
            row_bounds = _bounds(y_block)
            slots = []
            for y0, y1 in row_bounds:
                line = []
                for x0, x1 in col_bounds:
                    line.append(pymupdf.Rect(x0, y0, x1, y1))
                slots.append(line)
            grids.append(slots)
    return grids


def _bounds(centers: list[float]) -> list[tuple[float, float]]:
    if len(centers) == 1:
        return [(centers[0] - 40, centers[0] + 40)]
    mids = [(centers[i] + centers[i + 1]) / 2 for i in range(len(centers) - 1)]
    left = centers[0] - (mids[0] - centers[0])
    right = centers[-1] + (centers[-1] - mids[-1])
    edges = [left, *mids, right]
    inset = 2.5
    return [(edges[i] + inset, edges[i + 1] - inset) for i in range(len(centers))]


def _span_records(page) -> list[tuple[pymupdf.Rect, pymupdf.Point, SpanRec]]:
    """Every text run, with its box and baseline, read once per page."""
    found = []
    data = page.get_text('dict')
    for block in data['blocks']:
        if block.get('type') != 0:
            continue
        for line in block['lines']:
            for span in line['spans']:
                text = span['text']
                if not text.strip():
                    continue
                origin = span.get('origin') or (span['bbox'][0], span['bbox'][3])
                point = pymupdf.Point(origin)
                found.append((
                    pymupdf.Rect(span['bbox']),
                    point,
                    SpanRec(
                        text=text,
                        dx=0,
                        dy=0,
                        size=float(span['size']),
                        color=int(span['color']),
                        font=span.get('font') or 'Inter-Regular',
                    ),
                ))
    return found


def _spans_in(records, rect: pymupdf.Rect) -> list[SpanRec]:
    found = []
    for box, point, span in records:
        center = pymupdf.Point((box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)
        if not rect.contains(point) and not rect.contains(center):
            continue
        found.append(SpanRec(
            span.text,
            point.x - rect.x0,
            point.y - rect.y0,
            span.size,
            span.color,
            span.font,
        ))
    found.sort(key=lambda item: (round(item.dy, 1), item.dx))
    return found


def _images_in(page, infos, rect: pymupdf.Rect) -> list[ImageRec]:
    """Clip each picture from the page so a soft mask stays with the drawing."""
    found = []
    for info in infos:
        box = pymupdf.Rect(info['bbox'])
        if box.width > rect.width * 0.82 and box.height > rect.height * 0.82:
            continue
        center = pymupdf.Point((box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)
        if not rect.contains(center):
            continue
        if box.width < 18 or box.height < 18:
            continue
        clip = box & page.rect
        if clip.is_empty:
            continue
        pix = page.get_pixmap(clip=clip, matrix=pymupdf.Matrix(2, 2), alpha=True)
        found.append(ImageRec(
            clip.x0 - rect.x0,
            clip.y0 - rect.y0,
            clip.x1 - rect.x0,
            clip.y1 - rect.y0,
            pix.tobytes('png'),
        ))
    return found


def _labels(page) -> list[LabelRec]:
    found = []
    data = page.get_text('dict')
    for block in data['blocks']:
        if block.get('type') != 0:
            continue
        for line in block['lines']:
            text = ''.join(span['text'] for span in line['spans']).strip()
            kind = None
            if _START_LABEL.match(text):
                kind = 'start'
            elif _FINISH_LABEL.match(text):
                kind = 'finish'
            if kind is None:
                continue
            word = _WORD.search(text).group(1)
            span = line['spans'][0]
            found.append(LabelRec(
                kind=kind,
                word=word,
                bang=text.endswith('!'),
                size=float(span['size']),
                color=int(span['color']),
                font=span.get('font') or 'Inter-Bold',
                rect=pymupdf.Rect(line['bbox']),
            ))
    return found


def _chrome_edits(page, grids: list[GridRec]):
    covered = []
    for grid in grids:
        for row in grid.cells:
            for cell in row:
                covered.append(cell.rect)
        for label in grid.labels:
            covered.append(label.rect)
    edits = []
    data = page.get_text('dict')
    for block in data['blocks']:
        if block.get('type') != 0:
            continue
        for line in block['lines']:
            text = ''.join(span['text'] for span in line['spans'])
            updated, _counts = replace_finish(text)
            if updated == text:
                continue
            box = pymupdf.Rect(line['bbox'])
            if any(box.intersects(rect) and _overlap_ratio(box, rect) > 0.5 for rect in covered):
                continue
            span = line['spans'][0]
            edits.append((box, updated, float(span['size']), int(span['color']), span.get('font') or ''))
    return edits


def _overlap_ratio(left: pymupdf.Rect, right: pymupdf.Rect) -> float:
    inter = left & right
    if inter.is_empty or left.get_area() <= 0:
        return 0
    return inter.get_area() / left.get_area()


def _nearest_grid(label: LabelRec, grids: list[GridRec]) -> GridRec | None:
    if not grids:
        return None
    cx = (label.rect.x0 + label.rect.x1) / 2
    cy = (label.rect.y0 + label.rect.y1) / 2

    def distance(grid: GridRec) -> float:
        cells = [cell.rect for row in grid.cells for cell in row]
        left = min(rect.x0 for rect in cells)
        top = min(rect.y0 for rect in cells)
        right = max(rect.x1 for rect in cells)
        bottom = max(rect.y1 for rect in cells)
        dx = 0 if left <= cx <= right else min(abs(cx - left), abs(cx - right))
        dy = 0 if top <= cy <= bottom else min(abs(cy - top), abs(cy - bottom))
        return dx * dx + dy * dy

    return min(grids, key=distance)


def parse_page(doc, page_index: int, with_assets: bool) -> PageRec:
    page = doc[page_index]
    drawing_grids = _grids_from_drawings(page)
    grids: list[GridRec] = []
    records = _span_records(page) if with_assets else []
    image_infos = page.get_image_info(xrefs=True) if with_assets else []
    if drawing_grids:
        for slots, stroke, stroke_width, green_fill in drawing_grids:
            cells = []
            for line in slots:
                row = []
                for rect, green in line:
                    spans = _spans_in(records, rect) if with_assets else []
                    images = _images_in(page, image_infos, rect) if with_assets else []
                    row.append(CellRec(rect, green, spans, images))
                cells.append(row)
            grids.append(GridRec(
                len(cells), len(cells[0]), cells, stroke, stroke_width, green_fill, [],
            ))
    else:
        for slots in _grids_from_text(page):
            cells = []
            for line in slots:
                row = []
                for rect in line:
                    spans = _spans_in(records, rect) if with_assets else []
                    images = _images_in(page, image_infos, rect) if with_assets else []
                    row.append(CellRec(rect, False, spans, images))
                cells.append(row)
            grids.append(GridRec(
                len(cells), len(cells[0]), cells, _DEFAULT_STROKE, 1.35, _DEFAULT_GREEN, [],
            ))
    labels = _labels(page)
    for label in labels:
        grid = _nearest_grid(label, grids)
        if grid is not None:
            grid.labels.append(label)
    # A real green fill, sampled from a green drawing when the page has one.
    for grid in grids:
        for row in grid.cells:
            for cell in row:
                if not cell.green:
                    continue
                for drawing in page.get_drawings():
                    rect = drawing.get('rect')
                    fill = drawing.get('fill')
                    if rect is None or not _is_green(fill):
                        continue
                    if abs(rect.x0 - cell.rect.x0) < 8 and abs(rect.y0 - cell.rect.y0) < 8:
                        grid.green_fill = tuple(fill[:3])
                        if drawing.get('color'):
                            grid.stroke = tuple(drawing['color'][:3])
                        if drawing.get('width'):
                            grid.stroke_width = float(drawing['width'])
                        break
    chrome = _chrome_edits(page, grids) if with_assets else []
    return PageRec(page_index, page.rect.width, page.rect.height, grids, chrome)


def true_cells(grid: GridRec) -> list[tuple[int, int]]:
    return [
        (row, col)
        for row, line in enumerate(grid.cells)
        for col, cell in enumerate(line)
        if cell.green
    ]


def answer_grid(pages: list[PageRec]) -> GridRec | None:
    best = None
    best_count = 0
    for page in pages:
        for grid in page.grids:
            count = len(true_cells(grid))
            if count > best_count:
                best = grid
                best_count = count
    return best


def _font_kind(font_name: str) -> str:
    lowered = (font_name or '').lower()
    if 'bold' in lowered or 'smbld' in lowered:
        return 'bold'
    if 'italic' in lowered or 'oblique' in lowered:
        return 'italic'
    return 'regular'


def _font_supports(path: Path, text: str) -> bool:
    if not path.is_file():
        return False
    font = pymupdf.Font(fontfile=str(path))
    for char in text:
        if char.isspace():
            continue
        if not font.has_glyph(ord(char)):
            return False
    return True


def _pick_font(text: str, font_name: str) -> Path:
    kind = _font_kind(font_name)
    primary = _FONT_FILE[kind]
    if _font_supports(primary, text):
        return primary
    backup = _FONT_FILE['dejavu-bold' if kind == 'bold' else 'dejavu']
    if _font_supports(backup, text):
        return backup
    return primary


def _label_text(label: LabelRec, side: str) -> str:
    word = label.word
    if word in {'МАРЕ', 'МАРА', 'МААРА'}:
        word = 'МААРА'
    bang = '!' if label.bang else ''
    if label.kind == 'start':
        written = {
            'left': f'{word} →',
            'right': f'← {word}',
            'top': f'{word} ↓',
            'bottom': f'↑ {word}',
        }[side]
    else:
        written = {
            'right': f'→ {word}',
            'left': f'{word} ←',
            'bottom': f'↓ {word}',
            'top': f'↑ {word}',
        }[side]
    if bang and not written.endswith('!'):
        written = written.replace(word, word + bang)
    return written


def _label_origin(cell: pymupdf.Rect, side: str, width: float, size: float):
    gap = 5
    if side == 'left':
        return cell.x0 - gap - width, (cell.y0 + cell.y1) / 2 + size * 0.28
    if side == 'right':
        return cell.x1 + gap, (cell.y0 + cell.y1) / 2 + size * 0.28
    if side == 'top':
        return (cell.x0 + cell.x1) / 2 - width / 2, cell.y0 - gap
    return (cell.x0 + cell.x1) / 2 - width / 2, cell.y1 + gap + size * 0.75


def _paint_label(page, cell: pymupdf.Rect, side: str, text: str, size: float, color: int, font_name: str):
    font_path = _pick_font(text, font_name if 'bold' in font_name.lower() else 'Inter-Bold')
    font = pymupdf.Font(fontfile=str(font_path))
    used = size
    for _shrink in range(4):
        width = font.text_length(text, used)
        x, y = _label_origin(cell, side, width, used)
        box = pymupdf.Rect(x, y - used, x + width, y + used * 0.25)
        on_page = box.x0 >= 1 and box.y0 >= 1 and box.x1 <= page.rect.width - 1 and box.y1 <= page.rect.height - 1
        if on_page and not box.intersects(cell):
            page.insert_text(
                (x, y), text, fontsize=used,
                fontname='maze-' + font_path.stem, fontfile=str(font_path),
                color=_rgb_int(color),
            )
            return
        used *= 0.86
    width = font.text_length(text, used)
    x, y = _label_origin(cell, side, width, used)
    page.insert_text(
        (x, max(y, used)), text, fontsize=used,
        fontname='maze-' + font_path.stem, fontfile=str(font_path),
        color=_rgb_int(color),
    )


def _paint_span(page, origin, span: SpanRec):
    text, _counts = replace_finish(span.text)
    if not text:
        return
    # Keep a run on one font. Split only when Inter lacks a glyph.
    pieces = []
    buffer = ''
    buffer_path = None
    for char in text:
        path = _pick_font(char, span.font)
        if buffer and path != buffer_path:
            pieces.append((buffer, buffer_path))
            buffer = ''
        buffer += char
        buffer_path = path
    if buffer:
        pieces.append((buffer, buffer_path))
    cursor = origin[0]
    for piece, path in pieces:
        page.insert_text(
            (cursor, origin[1]),
            piece,
            fontsize=span.size,
            fontname='maze-' + path.stem,
            fontfile=str(path),
            color=_rgb_int(span.color) if span.color else _INK,
        )
        font = pymupdf.Font(fontfile=str(path))
        cursor += font.text_length(piece, span.size)


def text_matrix(grid: GridRec) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(cell.text() for cell in row) for row in grid.cells)


def _dihedral(size: int):
    """Local (row, col) -> canonical (row, col) for a square grid."""
    n = size
    return (
        ('same', lambda r, c: (r, c)),
        ('rot90', lambda r, c: (c, n - 1 - r)),
        ('rot180', lambda r, c: (n - 1 - r, n - 1 - c)),
        ('rot270', lambda r, c: (n - 1 - c, r)),
        ('flipx', lambda r, c: (r, n - 1 - c)),
        ('flipy', lambda r, c: (n - 1 - r, c)),
        ('transpose', lambda r, c: (c, r)),
        ('anti', lambda r, c: (n - 1 - c, n - 1 - r)),
    )


def match_orientation(grid: GridRec, canonical: tuple[tuple[str, ...], ...]):
    """Return local->canonical and canonical->local when the cells are a turn of the master."""
    if grid.rows != len(canonical) or grid.cols != len(canonical[0]):
        return None
    if grid.rows != grid.cols:
        local = text_matrix(grid)
        if local == canonical:
            identity = {(r, c): (r, c) for r in range(grid.rows) for c in range(grid.cols)}
            return identity, dict(identity)
        return None
    local = text_matrix(grid)
    for _name, forward in _dihedral(grid.rows):
        if all(
            local[r][c] == canonical[forward(r, c)[0]][forward(r, c)[1]]
            for r in range(grid.rows)
            for c in range(grid.cols)
        ):
            local_to = {(r, c): forward(r, c) for r in range(grid.rows) for c in range(grid.cols)}
            canonical_to = {canon: loc for loc, canon in local_to.items()}
            return local_to, canonical_to
    return None


def paint_page(source_doc, page_rec: PageRec, placement: Placement | None, canonical, out_doc):
    source = source_doc[page_rec.index]
    page = out_doc.new_page(width=page_rec.width, height=page_rec.height)
    page.show_pdf_page(page.rect, source_doc, page_rec.index)
    answer = any(cell.green for grid in page_rec.grids for row in grid.cells for cell in row)
    mapping = placement.as_dict() if placement is not None else {}

    for grid in page_rec.grids:
        for row in grid.cells:
            for cell in row:
                pad = pymupdf.Rect(cell.rect.x0 - 3, cell.rect.y0 - 3, cell.rect.x1 + 3, cell.rect.y1 + 3)
                page.draw_rect(pad, color=None, fill=(1, 1, 1), width=0)
        for label in grid.labels:
            pad = pymupdf.Rect(label.rect.x0 - 2, label.rect.y0 - 2, label.rect.x1 + 2, label.rect.y1 + 4)
            page.draw_rect(pad, color=None, fill=(1, 1, 1), width=0)

    for box, text, size, color, font_name in page_rec.chrome_edits:
        pad = pymupdf.Rect(box.x0 - 1, box.y0 - 1, box.x1 + 8, box.y1 + 2)
        page.draw_rect(pad, color=None, fill=(1, 1, 1), width=0)
        _paint_span(page, (box.x0, box.y1 - 1), SpanRec(text, 0, 0, size, color, font_name))

    for grid in page_rec.grids:
        if placement is None or (grid.rows, grid.cols) != (placement.path.rows, placement.path.cols):
            continue
        radius = 0.08
        matched = match_orientation(grid, canonical) if canonical is not None else None
        if matched is None:
            local_to = {(r, c): (r, c) for r in range(grid.rows) for c in range(grid.cols)}
            canonical_to = dict(local_to)
        else:
            local_to, canonical_to = matched
        physical_start = canonical_to[placement.path.start]
        physical_finish = canonical_to[placement.path.finish]
        # The route already picked a margin that fits this sheet.
        start_side = placement.path.start_side
        finish_side = placement.path.finish_side
        for row_index, row in enumerate(grid.cells):
            for col_index, cell in enumerate(row):
                canonical_slot = local_to[(row_index, col_index)]
                on_route = canonical_slot in placement.path.mask
                fill = grid.green_fill if answer and on_route else (1, 1, 1)
                page.draw_rect(
                    cell.rect,
                    color=grid.stroke,
                    fill=fill,
                    width=max(grid.stroke_width, 1.1),
                    radius=radius,
                )
                old_canonical = mapping.get(canonical_slot, canonical_slot)
                source_rc = canonical_to[old_canonical]
                source_cell = grid.cells[source_rc[0]][source_rc[1]]
                for image in source_cell.images:
                    target = pymupdf.Rect(
                        cell.rect.x0 + image.dx0,
                        cell.rect.y0 + image.dy0,
                        cell.rect.x0 + image.dx1,
                        cell.rect.y0 + image.dy1,
                    )
                    page.insert_image(target, stream=image.stream, keep_proportion=False)
                for span in source_cell.spans:
                    _paint_span(page, (cell.rect.x0 + span.dx, cell.rect.y0 + span.dy), span)
        start_label = next((label for label in grid.labels if label.kind == 'start'), None)
        finish_label = next((label for label in grid.labels if label.kind == 'finish'), None)
        if start_label is not None:
            row, col = physical_start
            _paint_label(
                page, grid.cells[row][col].rect, start_side,
                _label_text(start_label, start_side),
                start_label.size, start_label.color, start_label.font,
            )
        if finish_label is not None:
            row, col = physical_finish
            _paint_label(
                page, grid.cells[row][col].rect, finish_side,
                _label_text(finish_label, finish_side),
                finish_label.size, finish_label.color, finish_label.font,
            )
    return page


def _canonical_matrix(pages: list[PageRec], placement: Placement):
    sized = [
        grid
        for page in pages
        for grid in page.grids
        if (grid.rows, grid.cols) == (placement.path.rows, placement.path.cols)
    ]
    for grid in sized:
        if any(cell.green for row in grid.cells for cell in row):
            return text_matrix(grid)
    if sized:
        return text_matrix(sized[0])
    return None


def _wipe_old_route(page, page_rec: PageRec):
    """Remove the old cell text, pictures and finish word before the new route is drawn."""
    rects = []
    for grid in page_rec.grids:
        for row in grid.cells:
            for cell in row:
                rects.append(pymupdf.Rect(cell.rect.x0 - 2, cell.rect.y0 - 2, cell.rect.x1 + 2, cell.rect.y1 + 2))
        for label in grid.labels:
            rects.append(pymupdf.Rect(label.rect.x0 - 1, label.rect.y0 - 2, label.rect.x1 + 3, label.rect.y1 + 3))
    for box, *_rest in page_rec.chrome_edits:
        rects.append(pymupdf.Rect(box.x0 - 1, box.y0 - 1, box.x1 + 8, box.y1 + 2))
    if not rects:
        return
    for rect in rects:
        page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions(
        images=pymupdf.PDF_REDACT_IMAGE_REMOVE,
        graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
        text=pymupdf.PDF_REDACT_TEXT_REMOVE,
    )


def rebuild_pdf(data: bytes, placement: Placement | None) -> bytes:
    source = pymupdf.open(stream=data, filetype='pdf')
    cleaned = None
    out = None
    try:
        pages = [parse_page(source, index, with_assets=True) for index in range(source.page_count)]
        if not any(page.grids for page in pages):
            return data
        cleaned = pymupdf.open(stream=data, filetype='pdf')
        for page_rec, page in zip(pages, cleaned):
            _wipe_old_route(page, page_rec)
        canonical = _canonical_matrix(pages, placement) if placement is not None else None
        out = pymupdf.open()
        for page in pages:
            use = placement
            if placement is not None and not any(
                (grid.rows, grid.cols) == (placement.path.rows, placement.path.cols)
                for grid in page.grids
            ):
                use = None
            paint_page(cleaned, page, use, canonical, out)
        out.subset_fonts()
        return out.tobytes(deflate=True, garbage=4)
    finally:
        if out is not None:
            out.close()
        if cleaned is not None:
            cleaned.close()
        source.close()


def painted_mask(page):
    """Visible route. A sample of each cell is used, so a buried old fill does not count."""
    rects = []
    for drawing in page.get_drawings():
        rect = drawing.get('rect')
        fill = drawing.get('fill')
        if rect is None or not fill:
            continue
        if not (60 < rect.width < 260 and 32 < rect.height < 130):
            continue
        rects.append(pymupdf.Rect(rect))
    if len(rects) < 8:
        return None
    width = _median([rect.width for rect in rects])
    height = _median([rect.height for rect in rects])
    # Prefer the size that was drawn last (the new cells), not an older layer.
    late = rects[-min(len(rects), 40):]
    width = _median([rect.width for rect in late])
    height = _median([rect.height for rect in late])
    chosen = [rect for rect in rects if abs(rect.width - width) < 8 and abs(rect.height - height) < 8]
    xs = _cluster([rect.x0 for rect in chosen], max(18, width * 0.35))
    ys = _cluster([rect.y0 for rect in chosen], max(14, height * 0.35))
    xs = _split_axis(xs, width)[0] if xs else []
    ys = _split_axis(ys, height)[0] if ys else []
    if len(xs) < 3 or len(ys) < 3:
        return None
    green_slots = set()
    for row, y in enumerate(ys):
        for col, x in enumerate(xs):
            # Inside the rounded corner, above a centred clock or sum.
            clip = pymupdf.Rect(
                x + width * 0.12, y + height * 0.16,
                x + width * 0.22, y + height * 0.28,
            )
            pix = page.get_pixmap(clip=clip, matrix=pymupdf.Matrix(0.2, 0.2), alpha=False)
            if not pix.samples:
                continue
            red, green, blue = pix.samples[0], pix.samples[1], pix.samples[2]
            if green > red + 15 and red < 230:
                green_slots.add((row, col))
    if len(green_slots) < 2:
        return None
    return len(ys), len(xs), frozenset(green_slots)


def load_structure(path: Path) -> list[PageRec]:
    doc = pymupdf.open(path)
    try:
        return [parse_page(doc, index, with_assets=False) for index in range(doc.page_count)]
    finally:
        doc.close()
