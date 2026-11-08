"""Render a generated test paper to PDF with PyMuPDF only.

The earlier renderer used WeasyPrint, which loads Pango, GObject and
HarfBuzz from the operating system when the request arrives. On Railway
those libraries were missing from the linker path, so the download of a
freshly made test ended in «Server Error (500)». PyMuPDF ships its own
layout engine inside the wheel and needs nothing from the system, so the
same code works on a laptop, in the tests and in production.

Each variant starts on a new page; the answer key comes last, on its own
page, so a teacher can print the questions without the answers.
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

CSS = f"""
@font-face {{ font-family: {FONT_FAMILY}; src: url(Inter-Regular.ttf); }}
@font-face {{ font-family: {FONT_FAMILY}; src: url(Inter-Bold.ttf); font-weight: bold; }}
* {{ font-family: {FONT_FAMILY}; }}
body {{ font-size: 11pt; color: {INK}; line-height: 1.35; }}
p {{ margin: 0 0 3pt 0; }}
.brand {{ font-weight: bold; color: {ACCENT}; font-size: 10pt; margin-bottom: 2pt; }}
.title {{ font-weight: bold; color: {NAVY}; font-size: 15pt; margin-bottom: 4pt; }}
.paper-title {{ font-weight: bold; font-size: 12.5pt; margin-bottom: 2pt; }}
.meta {{ color: {MUTED}; font-size: 9.5pt; }}
.variant {{ font-weight: bold; font-size: 12.5pt; margin-top: 8pt; }}
.name {{ font-size: 10.5pt; margin-top: 4pt; margin-bottom: 10pt; }}
.q {{ margin-top: 9pt; margin-bottom: 0; }}
.num {{ font-weight: bold; color: {NAVY}; }}
.pts {{ color: {MUTED}; font-size: 9pt; }}
.opt {{ margin: 1pt 0 0 16pt; }}
.letter {{ font-weight: bold; }}
.line {{ color: {MUTED}; margin: 7pt 0 0 16pt; }}
.box {{ color: {MUTED}; font-size: 9pt; margin: 4pt 0 0 16pt; }}
.total {{ font-weight: bold; margin-top: 12pt; }}
.note {{ color: {MUTED}; font-size: 10pt; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 6pt; }}
th {{ background-color: #eef2f7; font-weight: bold; text-align: left; font-size: 9.5pt; padding: 3pt 4pt; border: 1px solid #cbd5e1; }}
td {{ font-size: 9.5pt; padding: 3pt 4pt; border: 1px solid #cbd5e1; vertical-align: top; }}
.sum td {{ font-weight: bold; background-color: #f8f7f4; }}
.worked {{ color: {MUTED}; font-size: 8.5pt; }}
"""

WRITE_LINE = '_' * 62


def _e(value):
    return html.escape(str(value if value is not None else ''))


def _header(test):
    parts = ['<p class="brand">MathKG</p>']
    if test.get('title'):
        parts.append(f'<p class="paper-title">{_e(test["title"])}</p>')
    parts.append(f'<p class="title">{_e(test.get("grade_label"))} · {_e(test.get("test_type_label"))} тест</p>')
    parts.append(f'<p class="meta">Темалар: {_e(test.get("topics_label"))}</p>')
    meta = [_e(test.get('created_label'))]
    if test.get('mix_label'):
        meta.append(f'Деңгээл: {_e(test["mix_label"])}')
    parts.append(f'<p class="meta">{" · ".join(m for m in meta if m)}</p>')
    if test.get('formats_label'):
        parts.append(f'<p class="meta">Суроолордун түрү: {_e(test["formats_label"])}</p>')
    if test.get('show_timer'):
        parts.append(f'<p class="meta">Убакыт: {_e(test.get("duration_minutes"))} мүнөт</p>')
    return ''.join(parts)


def _question(q):
    out = [
        f'<p class="q"><span class="num">{_e(q.get("number"))}.</span> {_e(q.get("text"))} '
        f'<span class="pts">({_e(q.get("points"))} балл)</span></p>'
    ]
    fmt = q.get('format')
    if q.get('figure'):
        out.append('<p class="box">[ Сүрөттү ушул жерге тарт ]</p>')
    if fmt == 'matching':
        rows = []
        left, right = q.get('left') or [], q.get('right') or []
        for i in range(max(len(left), len(right))):
            a = left[i] if i < len(left) else None
            b = right[i] if i < len(right) else None
            cell_a = f'<span class="letter">{_e(a["n"])})</span> {_e(a["text"])}' if a else ''
            cell_b = f'<span class="letter">{_e(b["letter"])})</span> {_e(b["text"])}' if b else ''
            rows.append(f'<tr><td>{cell_a}</td><td>{cell_b}</td></tr>')
        out.append(f'<table>{"".join(rows)}</table>')
        out.append(f'<p class="line">Жооп: {"_" * 40}</p>')
    elif q.get('options'):
        for opt in q['options']:
            out.append(f'<p class="opt"><span class="letter">{_e(opt["letter"])})</span> {_e(opt["text"])}</p>')
    elif q.get('line_slots'):
        for _ in q['line_slots']:
            out.append(f'<p class="line">{WRITE_LINE}</p>')
    else:
        out.append(f'<p class="line">Жооп: {"_" * 40}</p>')
    return ''.join(out)


def _variant_html(test, variant):
    body = [_header(test)]
    body.append(f'<p class="variant">Вариант {_e(variant.get("number"))}</p>')
    body.append('<p class="name">Аты-жөнү ______________________________   Класс __________</p>')
    for q in variant.get('questions', []):
        body.append(_question(q))
    body.append(f'<p class="total">Жалпы: {_e(variant.get("points"))} балл</p>')
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


def _write_section(writer, html_text, archive):
    story = pymupdf.Story(html=html_text, user_css=CSS, archive=archive)
    more = True
    while more:
        device = writer.begin_page(PAGE)
        more, _ = story.place(CONTENT)
        story.draw(device)
        writer.end_page()


def _stamp_footer(pdf_bytes):
    doc = pymupdf.open(stream=pdf_bytes, filetype='pdf')
    font = pymupdf.Font(fontfile=str(FONT_DIR / 'Inter-Regular.ttf'))
    for index, page in enumerate(doc, start=1):
        text = f'MathKG · {index} / {doc.page_count}'
        width = font.text_length(text, fontsize=8.5)
        # The Story content leaves its own coordinate transform open; wrap it
        # so the footer is drawn in plain page coordinates.
        page.wrap_contents()
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
    for variant in test.get('variants', []):
        _write_section(writer, _variant_html(test, variant), archive)
    _write_section(writer, _key_html(test), archive)
    writer.close()
    return _stamp_footer(buffer.getvalue())
