"""Print a MathKG advert on every downloaded PDF.

Each page keeps its size. The original page is shrunk a little and placed
at the top, and a short band at the bottom says what the site offers, gives
its address and carries a QR code to it. A very faint «MathKG» runs across
the page as a watermark.

The original files are never changed: pages are stamped when they are
downloaded, and the result is cached on local disk by file contents,
``STAMP_VERSION`` and who downloaded it.

A signed-in teacher's copy also names them («Жүктөгөн: aigul (ai***@gmail.com),
08.11.2026»), which discourages reposting. The e-mail is masked so a
reposted page does not leak a full address.
"""

import hashlib
import io
import logging
import math
import os
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

import pymupdf
import segno
from django.conf import settings

logger = logging.getLogger(__name__)

STAMP_VERSION = '1'
FONT_DIR = Path(__file__).resolve().parent / 'generators' / 'fonts' / 'test-pdf'
CACHE_DIR = Path(tempfile.gettempdir()) / 'mathkg-stamped'

NAVY = (0.114, 0.208, 0.341)       # 1D3557, the deck house navy
MUTED = (0.29, 0.353, 0.44)        # 4A5A70
RULE = (0.80, 0.84, 0.89)
MARK = (0.114, 0.208, 0.341)
LEVELS = ((0.0, 0.478, 0.353), (0.659, 0.267, 0.0), (0.141, 0.255, 0.549))

TAGLINE = 'MathKG: 1–11-класстар үчүн даяр сабактар, иш барактар жана тесттер'
CALL = 'Дагы көп материал жана тест түзүү: {host}'


def site_address():
    """``mathkg.com`` style host for print, and the full URL for the QR code."""
    url = (getattr(settings, 'SITE_URL', '') or 'https://mathkg.com').strip().rstrip('/')
    host = urlsplit(url).netloc or url
    if host.startswith('www.'):
        host = host[4:]
    return host, url + '/'


def _fonts():
    return (
        pymupdf.Font(fontfile=str(FONT_DIR / 'Inter-Regular.ttf')),
        pymupdf.Font(fontfile=str(FONT_DIR / 'Inter-Bold.ttf')),
    )


def _fit(font, text, size, width):
    """Largest font size up to ``size`` that keeps ``text`` within ``width``."""
    length = font.text_length(text, fontsize=size)
    if length <= width:
        return size
    return max(4.0, size * width / length)


def _draw_qr(page, rect, url):
    qr = segno.make(url, error='l', micro=False)
    matrix = [list(row) for row in qr.matrix]
    count = len(matrix)
    cell = rect.width / count
    shape = page.new_shape()
    for y, row in enumerate(matrix):
        x = 0
        while x < count:
            if not row[x]:
                x += 1
                continue
            start = x
            while x < count and row[x]:
                x += 1
            shape.draw_rect(pymupdf.Rect(
                rect.x0 + start * cell, rect.y0 + y * cell,
                rect.x0 + x * cell, rect.y0 + (y + 1) * cell,
            ))
    shape.finish(color=None, fill=(0, 0, 0), width=0)
    shape.commit()


