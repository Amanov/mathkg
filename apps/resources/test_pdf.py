"""Render a generated test paper to PDF with PyMuPDF only.

The earlier renderer used WeasyPrint, which loads Pango, GObject and
HarfBuzz from the operating system when the request arrives. On Railway
those libraries were missing from the linker path, so the download of a
freshly made test ended in «Server Error (500)». PyMuPDF ships its own
layout engine inside the wheel and needs nothing from the system, so the
same code works on a laptop, in the tests and in production.

Each variant starts on a new page with a Cambridge-style front block (name
box, «АДЕГЕНДЕ УШУЛАРДЫ ОКУ» rules). Every question has its number in the
margin, a faint squared working space, a dotted answer line and its marks
in [ ]. The answer key comes last, on its own page, so a teacher can print
the questions without the answers.
"""

import html
import io
from pathlib import Path

import pymupdf

# Inter without its GSUB table: its contextual alternates turn «-», «(» and
# «)» into glyphs with no Unicode value, so copied or searched PDF text broke.
FONT_DIR = Path(__file__).resolve().parent / 'generators' / 'fonts' / 'test-pdf'
FONT_FAMILY = 'MathKG-Kyrgyz'

PAGE = pymupdf.paper_rect('a4')
MARGIN_X = 40
MARGIN_TOP = 40
MARGIN_BOTTOM = 52
CONTENT = pymupdf.Rect(MARGIN_X, MARGIN_TOP, PAGE.width - MARGIN_X, PAGE.height - MARGIN_BOTTOM)

NAVY = '#0f3c58'
INK = '#1a1a2e'
MUTED = '#475569'
ACCENT = '#0d6efd'
LINE = '#94a3b8'

# No background colours on table cells: MuPDF repeats cell fills from an
# earlier page as grey stripes on the next one.
CSS = f"""
@font-face {{ font-family: {FONT_FAMILY}; src: url(Inter-Regular.ttf); }}
@font-face {{ font-family: {FONT_FAMILY}; src: url(Inter-Bold.ttf); font-weight: bold; }}
* {{ font-family: {FONT_FAMILY}; }}
body {{ font-size: 11pt; color: {INK}; line-height: 1.35; margin: 0; }}
p {{ margin: 0 0 3pt 0; }}
.brand {{ font-weight: bold; color: {ACCENT}; font-size: 10pt; margin-bottom: 2pt; }}
.title {{ font-weight: bold; color: {NAVY}; font-size: 15pt; margin-bottom: 4pt; }}
.paper-title {{ font-weight: bold; font-size: 12.5pt; margin-bottom: 2pt; }}
.meta {{ color: {MUTED}; font-size: 9.5pt; }}
.note {{ color: {MUTED}; font-size: 10pt; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 6pt; }}
th {{ font-weight: bold; color: {NAVY}; text-align: left; font-size: 9.5pt; padding: 3pt 4pt; border: 1px solid #cbd5e1; }}
td {{ font-size: 9.5pt; padding: 3pt 4pt; border: 1px solid #cbd5e1; vertical-align: top; }}
.sum td {{ font-weight: bold; border-top: 1.5px solid {LINE}; }}
.worked {{ color: {MUTED}; font-size: 8.5pt; }}

.cover {{ margin-top: 4pt; }}
.cover td {{ font-size: 9pt; padding: 4pt 5pt; border: 1px solid {LINE}; }}
.cover .lab {{ font-weight: bold; color: {NAVY}; text-align: center; font-size: 8.5pt; }}
.cover .val {{ text-align: center; font-size: 10pt; }}
.read {{ margin-top: 10pt; font-weight: bold; font-size: 10pt; }}
.rule {{ font-size: 9.5pt; margin: 1pt 0 0 0; }}
.gap {{ margin-bottom: 12pt; }}

.qt {{ width: 100%; margin-top: 14pt; }}
.qt td {{ border: none; padding: 0; font-size: 11pt; }}
.qt .n {{ width: 22pt; font-weight: bold; color: {NAVY}; }}
.qtext {{ margin: 0; }}
.opt {{ margin: 2pt 0 0 10pt; }}
.letter {{ font-weight: bold; }}
.match {{ width: 100%; margin-top: 5pt; }}
.match td {{ border: 1px solid #cbd5e1; padding: 3pt 5pt; font-size: 10.5pt; }}
.grid {{ margin-top: 6pt; }}
.ans {{ text-align: right; margin-top: 6pt; }}
.marks {{ font-weight: bold; font-size: 10pt; }}
.end {{ text-align: center; font-weight: bold; margin-top: 22pt; letter-spacing: 1pt; }}
"""

