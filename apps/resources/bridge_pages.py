"""Bridge topic pages: specs, draft import, and bundled download files.

Page copy lives in ``data/bridge/pages/<slug>.json``. Downloadable PDFs and
PPTX live in ``bundled_files/`` under their filename, which is also the
Resource title, so the existing download lookup finds them. Thumbnails
live in ``static/img/bridge/``.

Replacing a worksheet or slide deck without changing the page is a file
swap: put the new bytes at the same filename and run
``sync_bridge_resources`` (it refreshes the media copy). A revised draft
folder — one directory per slug, with ``page-draft/index.html`` — is
imported with ``import_bridge_drafts``.
"""

import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PAGES_DIR = APP_DIR / 'data' / 'bridge' / 'pages'
BUNDLED_DIR = APP_DIR / 'bundled_files'
THUMB_DIR = APP_DIR.parent.parent / 'static' / 'img' / 'bridge'
CPA_LABELS = ('Конкреттүү', 'Сүрөт', 'Абстракттуу')
BLOOM_LEVEL_NAMES = (
    'Эстеп калуу',
    'Түшүнүү',
    'Колдонуу',
    'Талдоо',
    'Баалоо',
    'Жаратуу',
)

_SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
_SPACE = re.compile(r'\s+')


def url_name_for(slug):
    return slug.replace('-', '_')


def iter_page_paths():
    if not PAGES_DIR.is_dir():
        return []
    return sorted(PAGES_DIR.glob('*.json'))


def load_page(slug):
    path = PAGES_DIR / f'{slug}.json'
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def iter_pages():
    pages = []
    for path in iter_page_paths():
        data = json.loads(path.read_text(encoding='utf-8'))
        data['slug'] = data.get('slug') or path.stem
        data['url_name'] = data.get('url_name') or url_name_for(data['slug'])
        pages.append(data)
    return pages


def referenced_filenames(pages=None):
    names = []
    seen = set()
    for page in pages if pages is not None else iter_pages():
        for section in page.get('sections') or []:
            for item in section.get('items') or []:
                for _label, name in item.get('files') or []:
                    if name and name not in seen:
                        seen.add(name)
                        names.append(name)
    return names


def page_spec(data):
    """Turn one page JSON document into a ``build_topic_page`` spec.

    Filenames are the Resource titles. Nothing here embeds file bytes, so a
    later content drop can replace the JSON and the files independently.
    """
    images = {}
    sections = []
    for section in data.get('sections') or []:
        items = []
        for item in section.get('items') or []:
            files = [tuple(pair) for pair in item.get('files') or []]
            stem = Path(files[0][1]).stem if files else item.get('title', 'item')
            image = item.get('image') or ''
            if image:
                images[stem] = image
            items.append({
                'title': item.get('title') or '',
                'note': item.get('note') or '',
                'level': item.get('level') or 'Колдонуу',
                'files': files,
                'svg': stem,
                'cpa': list(item.get('cpa') or []),
            })
        sections.append({
            'stage': section.get('stage') or '',
            'title': section.get('title') or '',
            'title_en': section.get('title_en') or '',
            'when': section.get('when') or '',
            'bloom': list(section.get('bloom') or []),
            'summary': section.get('summary') or '',
            'items': items,
        })
    guide = data.get('bloom_guide') or []
    return {
        'title': data.get('title') or data.get('slug') or '',
        'crumb': data.get('crumb') or '',
        'svg_dir': 'svg/topic/to-fractions',
        'file_prefix': '',
        'page_key': data.get('page_key') or data.get('url_name') or url_name_for(data.get('slug', 'bridge')),
        'images': images,
        'downloads_gated': True,
        'sections': sections,
        'singapore': list(data.get('singapore') or []),
        'bloom_guide': [tuple(pair) for pair in guide],
    }


def category_for(filename):
    if filename.lower().endswith('.pptx'):
        return 'presentation'
    return 'worksheet'