def _band(page, band, regular, bold, host, url, owner=''):
    """The advert along the bottom edge of the page."""
    pad = band.height * 0.09
    page.draw_line(
        pymupdf.Point(band.x0 + pad * 2, band.y0 + 0.5),
        pymupdf.Point(band.x1 - pad * 2, band.y0 + 0.5),
        color=RULE, width=0.6,
    )
    qr_side = band.height - pad * 2
    qr_rect = pymupdf.Rect(band.x1 - pad * 2 - qr_side, band.y0 + pad, band.x1 - pad * 2, band.y1 - pad)
    _draw_qr(page, qr_rect, url)

    # Three small level pills, the same mark as on the decks and worksheets.
    pill_w, pill_h = band.height * 0.07, band.height * 0.42
    left = band.x0 + pad * 2
    top = band.y0 + (band.height - pill_h) / 2
    for i, colour in enumerate(LEVELS):
        x = left + i * pill_w * 1.9
        page.draw_rect(
            pymupdf.Rect(x, top, x + pill_w, top + pill_h),
            color=None, fill=colour, radius=0.5,
        )
    text_left = left + pill_w * 6.5
    width = qr_rect.x0 - pad * 2 - text_left

    lines = [(TAGLINE, bold, NAVY), (CALL.format(host=host), regular, NAVY)]
    if owner:
        lines.append((owner, regular, MUTED))
    size = min(band.height * (0.27 if len(lines) == 2 else 0.235), 10.0)
    step = size * 1.2
    baseline = band.y0 + (band.height - step * len(lines)) / 2 + size * 0.95
    for text, font, colour in lines:
        writer = pymupdf.TextWriter(page.rect)
        writer.append(pymupdf.Point(text_left, baseline), text, font=font, fontsize=_fit(font, text, size, width))
        writer.write_text(page, color=colour)
        baseline += step
    page.insert_link({
        'kind': pymupdf.LINK_URI, 'from': pymupdf.Rect(text_left, band.y0, qr_rect.x1, band.y1), 'uri': url,
    })


def _stamp_page(page, source, index, regular, bold, host, url, owner=''):
    """Draw ``source[index]`` on ``page`` (same size) with the band and watermark."""
    rect = page.rect
    # Tall enough for a QR code about 1 cm wide on an A4 page.
    band_h = max(16.0, min(36.0, rect.height * 0.058))
    content_w = rect.width * (rect.height - band_h) / rect.height
    content = pymupdf.Rect(
        (rect.width - content_w) / 2, 0,
        (rect.width + content_w) / 2, rect.height - band_h,
    )
    page.show_pdf_page(content, source, index)
    # Drawn over the content with low opacity: most pages paint a white
    # background that would hide anything below it.
    text = 'MathKG'
    size = math.hypot(content.width, content.height) * 0.11
    length = bold.text_length(text, fontsize=size)
    centre = pymupdf.Point((content.x0 + content.x1) / 2, (content.y0 + content.y1) / 2)
    angle = math.degrees(math.atan2(content.height, content.width))
    writer = pymupdf.TextWriter(page.rect, opacity=0.06, color=MARK)
    writer.append(pymupdf.Point(centre.x - length / 2, centre.y + size * 0.35), text, font=bold, fontsize=size)
    writer.write_text(page, morph=(centre, pymupdf.Matrix(1, 1).prerotate(angle)))
    _band(page, pymupdf.Rect(0, rect.height - band_h, rect.width, rect.height), regular, bold, host, url, owner)


def _cells(layout, rect):
    """(cell rect, rotation) for each copy printed on one sheet.

    The A5 files hold two portrait halves, each a landscape page turned on
    its side; the A6 files hold four quarters. Every copy gets its own band,
    so each one still carries the advert after the sheet is cut.
    """
    w, h = rect.width, rect.height
    if layout == 'a5':
        return [(pymupdf.Rect(0, 0, w / 2, h), 270), (pymupdf.Rect(w / 2, 0, w, h), 270)]
    if layout == 'a6':
        return [
            (pymupdf.Rect(0, 0, w / 2, h / 2), 0), (pymupdf.Rect(w / 2, 0, w, h / 2), 0),
            (pymupdf.Rect(0, h / 2, w / 2, h), 0), (pymupdf.Rect(w / 2, h / 2, w, h), 0),
        ]
    return [(rect, 0)]


def layout_for(name):
    stem = Path(str(name)).stem.lower()
    for layout in ('a5', 'a6'):
        if stem.endswith('-' + layout):
            return layout
    return 'single'


