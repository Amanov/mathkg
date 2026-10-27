"""Rewrite pack-PDF text without redrawing the page.

The mazes were exported from LibreOffice Impress, and the other pack
sheets from the MathKG brand kit. Neither the Impress files nor that
script are in this repository, so the drawing stays as it was printed.
This module only replaces text runs, in the same face, size, colour
and position. A header breadcrumb is right-aligned back to the edge
it already occupied, because those labels sit on the right.

«учун» is left alone. In the symmetry teacher card it means "its tip",
and the other hits are inside words such as «окуучунун».
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pymupdf

from apps.resources.kyrgyz_text import (
    NBSP,
    _DECIMAL,
    _FOREIGN,
    _IRET,
    _STUDENT,
    _THOUSANDS,
    _WORD,
    _cap_like,
    _latin_token,
    _obvious_thousands,
    _skip_decimal,
)

_FONTS = Path(__file__).resolve().parent / 'generators' / 'fonts'
_FONT_FILE = {
    'Inter-Regular': _FONTS / 'Inter-Regular.ttf',
    'Inter-Bold': _FONTS / 'Inter-Bold.ttf',
    'Inter-Italic': _FONTS / 'Inter-Italic.ttf',
    'Carlito-Regular': _FONTS / 'Carlito-Regular.ttf',
}

# «6-класс › Topic» and «4–5-класс › Topic». The topic stays.
_CRUMB = re.compile(
    r'^(\d{1,2}(?:[–—−-]\d{1,2})?-класс)\s*[›>]\s*(\S.*?)\s*$'
)
# The grade chip is its own run, and the topic is the next one.
_CRUMB_ONLY = re.compile(
    r'^(\d{1,2}(?:[–—−-]\d{1,2})?-класс)\s*[›>]\s*$'
)

_MARE = (
    ('МАРЕге', 'МАРАга'),
    ('МАРЕ', 'МАРА'),
)
_ZHEYIL = (
    ('Жейилгени', 'Желгени'),
    ('жейилгени', 'желгени'),
    ('Жейилген', 'Желген'),
    ('жейилген', 'желген'),
    ('Жейилди', 'Желди'),
    ('жейилди', 'желди'),
)

_MANIFEST = Path(__file__).resolve().parent / 'data' / 'pack_pdf_manifest.json'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def empty_counts():
    return {
        'breadcrumb': 0, 'mare': 0, 'zheyil': 0, 'iret': 0,
        'student': 0, 'dukon': 0, 'latin': 0, 'thousands': 0,
        'decimal': 0,
    }


def _font_file(font_name: str) -> Path:
    path = _FONT_FILE.get(font_name)
    if path is not None:
        return path
    lowered = font_name.lower()
    if 'italic' in lowered:
        return _FONT_FILE['Inter-Italic']
    if 'bold' in lowered or 'smbld' in lowered:
        return _FONT_FILE['Inter-Bold']
    return _FONT_FILE['Inter-Regular']


def _replace_count(text, old, new):
    hits = text.count(old)
    if not hits:
        return text, 0
    return text.replace(old, new), hits


def correct_text(text: str) -> tuple[str, dict, str]:
    """Return the corrected run, counts, and ``left`` or ``right`` alignment.

    A breadcrumb keeps the topic and is drawn from the right edge, matching
    the header. Every other edit keeps the original left edge.
    """
    counts = empty_counts()
    align = 'left'
    updated = text
    if _CRUMB_ONLY.match(updated):
        counts['breadcrumb'] += 1
        return '', counts, align
    crumb = _CRUMB.match(updated)
    if crumb:
        updated = crumb.group(2)
        counts['breadcrumb'] += 1
        align = 'right'

    for old, new in _MARE:
        updated, hits = _replace_count(updated, old, new)
        counts['mare'] += hits
    for old, new in _ZHEYIL:
        updated, hits = _replace_count(updated, old, new)
        counts['zheyil'] += hits

    def iret(match):
        return ('И' if match.group(1) == 'И' else 'и') + 'рээт'

    updated, hits = _IRET.subn(iret, updated)
    counts['iret'] += hits

    for old, new in _STUDENT:
        pattern = re.compile(
            rf'(?<![А-Яа-яӨөҮүҢң])({old[0].upper()}{old[1:]}|{old})(?![А-Яа-яӨөҮүҢң])'
        )

        def student(match, replacement=new):
            return _cap_like(match.group(0), replacement)

        updated, hits = pattern.subn(student, updated)
        counts['student'] += hits

    updated, hits = _replace_count(updated, 'дукөн', 'дүкөн')
    counts['dukon'] += hits
    updated, hits = _replace_count(updated, 'Дукөн', 'Дүкөн')
    counts['dukon'] += hits

    def latin(match):
        return _latin_token(match.group(0))

    replaced = _WORD.sub(latin, updated)
    if replaced != updated:
        counts['latin'] += sum(
            1 for old, new in zip(_WORD.findall(updated), _WORD.findall(replaced)) if old != new
        )
        updated = replaced

    def thousands(match):
        token = match.group(0)
        if token.startswith('0,') or not _obvious_thousands(token):
            return token
        counts['thousands'] += 1
        return token.replace(',', NBSP)

    updated = _THOUSANDS.sub(thousands, updated)

    def decimal(match):
        if _skip_decimal(updated, match):
            return match.group(0)
        counts['decimal'] += 1
        return match.group(1) + ',' + match.group(2)

    updated = _DECIMAL.sub(decimal, updated)
    if updated != text and _FOREIGN.search(updated) and not _FOREIGN.search(text):
        raise ValueError('rewrite introduced a non-Kyrgyz letter')
    return updated, counts, align


def _rgb(color: int) -> tuple[float, float, float]:
    return (
        ((color >> 16) & 255) / 255,
        ((color >> 8) & 255) / 255,
        (color & 255) / 255,
    )


def _add(total, part):
    for key, value in part.items():
        total[key] += value


def rewrite_pdf(data: bytes) -> tuple[bytes, dict]:
    """Return new PDF bytes and per-group counts.

    When no run changes, the original bytes are returned. Drawings and
    images are not repainted; only the text inside a changed run is removed
    and written again.
    """
    counts = empty_counts()
    doc = pymupdf.open(stream=data, filetype='pdf')
    try:
        changed = False
        for page in doc:
            edits = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        original = span['text']
                        if not original.strip():
                            continue
                        updated, part, align = correct_text(original)
                        if updated == original:
                            continue
                        _add(counts, part)
                        edits.append((span, updated, align))
            if not edits:
                continue
            changed = True
            for span, _updated, _align in edits:
                rect = pymupdf.Rect(span['bbox'])
                page.add_redact_annot(rect, fill=None)
            page.apply_redactions(
                images=pymupdf.PDF_REDACT_IMAGE_NONE,
                graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                text=pymupdf.PDF_REDACT_TEXT_REMOVE,
            )
            for span, updated, align in edits:
                if not updated:
                    continue
                font_path = _font_file(span['font'])
                size = span['size']
                origin_x, origin_y = span['origin']
                if align == 'right':
                    width = pymupdf.Font(fontfile=str(font_path)).text_length(updated, fontsize=size)
                    origin_x = span['bbox'][2] - width
                page.insert_text(
                    (origin_x, origin_y),
                    updated,
                    fontsize=size,
                    fontname='pack-' + font_path.stem,
                    fontfile=str(font_path),
                    color=_rgb(span['color']),
                )
        if not changed:
            return data, counts
        # The replacement faces are full fonts. Keep only the glyphs this
        # file actually draws, so the pack does not grow by a megabyte.
        doc.subset_fonts()
        return doc.tobytes(deflate=True, garbage=3), counts
    finally:
        doc.close()


def load_manifest():
    import json
    return json.loads(_MANIFEST.read_text(encoding='utf-8'))


def refresh_pdf_media(media_root):
    """Rewrite volume copies whose bytes are still the recorded old PDF."""
    root = Path(media_root)
    manifest = load_manifest()
    totals = {'updated': 0, 'already': 0, 'missing': 0, 'foreign': 0, 'rejected': 0}
    for relative, entry in manifest.items():
        path = root / relative
        if not path.is_file():
            totals['missing'] += 1
            continue
        current = path.read_bytes()
        digest = sha256_bytes(current)
        if digest == entry['new']:
            totals['already'] += 1
            continue
        if digest != entry['old']:
            totals['foreign'] += 1
            continue
        rewritten, _counts = rewrite_pdf(current)
        if sha256_bytes(rewritten) != entry['new']:
            totals['rejected'] += 1
            continue
        temporary = path.with_name(path.name + '.packpdf-tmp')
        try:
            temporary.write_bytes(rewritten)
            temporary.replace(path)
        finally:
            if temporary.exists():
                temporary.unlink()
        totals['updated'] += 1
    print('pack pdf: ' + ' '.join(f'{name}={count}' for name, count in totals.items()))
    return totals