# Dotted answer line, right-aligned like a Cambridge paper.
WRITE_LINE = '.' * 46
ANSWER_LINE = f'Жообу: {WRITE_LINE}'
# Height (pt) of the squared working space under each kind of question.
GRID_HEIGHT = {
    'extended': 128,
    'written': 128,
    'diagram': 142,
    'calculation': 71,
    'short_response': 57,
    'fill_blank': 0,
    'choice': 0,
    'true_false': 0,
    'matching': 0,
}
GRID_STEP = 14.17  # 5 mm squares
GRID_LINE = (0.86, 0.90, 0.95)
GRID_EDGE = (0.74, 0.80, 0.88)


def _e(value):
    return html.escape(str(value if value is not None else ''))


def _header(test):
    parts = ['<p class="brand">MathKG</p>']
    if test.get('title'):
        parts.append(f'<p class="paper-title">{_e(test["title"])}</p>')
    parts.append(f'<p class="title">{_e(test.get("grade_label"))} · {_e(test.get("test_type_label"))} тест</p>')
    parts.append(f'<p class="meta">Темалар: {_e(test.get("topics_label"))}</p>')
    meta = []
    if test.get('mix_label'):
        meta.append(f'Деңгээл: {_e(test["mix_label"])}')
    if test.get('formats_label'):
        meta.append(f'Суроолордун түрү: {_e(test["formats_label"])}')
    if meta:
        parts.append(f'<p class="meta">{" · ".join(meta)}</p>')
    return ''.join(parts)


def _cover(test, variant):
    """Name box and rules, laid out like a Cambridge exam front page."""
    minutes = test.get('duration_minutes')
    return (
        '<table class="cover">'
        '<tr><td class="lab" colspan="3">Аты-жөнү</td><td class="lab">Класс</td><td class="lab">Күнү</td></tr>'
        '<tr><td class="val" colspan="3">&#160;</td><td class="val">&#160;</td>'
        f'<td class="val">{_e(test.get("created_label"))}</td></tr>'
        '<tr><td class="lab">Сабак</td><td class="lab">Класс деңгээли</td><td class="lab">Тест</td>'
        '<td class="lab">Вариант</td><td class="lab">Балл</td></tr>'
        f'<tr><td class="val">Математика</td><td class="val">{_e(test.get("grade_label"))}</td>'
        f'<td class="val">{_e(test.get("title") or test.get("test_type_label"))}</td>'
        f'<td class="val">{_e(variant.get("number"))}</td>'
        f'<td class="val">____ / {_e(variant.get("points"))}</td></tr>'
        '</table>'
        '<p class="read">АДЕГЕНДЕ УШУЛАРДЫ ОКУ</p>'
        '<p class="rule">Аты-жөнүңдү жана классыңды жаз.</p>'
        '<p class="rule">Бардык суроолорго жооп бер.</p>'
        '<p class="rule">Чыгарылышын суроонун астындагы чакмак талаага жаз.</p>'
        '<p class="rule">Ар бир суроонун баллы [ ] кашаанын ичинде берилген.</p>'
        f'<p class="rule">Жалпы балл: {_e(variant.get("points"))}.</p>'
        + (f'<p class="rule">Убакыт: {_e(minutes)} мүнөт.</p>' if minutes else '')
        + '<p class="gap"></p>'
    )


def _question(q, grid_id):
    fmt = q.get('format')
    out = [f'<p class="qtext">{_e(q.get("text"))}</p>']
    if fmt == 'matching':
        rows = []
        left, right = q.get('left') or [], q.get('right') or []
        for i in range(max(len(left), len(right))):
            a = left[i] if i < len(left) else None
            b = right[i] if i < len(right) else None
            cell_a = f'<span class="letter">{_e(a["n"])})</span> {_e(a["text"])}' if a else ''
            cell_b = f'<span class="letter">{_e(b["letter"])})</span> {_e(b["text"])}' if b else ''
            rows.append(f'<tr><td>{cell_a}</td><td>{cell_b}</td></tr>')
        out.append(f'<table class="match">{"".join(rows)}</table>')
    elif q.get('options'):
        for opt in q['options']:
            out.append(f'<p class="opt"><span class="letter">{_e(opt["letter"])})</span> {_e(opt["text"])}</p>')
    height = GRID_HEIGHT.get(fmt, 71 if q.get('line_slots') else 0)
    if q.get('figure'):
        height = max(height, GRID_HEIGHT['diagram'])
    if height:
        out.append(f'<div class="grid" id="{grid_id}" style="height: {height}pt"></div>')
    out.append(
        f'<p class="ans">{ANSWER_LINE}&#160;&#160;&#160;'
        f'<span class="marks">[{_e(q.get("points"))}]</span></p>'
    )
    return (
        f'<table class="qt"><tr><td class="n">{_e(q.get("number"))}</td>'
        f'<td>{"".join(out)}</td></tr></table>'
    )


def _variant_html(test, variant):
    body = [_header(test), _cover(test, variant)]
    for q in variant.get('questions', []):
        body.append(_question(q, f'grid-{variant.get("number")}-{q.get("number")}'))
    body.append('<p class="end">ТЕСТТИН АЯГЫ</p>')
    return f'<body>{"".join(body)}</body>'