def sync_bridge_resources(Resource, refresh_media=False):
    """Create a Resource row per referenced file. Optionally overwrite media copies.

    ``Resource`` is passed in so a migration can use the historical model.
    Returns ``(created, refreshed)`` counts.
    """
    created = 0
    refreshed = 0
    for name in referenced_filenames():
        bundled = BUNDLED_DIR / name
        row = Resource.objects.filter(title=name).first()
        if row is None:
            Resource.objects.create(
                title=name,
                file=f'resources/files/{name}',
                category=category_for(name),
                is_active=True,
            )
            created += 1
        elif not row.is_active:
            row.is_active = True
            row.save(update_fields=['is_active'])
        if refresh_media and bundled.is_file():
            if _refresh_media_copy(bundled):
                refreshed += 1
    return created, refreshed


def _refresh_media_copy(bundled):
    from django.conf import settings

    root = Path(settings.MEDIA_ROOT) / 'resources' / 'files'
    root.mkdir(parents=True, exist_ok=True)
    dest = root / bundled.name
    payload = bundled.read_bytes()
    if dest.is_file() and dest.read_bytes() == payload:
        return False
    dest.write_bytes(payload)
    return True


class _NodeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': 'root', 'classes': [], 'attrs': {}, 'text': '', 'children': []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        node = {
            'tag': tag,
            'classes': attr_map.get('class', '').split(),
            'attrs': attr_map,
            'text': '',
            'children': [],
        }
        self.stack[-1]['children'].append(node)
        if tag not in ('img', 'br', 'meta', 'link', 'input', 'hr'):
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index]['tag'] == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        if data:
            self.stack[-1]['text'] += data


def _walk(node):
    yield node
    for child in node['children']:
        yield from _walk(child)


def _has(node, class_name):
    return class_name in node['classes']


def _direct(node):
    return _SPACE.sub(' ', node.get('text') or '').strip()


def _bloom_level(text):
    for name in BLOOM_LEVEL_NAMES:
        if name in text:
            return name
    return ''


def _find(node, class_name, tag=None):
    for child in _walk(node):
        if child is node:
            continue
        if _has(child, class_name) and (tag is None or child['tag'] == tag):
            return child
    return None


def _findall(node, class_name, tag=None):
    found = []
    for child in _walk(node):
        if child is node:
            continue
        if _has(child, class_name) and (tag is None or child['tag'] == tag):
            found.append(child)
    return found


