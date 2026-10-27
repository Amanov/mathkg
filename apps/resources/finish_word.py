"""Replace the maze finish word with «МААРА».

«МАРА» and a leftover «МАРЕ» are the same label. The dative is part of
that word («МАРАга», «МАРЕге»), so those become «МААРАга». A different
word that only contains the letters, such as «мараттык», is left alone.

Migration 0051 rewrites «МАРЕ» to «МАРА» and checks the recorded hash, so
this pass is a separate rewrite. It does not change ``pack_pdf.rewrite_pdf``.
"""

from __future__ import annotations

import hashlib
import html
import io
import os
import re
import zipfile
from pathlib import Path

import pymupdf

_LETTERS = 'A-Za-zА-Яа-яЁёӨөҮүҢң'
_SUFFIX = r'(?:га|ге|нын|нин|ны|ни|да|де|дан|ден|менен|дай|дей)'
_FINISH = re.compile(
    rf'(?<![{_LETTERS}])'
    rf'(МАРЕ|МАРА|Маре|Мара|маре|мара)'
    rf'({_SUFFIX})?'
    rf'(?![{_LETTERS}])'
)
# Front-vowel endings on «МАРЕ» follow the back vowel in «МААРА».
_BACK = {
    'ге': 'га',
    'нин': 'нын',
    'ни': 'ны',
    'де': 'да',
    'ден': 'дан',
    'дей': 'дай',
}
_STEM = {
    'МАРЕ': 'МААРА',
    'МАРА': 'МААРА',
    'Маре': 'Маара',
    'Мара': 'Маара',
    'маре': 'маара',
    'мара': 'маара',
}

_MANIFEST = Path(__file__).resolve().parent / 'data' / 'finish_word_manifest.json'
_A_P = re.compile(r'(<a:p(?:\s[^>]*)?>)(.*?)(</a:p>)', re.DOTALL)
_A_T = re.compile(r'(<a:t(?:\s[^>]*)?>)(.*?)(</a:t>)', re.DOTALL)
_SLIDE_PART = re.compile(r'\bppt/slides/slide\d+\.xml$')


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def empty_counts():
    return {'mara': 0, 'maraga': 0, 'mare': 0, 'marege': 0, 'other': 0}


def _add(total, part):
    for key, value in part.items():
        total[key] = total.get(key, 0) + value


def _rewrite_token(stem: str, suffix: str) -> str:
    written = _STEM[stem]
    if stem.lower() == 'маре':
        suffix = _BACK.get(suffix, suffix)
    return written + suffix


def replace_finish(text: str) -> tuple[str, dict]:
    """Return the text and how many finish-word tokens changed."""
    counts = empty_counts()

    def sub(match):
        stem, suffix = match.group(1), match.group(2) or ''
        key = stem.lower()
        if key == 'мара' and suffix == 'га':
            counts['maraga'] += 1
        elif key == 'мара' and suffix == '':
            counts['mara'] += 1
        elif key == 'маре' and suffix == 'ге':
            counts['marege'] += 1
        elif key == 'маре' and suffix == '':
            counts['mare'] += 1
        else:
            counts['other'] += 1
        return _rewrite_token(stem, suffix)

    return _FINISH.sub(sub, text), counts


def _rgb(color: int) -> tuple[float, float, float]:
    from apps.resources.pack_pdf import _rgb as pack_rgb
    return pack_rgb(color)


def rewrite_pdf(data: bytes) -> tuple[bytes, dict]:
    """Replace finish-word runs. Unchanged bytes are returned as they were."""
    from apps.resources.pack_pdf import _font_file

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
                        updated, part = replace_finish(original)
                        if updated == original:
                            continue
                        _add(counts, part)
                        edits.append((span, updated))
            if not edits:
                continue
            changed = True
            for span, _updated in edits:
                page.add_redact_annot(pymupdf.Rect(span['bbox']), fill=None)
            page.apply_redactions(
                images=pymupdf.PDF_REDACT_IMAGE_NONE,
                graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                text=pymupdf.PDF_REDACT_TEXT_REMOVE,
            )
            for span, updated in edits:
                font_path = _font_file(span['font'])
                page.insert_text(
                    span['origin'],
                    updated,
                    fontsize=span['size'],
                    fontname='finish-' + font_path.stem,
                    fontfile=str(font_path),
                    color=_rgb(span['color']),
                )
        if not changed:
            return data, counts
        doc.subset_fonts()
        return doc.tobytes(deflate=True, garbage=3), counts
    finally:
        doc.close()


def _xml_escape(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _rewrite_runs(texts: list[str], counts: dict) -> list[str]:
    from apps.resources.kyrgyz_text import _redistribute

    joined = ''.join(texts)
    updated, part = replace_finish(joined)
    if updated == joined:
        return texts
    _add(counts, part)
    if len(texts) == 1:
        return [updated]
    return _redistribute(texts, updated)


def _rewrite_xml(xml: str, counts: dict) -> str:
    def replacer(match):
        inner = match.group(2)
        runs = list(_A_T.finditer(inner))
        if not runs:
            return match.group(0)
        texts = [html.unescape(run.group(2)) for run in runs]
        new_texts = _rewrite_runs(texts, counts)
        if new_texts == texts:
            return match.group(0)
        rebuilt = inner
        for run, new_text in zip(reversed(runs), reversed(new_texts)):
            original = html.unescape(run.group(2))
            if new_text == original:
                continue
            rebuilt = rebuilt[: run.start(2)] + _xml_escape(new_text) + rebuilt[run.end(2) :]
        return match.group(1) + rebuilt + match.group(3)

    return _A_P.sub(replacer, xml)


def rewrite_pptx(data: bytes) -> tuple[bytes, dict]:
    """Replace the finish word on slides. Other parts stay byte for byte."""
    counts = empty_counts()
    source = io.BytesIO(data)
    with zipfile.ZipFile(source) as zin:
        replacements = {}
        for info in zin.infolist():
            if not _SLIDE_PART.search(info.filename):
                continue
            raw = zin.read(info)
            try:
                xml = raw.decode('utf-8')
            except UnicodeDecodeError:
                continue
            updated = _rewrite_xml(xml, counts)
            if updated != xml:
                replacements[info.filename] = updated.encode('utf-8')
        if not replacements:
            return data, counts
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w', allowZip64=True) as zout:
            for info in zin.infolist():
                payload = replacements.get(info.filename, zin.read(info))
                cloned = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
                cloned.compress_type = info.compress_type
                cloned.external_attr = info.external_attr
                cloned.internal_attr = info.internal_attr
                cloned.flag_bits = info.flag_bits & ~0x8
                cloned.create_system = info.create_system
                zout.writestr(cloned, payload)
        return out.getvalue(), counts


def load_manifest():
    import json
    return json.loads(_MANIFEST.read_text(encoding='utf-8'))


def _rewrite_bytes(path: Path, data: bytes):
    if path.suffix.lower() == '.pdf':
        return rewrite_pdf(data)
    if path.suffix.lower() == '.pptx':
        return rewrite_pptx(data)
    return data, empty_counts()


def refresh_finish_media(media_root):
    """Rewrite a volume file only when its sha256 is still the recorded old hash."""
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
        rewritten, _counts = _rewrite_bytes(path, current)
        if sha256_bytes(rewritten) != entry['new']:
            totals['rejected'] += 1
            continue
        temporary = path.with_name(path.name + '.finish-tmp')
        try:
            temporary.write_bytes(rewritten)
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()
        totals['updated'] += 1
    print('finish word: ' + ' '.join(f'{name}={count}' for name, count in totals.items()))
    return totals
