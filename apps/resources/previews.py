"""First-page previews for topic-page thumbnails.

PDFs are drawn with PyMuPDF. Decks are exported by LibreOffice, which is
what produced the 16:9 slide size these thumbnails already use. The width
is 1100px, matching ``static/img/topic-pages/``.
"""

from __future__ import annotations

import subprocess
import tempfile
from io import BytesIO
from pathlib import Path

import pymupdf
from PIL import Image

PREVIEW_WIDTH = 1100
# Existing thumbnails sit on one of these heights. A render that lands a
# pixel or two away is the same page, so it keeps that canvas.
_HEIGHTS = (778, 619)


def _webp(image: Image.Image) -> bytes:
    if image.mode != 'RGB':
        image = image.convert('RGB')
    width, height = image.size
    if width != PREVIEW_WIDTH:
        height = round(height * PREVIEW_WIDTH / width)
        image = image.resize((PREVIEW_WIDTH, height), Image.Resampling.LANCZOS)
    for target in _HEIGHTS:
        if image.height != target and abs(image.height - target) <= 2:
            image = image.resize((PREVIEW_WIDTH, target), Image.Resampling.LANCZOS)
            break
    buffer = BytesIO()
    image.save(buffer, format='WEBP', quality=80, method=6)
    return buffer.getvalue()


def render_pdf_preview(data: bytes) -> bytes:
    doc = pymupdf.open(stream=data, filetype='pdf')
    try:
        page = doc[0]
        zoom = PREVIEW_WIDTH / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        return _webp(image)
    finally:
        doc.close()


def render_pptx_preview(path: Path) -> bytes:
    """Export the first slide. LibreOffice writes one PNG for a deck."""
    path = Path(path)
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp) / 'profile'
        out = Path(tmp) / 'out'
        out.mkdir()
        subprocess.run(
            [
                'soffice',
                '--headless',
                '--norestore',
                '--nolockcheck',
                f'-env:UserInstallation=file://{profile}',
                '--convert-to',
                'png',
                '--outdir',
                str(out),
                str(path),
            ],
            check=True,
            timeout=180,
            capture_output=True,
        )
        pngs = sorted(out.glob('*.png'))
        if not pngs:
            raise RuntimeError(f'no slide preview for {path.name}')
        return _webp(Image.open(pngs[0]))
