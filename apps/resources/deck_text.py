"""Edit lesson-deck text without rebuilding the PowerPoint package.

``Presentation.save()`` rewrites the whole package. This module only
replaces the characters inside existing ``a:t`` nodes (and ``dc:title``).
Pictures, charts, slide order and every other byte of XML stay as they
were. Unchanged zip entries are copied back in the same compression
format; their decompressed bytes are identical.
"""

from __future__ import annotations

import hashlib
import html
import io
import json
import os
import re
import zipfile
from pathlib import Path

TYPO_OLD = 'Турдуу пикирлер учун'
TYPO_NEW = 'Түрдүү пикирлер үчүн'

# Exact ``a:t`` text only. Master placeholders and invented card names are
# not in this map, so they stay as authored.
ENGLISH_REPLACEMENTS = {
    'Answer': 'Жооп',
    'START': 'Башта',
    'START!': 'Башта!',
    'one thousand': 'миң',
    'Find someone to challenge!': 'Атаандаш тап!',
    'The person who lost last (or lowest number)\t chooses the attribute to compare.': (
        'Акыркы жолу утулган (же эң кичине сан)\t салыштыра турган белгини тандайт.'
    ),
    'Find out who wins! (If it\u2019s a draw the other person chooses an attribute.)': (
        'Ким утканын бил! (Тең чыкса, экинчиси белгини тандайт.)'
    ),
    'Swap cards and find someone to challenge!': 'Карталарды алмаштыр да, атаандаш тап!',
    'Record the amount of wins you get!': 'Канча жолу утканыңды жазып тур!',
    'If you lost last, ': 'Эгер акыркы жолу утулсаң, ',
    'you can\u2019t use that same attribute ': 'ошол эле белгини колдоно албайсың ',
    'with your new card!': 'жаңы картаң менен!',
    'Split the cards in your groups. Only look at your top card.': (
        'Карталарды топто бөлүшкүлө. Үстүнкү картаңарды гана карагыла.'
    ),
    'Youngest player chooses the attribute to compare first.': (
        'Эң кичүү оюнчу биринчи салыштыра турган белгини тандайт.'
    ),
    'Find out who wins! (If it\u2019s a draw the person to the left chooses an attribute.)': (
        'Ким утканын бил! (Тең чыкса, сол жактагы белгини тандайт.)'
    ),
    'Whoever has the highest value gets the other cards.': (
        'Эң чоң мааниге ээ оюнчу калган карталарды алат.'
    ),
    'Continue until one player has all the cards!': 'Бир оюнчу бардык картаны алганча уланткыла!',
    'Hard Work': 'Эмгек',
    'Teamwork': 'Кызматташтык',
    'Persistence': 'Туруктуулук',
    'Mindset': 'Ой жүгүртүү',
    'Questions?': 'Суроолор?',
    'Comments?': 'Пикирлер?',
    'Suggestions?': 'Сунуштар?',
    '\u2026or have you found a mistake!?': '\u2026же ката таптыңызбы?',
    'Any feedback would be appreciated ': 'Ар кандай пикирге ыраазыбыз ',
    'Please feel free to email:': 'Кат жазсаңыз болот:',
}

_GRADE_WORD = r'\d{1,2}(?:[–—−-]\d{1,2})?-класс'
# A whole run that is only the grade chip (``6-класс ›``, ``5–6-класс``,
# ``6-класс · Математика``).
_GRADE_ONLY = re.compile(rf'^\s*(?:{_GRADE_WORD})(?:\s*[›·])?(?:\s*Математика)?\s*$')
# Leading breadcrumb ``1-класс › topic``.
_GRADE_PREFIX = re.compile(rf'^(?:{_GRADE_WORD})\s*[›·]\s*')
# Trailing title tag ``topic · 7–8-класс`` or ``topic - 5-6-класс``.
_GRADE_TRAIL = re.compile(rf'\s*[·\-–—]\s*(?:{_GRADE_WORD})\s*$')
_CAMBRIDGE = re.compile(
    r'Cambridge(?:\s+Stage|\s+Primary)?\s+\d+[A-Za-z]*',
)

_A_P = re.compile(r'(<a:p(?:\s[^>]*)?>)(.*?)(</a:p>)', re.DOTALL)
_A_T = re.compile(r'(<a:t(?:\s[^>]*)?>)(.*?)(</a:t>)', re.DOTALL)
_DC_TITLE = re.compile(r'(<dc:title(?:\s[^>]*)?>)(.*?)(</dc:title>)', re.DOTALL)