def parse_draft_html(html):
    """Pull the topic-page fields out of a static draft."""
    start = html.find('<main')
    end = html.find('</main>')
    if start < 0 or end < 0:
        raise ValueError('draft has no <main> topic page')
    parser = _NodeParser()
    parser.feed(html[start:end + len('</main>')])
    main = _find(parser.root, 'topic-page') or parser.root

    title_node = _find(main, 'topic-page__title', 'h1')
    crumb_node = _find(main, 'topic-crumbs')
    title = _direct(title_node) if title_node else ''
    crumb = _direct(crumb_node) if crumb_node else ''

    singapore = []
    grid = _find(main, 'sg-grid')
    if grid is not None:
        pending = None
        for child in grid['children']:
            if child['tag'] == 'dt':
                pending = _direct(child)
            elif child['tag'] == 'dd' and pending:
                singapore.append({'label': pending, 'text': _direct(child)})
                pending = None

    bloom_guide = []
    for guide in _findall(main, 'guide-list'):
        pending = None
        pairs = []
        for child in guide['children']:
            if child['tag'] == 'dt':
                pending = _direct(child)
            elif child['tag'] == 'dd' and pending:
                pairs.append([pending, _direct(child)])
                pending = None
        if pairs:
            bloom_guide = pairs

    sections = []
    for section_node in _findall(main, 'topic-section', 'section'):
        head = _find(section_node, 'topic-section__head') or section_node
        stage = _find(head, 'stage-tag')
        heading = _find(head, 'topic-section__title', 'h2')
        title_en = _find(head, 'topic-section__en') if heading else None
        summary = _find(head, 'topic-section__summary')
        when = _find(head, 'topic-section__when')
        bloom = [_direct(chip) for chip in _findall(head, 'bloom-chip') if _direct(chip)]
        items = []
        for article in _findall(section_node, 'topic-row', 'article'):
            image = _find(article, 'mk-zoom', 'img') or next(
                (node for node in _walk(article) if node['tag'] == 'img'), None,
            )
            image_name = ''
            if image is not None:
                src = image['attrs'].get('src') or ''
                image_name = src.replace('\\', '/').rsplit('/', 1)[-1]
            title_el = _find(article, 'topic-row__title', 'h3')
            note_el = _find(article, 'topic-row__note')
            level = ''
            for node in _walk(article):
                if _has(node, 'bloom-tag'):
                    level = _bloom_level(_direct(node))
                    if level:
                        break
            cpa = []
            for chip in _findall(article, 'cpa-chip'):
                if 'on' in chip['classes']:
                    label = _direct(chip)
                    if label:
                        cpa.append(label)
            files = []
            for pill in _findall(article, 'file-pill', 'a'):
                href = pill['attrs'].get('href') or ''
                filename = href.replace('\\', '/').rsplit('/', 1)[-1]
                label = _direct(pill)
                if filename and label and not filename.endswith('.html'):
                    files.append([label, filename])
            items.append({
                'title': _direct(title_el) if title_el else '',
                'note': _direct(note_el) if note_el else '',
                'level': level,
                'cpa': cpa,
                'image': f'img/bridge/{image_name}' if image_name else '',
                'image_name': image_name,
                'files': files,
            })
        stage_text = _direct(stage) if stage else ''
        section_title = _direct(heading) if heading else ''
        if section_title and stage_text.endswith(section_title):
            stage_text = stage_text[: -len(section_title)].strip()
        sections.append({
            'stage': stage_text,
            'title': section_title,
            'title_en': _direct(title_en) if title_en else '',
            'summary': _direct(summary) if summary else '',
            'when': _direct(when) if when else '',
            'bloom': bloom,
            'items': items,
        })

    return {
        'title': title,
        'crumb': crumb,
        'singapore': singapore,
        'bloom_guide': bloom_guide,
        'sections': sections,
    }


def _copy_downloads(slug_dir):
    copied = []
    for path in slug_dir.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in ('.pdf', '.pptx'):
            continue
        if 'page-draft' in path.parts or 'src' in path.parts:
            continue
        dest = BUNDLED_DIR / path.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        copied.append(path.name)
    return copied


def _copy_thumbnail(slug_dir, image_name):
    if not image_name:
        return False
    candidates = [
        slug_dir / 'page-draft' / 'assets' / image_name,
        slug_dir / 'thumbnails' / image_name,
    ]
    source = next((path for path in candidates if path.is_file()), None)
    if source is None:
        return False
    dest = THUMB_DIR / image_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    return True


def import_draft_tree(root):
    """Read one folder per slug and rewrite specs plus bundled files.

    ``root`` is the extracted archive (folders named by URL slug). Returns a
    list of ``{slug, files, thumbs, items}`` summaries.
    """
    root = Path(root)
    summaries = []
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    for slug_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        slug = slug_dir.name
        if not _SLUG_RE.match(slug):
            continue
        draft = slug_dir / 'page-draft' / 'index.html'
        if not draft.is_file():
            continue
        parsed = parse_draft_html(draft.read_text(encoding='utf-8'))
        copied = _copy_downloads(slug_dir)
        thumbs = 0
        for section in parsed['sections']:
            for item in section['items']:
                if _copy_thumbnail(slug_dir, item.pop('image_name', '')):
                    thumbs += 1
                else:
                    item.pop('image_name', None)
        document = {
            'slug': slug,
            'url_name': url_name_for(slug),
            'page_key': url_name_for(slug),
            'title': parsed['title'],
            'crumb': parsed['crumb'],
            'singapore': parsed['singapore'],
            'bloom_guide': parsed['bloom_guide'],
            'sections': parsed['sections'],
        }
        (PAGES_DIR / f'{slug}.json').write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        summaries.append({
            'slug': slug,
            'title': parsed['title'],
            'files': len(copied),
            'thumbs': thumbs,
            'items': sum(len(section['items']) for section in parsed['sections']),
        })
    return summaries