def _key_html(test):
    body = [
        '<p class="brand">MathKG</p>',
        '<p class="title">Жооп ачкычы жана баалоо схемасы</p>',
        f'<p class="meta">{_e(test.get("grade_label"))} · {_e(test.get("test_type_label"))} тест</p>',
        f'<p class="meta">Темалар: {_e(test.get("topics_label"))}</p>',
    ]
    if test.get('marking_note'):
        body.append(f'<p class="note">{_e(test["marking_note"])}</p>')
    if test.get('borrowed'):
        body.append('<p class="note">Кээ бир деңгээлде суроо жетпей калды. '
                    'Жетишпеген орун башка деңгээлден толду.</p>')
    rows = ['<tr><th>Вариант</th><th>№</th><th>Түрү</th><th>Жооп</th><th>Балл</th></tr>']
    for variant in test.get('variants', []):
        for q in variant.get('questions', []):
            worked = f'<br><span class="worked">{_e(q["solution"])}</span>' if q.get('solution') else ''
            rows.append(
                f'<tr><td>{_e(variant.get("number"))}</td><td>{_e(q.get("number"))}</td>'
                f'<td>{_e(q.get("type_label"))}</td><td>{_e(q.get("answer"))}{worked}</td>'
                f'<td>{_e(q.get("points"))}</td></tr>'
            )
        rows.append(
            f'<tr class="sum"><td>{_e(variant.get("number"))}</td><td></td><td>Жалпы</td>'
            f'<td></td><td>{_e(variant.get("points"))}</td></tr>'
        )
    body.append(f'<table>{"".join(rows)}</table>')
    if test.get('sample_only'):
        body.append('<p class="note">Бул суроолор үлгү катары белгиленген. Алар үлгү банкынан алынды.</p>')
    return f'<body>{"".join(body)}</body>'


def _write_section(writer, html_text, archive, first_page, grids):
    """Lay out one section; remember where each working space landed."""
    story = pymupdf.Story(html=html_text, user_css=CSS, archive=archive)
    page = first_page
    more = True

    def record(pos):
        if pos.id and pos.id.startswith('grid-') and pos.open_close & 1:
            grids.append((page, pymupdf.Rect(pos.rect)))

    while more:
        device = writer.begin_page(PAGE)
        more, _ = story.place(CONTENT)
        story.element_positions(record)
        story.draw(device)
        writer.end_page()
        page += 1
    return page


def _draw_grid(page, rect):
    """Faint 5 mm squares, like squared exam paper."""
    shape = page.new_shape()
    x = rect.x0
    while x <= rect.x1 + 0.1:
        shape.draw_line((x, rect.y0), (x, rect.y1))
        x += GRID_STEP
    y = rect.y0
    while y <= rect.y1 + 0.1:
        shape.draw_line((rect.x0, y), (rect.x1, y))
        y += GRID_STEP
    shape.finish(color=GRID_LINE, width=0.4)
    shape.draw_rect(rect)
    shape.finish(color=GRID_EDGE, width=0.6)
    shape.commit(overlay=False)


def _stamp_footer(pdf_bytes, grids=()):
    doc = pymupdf.open(stream=pdf_bytes, filetype='pdf')
    font = pymupdf.Font(fontfile=str(FONT_DIR / 'Inter-Regular.ttf'))
    for index, page in enumerate(doc, start=1):
        text = f'MathKG · {index} / {doc.page_count}'
        width = font.text_length(text, fontsize=8.5)
        # The Story content leaves its own coordinate transform open; wrap it
        # so the footer and the grids are drawn in plain page coordinates.
        page.wrap_contents()
        for number, rect in grids:
            if number == index - 1:
                # Whole squares only, so the right edge is a full line.
                cols = max(1, int(rect.width // GRID_STEP))
                rows = max(1, int(rect.height // GRID_STEP))
                _draw_grid(page, pymupdf.Rect(
                    rect.x0, rect.y0, rect.x0 + cols * GRID_STEP, rect.y0 + rows * GRID_STEP,
                ))
        writer = pymupdf.TextWriter(page.rect, color=(0.28, 0.33, 0.41))
        writer.append(((page.rect.width - width) / 2, page.rect.height - 24), text, font=font, fontsize=8.5)
        writer.write_text(page)
    out = doc.tobytes(garbage=3, deflate=True)
    doc.close()
    return out


def render_test_pdf(test):
    """PDF bytes for a GeneratedTest payload."""
    archive = pymupdf.Archive(str(FONT_DIR))
    buffer = io.BytesIO()
    writer = pymupdf.DocumentWriter(buffer)
    grids = []
    page = 0
    for variant in test.get('variants', []):
        page = _write_section(writer, _variant_html(test, variant), archive, page, grids)
    _write_section(writer, _key_html(test), archive, page, [])
    writer.close()
    return _stamp_footer(buffer.getvalue(), grids)