_SLIDE_PART = re.compile(r'^ppt/(?:slides|notesSlides)/.+\.xml$')
_MANIFEST = Path(__file__).resolve().parent / 'data' / 'deck_text_manifest.json'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _xml_escape(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _replace_phrase(texts, old, new):
    """Replace ``old`` even when it is split across several runs.

    The replacement sits on the first overlapping run. Middle runs become
    empty (the ``a:t`` node stays). The tail after the phrase stays on the
    last overlapping run.
    """
    out = list(texts)
    found = 0
    while True:
        joined = ''.join(out)
        start = joined.find(old)
        if start < 0:
            return out, found
        end = start + len(old)
        spans = []
        pos = 0
        for index, text in enumerate(out):
            spans.append((pos, pos + len(text), index))
            pos += len(text)
        overlapping = [index for begin, finish, index in spans if finish > start and begin < end]
        first = overlapping[0]
        last = overlapping[-1]
        begin, _, _ = spans[first]
        last_begin = spans[last][0]
        prefix = out[first][: start - begin]
        suffix = out[last][end - last_begin :]
        if first == last:
            out[first] = prefix + new + suffix
        else:
            out[first] = prefix + new
            for index in overlapping[1:-1]:
                out[index] = ''
            out[last] = suffix
        found += 1


def _tidy_cambridge(text: str) -> str:
    updated = _CAMBRIDGE.sub('', text)
    if updated == text:
        return text
    updated = re.sub(r'\(\s*,\s*', '(', updated)
    updated = re.sub(r'\(\s*\)', '', updated)
    updated = re.sub(r'[;,]\s*\.', '.', updated)
    updated = re.sub(r';\s+\(', ' (', updated)
    updated = re.sub(r'[ \t]{2,}', ' ', updated)
    updated = re.sub(r' +([,.;:»])', r'\1', updated)
    updated = re.sub(r'\(\s+', '(', updated)
    return updated.strip()


def _apply_grade(text: str) -> str:
    if _GRADE_ONLY.match(text):
        return ''
    updated = _GRADE_PREFIX.sub('', text)
    updated = _GRADE_TRAIL.sub('', updated)
    if 'Cambridge' in updated:
        updated = _tidy_cambridge(updated)
    return updated


def edit_runs(texts, *, typo=False, grade=False, english=False, kyrgyz=False):
    """Return new run strings and a count of each fix that fired."""
    counts = {'typo': 0, 'grade': 0, 'english': 0, 'kyrgyz': 0}
    out = list(texts)
    if typo:
        out, found = _replace_phrase(out, TYPO_OLD, TYPO_NEW)
        counts['typo'] += found
    for index, text in enumerate(out):
        updated = text
        if english and updated in ENGLISH_REPLACEMENTS:
            updated = ENGLISH_REPLACEMENTS[updated]
            counts['english'] += 1
        if grade:
            graded = _apply_grade(updated)
            if graded != updated:
                counts['grade'] += 1
                updated = graded
        out[index] = updated
    if kyrgyz:
        from apps.resources.kyrgyz_text import apply_kyrgyz_runs

        out, kyrgyz_counts = apply_kyrgyz_runs(out)
        counts['kyrgyz'] += kyrgyz_counts['total']
    return out, counts


def _edit_xml(xml: str, **flags) -> tuple[str, dict]:
    counts = {'typo': 0, 'grade': 0, 'english': 0, 'kyrgyz': 0}

    def take(part_counts):
        for key in counts:
            counts[key] += part_counts[key]

    def rewrite_container(pattern, source):
        changed = False

        def replacer(match):
            nonlocal changed
            inner = match.group(2)
            runs = list(_A_T.finditer(inner))
            if not runs:
                # dc:title has no a:t children; treat the whole node as one run.
                if pattern is _DC_TITLE:
                    new_texts, part_counts = edit_runs([html.unescape(inner)], **flags)
                    take(part_counts)
                    if new_texts[0] == html.unescape(inner):
                        return match.group(0)
                    changed = True
                    return match.group(1) + _xml_escape(new_texts[0]) + match.group(3)
                return match.group(0)
            texts = [html.unescape(run.group(2)) for run in runs]
            new_texts, part_counts = edit_runs(texts, **flags)
            take(part_counts)
            if new_texts == texts:
                return match.group(0)
            changed = True
            rebuilt = inner
            for run, new_text in zip(reversed(runs), reversed(new_texts)):
                original = html.unescape(run.group(2))
                if new_text == original:
                    continue
                rebuilt = rebuilt[: run.start(2)] + _xml_escape(new_text) + rebuilt[run.end(2) :]
            return match.group(1) + rebuilt + match.group(3)

        updated = pattern.sub(replacer, source)
        return updated, changed

    updated, _ = rewrite_container(_A_P, xml)
    if '<dc:title' in updated:
        updated, _ = rewrite_container(_DC_TITLE, updated)
    return updated, counts


def _is_text_part(name: str) -> bool:
    return bool(_SLIDE_PART.match(name) or name == 'docProps/core.xml')


def rewrite_pptx(data: bytes, *, typo=False, grade=False, english=False, kyrgyz=False) -> tuple[bytes, dict]:
    """Return new package bytes and fix counts.

    When nothing matches, the original bytes are returned unchanged.
    Kyrgyz fixes stay on slides and notes. ``dc:title`` is left alone,
    because resource rows are looked up by the exact title.
    """
    counts = {'typo': 0, 'grade': 0, 'english': 0, 'kyrgyz': 0}
    source = io.BytesIO(data)
    with zipfile.ZipFile(source) as zin:
        proven_token = None
        proven_var = None
        if kyrgyz:
            from apps.resources.kyrgyz_text import collect_proven, paragraph_texts, _PROVEN

            proven_var = _PROVEN
            paragraphs = []
            for info in zin.infolist():
                if not _SLIDE_PART.match(info.filename):
                    continue
                try:
                    xml = zin.read(info).decode('utf-8')
                except UnicodeDecodeError:
                    continue
                paragraphs.extend(paragraph_texts(xml))
            proven_token = proven_var.set(collect_proven(paragraphs))
        try:
            replacements = {}
            for info in zin.infolist():
                if not _is_text_part(info.filename):
                    continue
                raw = zin.read(info)
                try:
                    xml = raw.decode('utf-8')
                except UnicodeDecodeError:
                    continue
                part_kyrgyz = kyrgyz and bool(_SLIDE_PART.match(info.filename))
                updated, part_counts = _edit_xml(
                    xml, typo=typo, grade=grade, english=english, kyrgyz=part_kyrgyz,
                )
                for key in counts:
                    counts[key] += part_counts[key]
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
                    # Bit 3 (data descriptor) is rewritten by ZipFile from the CRC.
                    # Drop the old extra field so a resized XML part does not keep
                    # a stale uncompressed size.
                    cloned.flag_bits = info.flag_bits & ~0x8
                    cloned.create_system = info.create_system
                    zout.writestr(cloned, payload)
            return out.getvalue(), counts
        finally:
            if proven_token is not None:
                proven_var.reset(proven_token)


def load_manifest() -> dict:
    return json.loads(_MANIFEST.read_text(encoding='utf-8'))


def refresh_one(path: Path, entry: dict) -> str:
    """Overwrite ``path`` only when its bytes are still the recorded old deck.

    Returns ``updated``, ``already``, ``missing``, ``foreign`` or ``rejected``.
    A result whose hash is not the recorded new hash is not written.
    """
    if not path.is_file():
        return 'missing'
    current = path.read_bytes()
    digest = sha256_bytes(current)
    if digest == entry['new']:
        return 'already'
    if digest != entry['old']:
        return 'foreign'
    flags = {name: True for name in entry.get('fixes', [])}
    rewritten, _counts = rewrite_pptx(current, **flags)
    if sha256_bytes(rewritten) != entry['new']:
        return 'rejected'
    temporary = path.with_name(path.name + '.decktext-tmp')
    try:
        temporary.write_bytes(rewritten)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return 'updated'


def refresh_media(media_root: Path) -> dict:
    """Apply the manifest to files under ``media_root``. No database writes."""
    manifest = load_manifest()
    totals = {'updated': 0, 'already': 0, 'missing': 0, 'foreign': 0, 'rejected': 0}
    root = Path(media_root)
    for relative, entry in manifest.items():
        outcome = refresh_one(root / relative, entry)
        totals[outcome] += 1
    print(
        'deck text: '
        + ' '.join(f'{name}={count}' for name, count in totals.items())
    )
    return totals