def stamp_pdf(data, layout='single', owner=''):
    """Return ``data`` (PDF bytes) with the advert band and watermark.

    ``owner`` is an extra line naming who downloaded this copy.
    """
    host, url = site_address()
    regular, bold = _fonts()
    source = pymupdf.open(stream=data, filetype='pdf')
    out = pymupdf.open()
    for index in range(source.page_count):
        rect = source[index].rect
        sheet_layout = layout if rect.width > rect.height else 'single'
        page = out.new_page(width=rect.width, height=rect.height)
        for cell, rotation in _cells(sheet_layout, rect):
            if sheet_layout == 'single':
                _stamp_page(page, source, index, regular, bold, host, url, owner)
                continue
            # Lift the copy out upright, stamp it, and put it back in place.
            upright = pymupdf.open()
            size = (cell.height, cell.width) if rotation else (cell.width, cell.height)
            piece = upright.new_page(width=size[0], height=size[1])
            piece.show_pdf_page(piece.rect, source, index, clip=cell, rotate=rotation)
            stamped = pymupdf.open()
            _stamp_page(
                stamped.new_page(width=size[0], height=size[1]),
                upright, 0, regular, bold, host, url, owner,
            )
            page.show_pdf_page(cell, stamped, 0, rotate=-rotation)
    metadata = dict(source.metadata or {})
    metadata.update({'creator': 'MathKG', 'producer': f'MathKG ({host})'})
    out.set_metadata({k: v for k, v in metadata.items() if k in (
        'title', 'author', 'subject', 'keywords', 'creator', 'producer',
    ) and v})
    buffer = io.BytesIO()
    out.save(buffer, garbage=3, deflate=True)
    source.close()
    out.close()
    return buffer.getvalue()


CACHE_LIMIT = 3000


def mask_email(email):
    """``aigul.asanova@gmail.com`` → ``ai***@gmail.com``: enough to trace, not to spam."""
    local, _, domain = (email or '').partition('@')
    if not domain:
        return ''
    return f'{local[:2]}***@{domain}'


def owner_line(user, today):
    """«Жүктөгөн: aigul (ai***@gmail.com), 08.11.2026» for a signed-in user."""
    if user is None or not getattr(user, 'is_authenticated', False):
        return ''
    who = user.username or ''
    email = mask_email(user.email)
    if email:
        who = f'{who} ({email})' if who else email
    return f'Жүктөгөн: {who}, {today:%d.%m.%Y}. Бул нусканы башка жакка жарыялабаңыз.'


def _cache_path(name, data, owner):
    digest = hashlib.sha1(data).hexdigest()[:16]
    host, _ = site_address()
    key = hashlib.sha1(f'{STAMP_VERSION}|{host}|{digest}|{owner}'.encode()).hexdigest()[:20]
    return CACHE_DIR / f'{key}-{Path(name).name}'


def _prune_cache():
    """Keep the cache from growing without end: drop the oldest files."""
    try:
        files = sorted(CACHE_DIR.glob('*.pdf'), key=lambda path: path.stat().st_mtime)
    except OSError:
        return
    for path in files[:max(0, len(files) - CACHE_LIMIT)]:
        try:
            path.unlink()
        except OSError:
            pass


def stamped_download(file_handle, name, owner=''):
    """A binary handle to serve for ``name``.

    PDFs come back stamped (with ``owner`` as an extra line); anything else,
    or a PDF that cannot be read, comes back unchanged so a download never
    fails because of the advert.
    """
    if not str(name).lower().endswith('.pdf'):
        return file_handle
    try:
        data = file_handle.read()
    finally:
        file_handle.close()
    cached = _cache_path(name, data, owner)
    try:
        return cached.open('rb')
    except OSError:
        pass
    try:
        stamped = stamp_pdf(data, layout_for(name), owner)
    except Exception:  # A broken PDF is still served as it is.
        logger.exception('Could not stamp %s', name)
        return io.BytesIO(data)
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = cached.with_name(f'{cached.name}.{os.getpid()}.part')
        tmp.write_bytes(stamped)
        tmp.replace(cached)
        _prune_cache()
    except OSError:
        logger.warning('Could not cache stamped %s', name)
    return io.BytesIO(stamped)
