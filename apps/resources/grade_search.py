"""Grade-aware search over topic pages that already carry a grade.

Nothing here assigns a grade. A page is searchable by class only when the
site already prints one:

* a hand-built lesson page uses the badge (or the grade tabs) that page
  renders;
* a flat lesson URL filled by a grade pack uses that pack's badge, which
  is what the page shows;
* a database topic (``/resources/topic/...``) uses the 12-year continuum
  band from ``grade-tags.csv``, which is the badge on those pages;
* anything left uses the menu audit label, the same chip the menu shows.

Pages with none of those are left out. Sections come from the continuum
``area`` column, then from the topic slug or the same URL prefixes the
continuum already uses (``algebra-``, ``data-``, ``probability-``, ...).
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from apps.resources.continuum import DATA_DIR, clean_title

SECTION_ORDER = (
    'Сандар',
    'Пропорция',
    'Алгебра',
    'Геометрия',
    'Дата',
    'Ыктымалдуулук',
)
SECTION_RANK = {name: index for index, name in enumerate(SECTION_ORDER)}

TOPIC_SECTIONS = {
    'number': 'Сандар',
    'proportion': 'Пропорция',
    'algebra': 'Алгебра',
    'geometry': 'Геометрия',
    'statistics': 'Дата',
    'probability': 'Ыктымалдуулук',
}

# The statistics lesson states its own badge in the view. It is not in the
# continuum table.
FIXED_PAGES = {
    '/statistika-ortocho/': {
        'title': 'Орточо, медиана, мода, кулач',
        'label': '6–7 кл.',
        'section': 'Дата',
    },
}

_GRADE_WORD = r'(?:класс|кл\.?|grade)'
_NUM_THEN_WORD = re.compile(
    rf'(?<!\d)(\d{{1,2}})\s*[-–—]?\s*{_GRADE_WORD}(?!\w)',
    re.IGNORECASE,
)
_WORD_THEN_NUM = re.compile(
    rf'(?<!\w){_GRADE_WORD}\s*[-–—]?\s*(\d{{1,2}})(?!\d)',
    re.IGNORECASE,
)

_CACHE = None


def norm_url(url):
    if not url:
        return ''
    url = url.split('?', 1)[0].split('#', 1)[0].strip()
    if not url.startswith('/'):
        url = '/' + url
    if len(url) > 1 and not url.endswith('/'):
        url += '/'
    return url


def parse_grade_query(query):
    """Split «7-класс ондук» into ``(7, 'ондук')``.

    Accepts the forms teachers type: «7-класс», «7 класс», «7класс»,
    «7-кл», «класс 7», «7-grade», «grade 7». A number on its own is not a
    grade. Returns ``(None, query)`` when there is no grade phrase.
    """
    raw = (query or '').strip()
    matches = []
    for pattern in (_NUM_THEN_WORD, _WORD_THEN_NUM):
        for match in pattern.finditer(raw):
            number = int(match.group(1))
            if 1 <= number <= 12:
                matches.append(match)
    if not matches:
        return None, raw

    matches.sort(key=lambda match: (match.start(), -(match.end() - match.start())))
    chosen = []
    last_end = -1
    for match in matches:
        if match.start() < last_end:
            continue
        chosen.append(match)
        last_end = match.end()

    grade = int(chosen[0].group(1))
    text = raw
    for match in reversed(chosen):
        text = text[:match.start()] + ' ' + text[match.end():]
    text = re.sub(r'\s+', ' ', text).strip(' -–—,;')
    return grade, text


def grades_from_label(label):
    """'7 кл.' -> {7}; '6–7 кл.' and '7–9' include every class in the span."""
    numbers = [int(piece) for piece in re.findall(r'\d+', label or '')]
    numbers = [number for number in numbers if 1 <= number <= 12]
    if not numbers:
        return frozenset()
    if len(numbers) == 1:
        return frozenset(numbers)
    return frozenset(range(numbers[0], numbers[-1] + 1))


def section_sort_key(name, root_order=None):
    """The six curriculum sections first, in menu order, then anything else."""
    root_order = root_order or {}
    if name in SECTION_RANK:
        return (0, SECTION_RANK[name], '')
    if name == 'Башка':
        return (2, root_order.get(name, 9999), name)
    return (1, root_order.get(name, 9999), name)


def catalog():
    pages, _index = _cached()
    return pages


def catalog_index():
    _pages, index = _cached()
    return index


def pages_for_search(grade, text):
    """Topic rows whose stored grade includes ``grade`` and whose title,
    section, or path contains ``text`` (empty text keeps every match)."""
    needle = (text or '').strip().lower()
    rows = []
    for page in catalog():
        if grade is not None and grade not in page['grades']:
            continue
        if needle and needle not in page['haystack']:
            continue
        rows.append(_row(page))
    rows.sort(key=lambda row: (section_sort_key(row['breadcrumb'][0] if row['breadcrumb'] else ''), row['title']))
    return rows


def grade_counts(text):
    """How many catalog pages each class has, optionally filtered by text."""
    needle = (text or '').strip().lower()
    counts = defaultdict(int)
    for page in catalog():
        if needle and needle not in page['haystack']:
            continue
        for number in page['grades']:
            counts[number] += 1
    return dict(counts)


# The school classes that get a page of their own at /N-klass/.
GRADE_PAGE_RANGE = range(1, 12)


def grade_page_numbers():
    """Classes 1 to 11 that have at least one topic page, in order."""
    counts = grade_counts('')
    return [number for number in GRADE_PAGE_RANGE if counts.get(number)]


def preview_results(results, limit=8):
    """A short dropdown sample that still shows more than one section."""
    buckets = defaultdict(list)
    for row in results:
        section = row['breadcrumb'][0] if row['breadcrumb'] else ''
        buckets[section].append(row)
    sections = sorted(buckets, key=lambda name: section_sort_key(name))
    picked = []
    while len(picked) < limit and any(buckets.values()):
        for section in sections:
            bucket = buckets[section]
            if not bucket:
                continue
            picked.append(bucket.pop(0))
            if len(picked) >= limit:
                break
    return picked


def _row(page):
    return {
        'title': page['title'],
        'url': page['url'],
        'breadcrumb': list(page['breadcrumb']),
        'grade': page['label'],
    }


def _cached():
    global _CACHE
    if _CACHE is None:
        pages = _build_catalog()
        _CACHE = (pages, {page['url']: page for page in pages})
    return _CACHE


def _build_catalog():
    from django.urls import Resolver404, resolve

    from apps.resources.data.menu_grades import AUDIT_GRADES, _short
    from apps.resources.data.pack_pages import PATH_PAGES, SLUG_PAGES, SPLIT_BADGES

    rows = _grade_rows()
    by_href = {norm_url(row['href']): row for row in rows}
    unanimous = _unanimous_prefixes(rows)
    hand_built = _hand_built()
    bridge_crumbs, bridge_titles = _bridge_meta()
    placeholders = _placeholder_titles()

    candidates = set(by_href) | set(hand_built) | set(FIXED_PAGES)
    for url in AUDIT_GRADES:
        candidates.add(norm_url(url))
    for slug in SLUG_PAGES:
        candidates.add(f'/{slug.strip("/")}/')
    for key in PATH_PAGES:
        candidates.add('/resources/topic/' + '/'.join(key) + '/')

    pages = []
    for url in candidates:
        if not _is_lesson_url(url):
            continue
        try:
            resolve(url)
        except Resolver404:
            continue

        fixed = FIXED_PAGES.get(url)
        hand = hand_built.get(url)
        pack, override = _pack_for(url, SLUG_PAGES, PATH_PAGES, SPLIT_BADGES)
        csv_row = by_href.get(url)
        crumb = ''
        if hand and hand.get('crumb'):
            crumb = hand['crumb']
        elif pack and pack.get('crumb'):
            crumb = pack['crumb']
        elif url in bridge_crumbs:
            crumb = bridge_crumbs[url]

        if fixed:
            label = fixed['label']
        else:
            label = _label_for(url, hand, pack, override, csv_row, AUDIT_GRADES, _short)
        grades = grades_from_label(label)
        if not grades:
            continue

        title = _title_for(url, fixed, hand, csv_row, placeholders, pack, bridge_titles)
        if not title:
            continue

        area = (csv_row or {}).get('area') or ''
        section = fixed['section'] if fixed else _section(url, area.strip(), crumb, unanimous)
        subgroup = ((csv_row or {}).get('subgroup_path') or '').strip()
        breadcrumb = _breadcrumb(section, subgroup, crumb)
        haystack = ' '.join(part for part in (title, section, subgroup, crumb) if part).lower()
        pages.append({
            'title': title,
            'url': url,
            'breadcrumb': breadcrumb,
            'label': label,
            'grades': grades,
            'haystack': haystack,
        })

    pages.sort(key=lambda page: (section_sort_key(page['breadcrumb'][0]), page['title']))
    return pages


def _grade_rows():
    with (DATA_DIR / 'grade-tags.csv').open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def _unanimous_prefixes(rows):
    """First URL token -> section, where the continuum gives that token one area."""
    buckets = defaultdict(set)
    for row in rows:
        href = (row.get('href') or '').strip().strip('/')
        area = (row.get('area') or '').strip()
        if not href or href.startswith('resources/') or not area:
            continue
        buckets[href.split('-')[0]].add(area)
    return {token: next(iter(areas)) for token, areas in buckets.items() if len(areas) == 1}


def _hand_built():
    from apps.resources.data.directed_numbers_page import DIRECTED_NUMBERS
    from apps.resources.data.grade_topic_pages import (
        ALL_OPERATIONS,
        HCF_LCM_PRIME_FACTORISATION,
        INTEGERS_ADD_SUB_1_2_DIGIT,
        KOSHUU_1_DIGIT,
    )
    from apps.resources.topic_pages import FOUR_BASIC_OPERATIONS

    return {
        '/four_basic_operations/': FOUR_BASIC_OPERATIONS,
        '/directed_numbers/': DIRECTED_NUMBERS,
        '/all_operations/': ALL_OPERATIONS,
        '/koshuu-1-digit/': KOSHUU_1_DIGIT,
        '/integers-adding-subtracting-1-2-digit/': INTEGERS_ADD_SUB_1_2_DIGIT,
        '/hcf-lcm-prime-factorisation-mixed/': HCF_LCM_PRIME_FACTORISATION,
    }


def _bridge_meta():
    folder = Path(__file__).resolve().parent / 'data' / 'bridge' / 'pages'
    crumbs = {}
    titles = {}
    if not folder.is_dir():
        return crumbs, titles
    for path in folder.glob('*.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        slug = (data.get('slug') or '').strip('/')
        if not slug:
            continue
        url = f'/{slug}/'
        crumbs[url] = data.get('crumb') or ''
        titles[url] = clean_title(data.get('title') or '')
    return crumbs, titles


def _placeholder_titles():
    from apps.resources.views.onduktar_placeholders import OPERATION_PLACEHOLDER_TITLES
    return OPERATION_PLACEHOLDER_TITLES


def _pack_for(url, slug_pages, path_pages, split_badges):
    slug = url.strip('/')
    if '/' not in slug and slug in slug_pages:
        return slug_pages[slug], split_badges.get(slug)
    if slug.startswith('resources/topic/'):
        key = tuple(slug.split('/')[2:])
        return path_pages.get(key), split_badges.get(key)
    return None, None


def _label_from_spec(spec, override=None):
    if override:
        return override
    if not spec:
        return ''
    if spec.get('grade_badge'):
        return spec['grade_badge']
    grades = sorted({
        item['grade']
        for section in spec.get('sections', [])
        for item in section.get('items', [])
        if isinstance(item.get('grade'), int) and item['grade'] > 0
    })
    if not grades:
        return ''
    if len(grades) == 1:
        return f'{grades[0]}-класс'
    return f'{grades[0]}–{grades[-1]} кл.'


def _label_for(url, hand, pack, override, csv_row, audit_grades, short):
    # The badge the page actually renders wins over the other copies.
    if hand:
        label = _label_from_spec(hand)
        if label:
            return label
    continuum = ((csv_row or {}).get('grade_band') or '').strip()
    if url.startswith('/resources/topic/'):
        if continuum:
            return continuum
        label = _label_from_spec(pack, override)
        if label:
            return label
    else:
        label = _label_from_spec(pack, override)
        if label:
            return label
        if continuum:
            return continuum
    raw = audit_grades.get(url)
    if raw:
        return short(raw)
    return ''


def _title_for(url, fixed, hand, csv_row, placeholders, pack, bridge_titles):
    if fixed:
        return fixed['title']
    if hand and hand.get('title'):
        return clean_title(hand['title'])
    if csv_row and csv_row.get('title'):
        return clean_title(csv_row['title'])
    slug = url.strip('/').split('/')[-1]
    if slug in placeholders:
        return placeholders[slug]
    if url in bridge_titles and bridge_titles[url]:
        return bridge_titles[url]
    if pack and pack.get('title'):
        return clean_title(pack['title'])
    return ''


def _section(url, csv_area, crumb, unanimous):
    if csv_area in SECTION_RANK:
        return csv_area
    parts = [part for part in url.strip('/').split('/') if part]
    if len(parts) >= 3 and parts[0] == 'resources' and parts[1] == 'topic':
        mapped = TOPIC_SECTIONS.get(parts[2])
        if mapped:
            return mapped
    slug = parts[0] if parts else ''
    if slug == 'statistika-ortocho' or slug.startswith('data-'):
        return 'Дата'
    if slug.startswith('probability-'):
        return 'Ыктымалдуулук'
    token = slug.split('-')[0]
    if token in unanimous:
        return unanimous[token]
    if slug.startswith('percentages-to-') or slug.startswith('percentages-with-'):
        return 'Сандар'
    if slug.startswith('percentages-'):
        return 'Пропорция'
    head = _crumb_head(crumb)
    if head == 'Сан':
        return 'Сандар'
    if head:
        return head
    return 'Башка'


def _crumb_head(crumb):
    if not crumb:
        return ''
    return re.split(r'\s*[›·]\s*', crumb, maxsplit=1)[0].strip()


def _breadcrumb(section, subgroup, crumb):
    extra = []
    source = subgroup or crumb
    if source:
        extra = [part.strip() for part in re.split(r'\s*[>›·]\s*', source) if part.strip()]
    crumbs = [section]
    for part in extra:
        if part and part != section and part not in crumbs:
            crumbs.append(part)
    return crumbs


def _is_lesson_url(url):
    if not url.startswith('/') or url.startswith('//') or '<' in url or ' ' in url:
        return False
    bare = url.rstrip('/')
    if bare in ('', '/resources', '/home'):
        return False
    blocked = (
        '/admin', '/account', '/login', '/logout', '/register', '/password',
        '/activate', '/search', '/dashboard', '/analytics', '/track-click',
        '/news', '/about', '/pricing', '/topics', '/tarsia-builder',
        '/resources/download',
    )
    return not bare.startswith(blocked)
