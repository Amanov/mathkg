"""Links between pack pages (2026-11-09).

One pack group is shown on many menu URLs: «Убакыт» on five, the linear
graph pack on forty. The pages are the same, so:

* every copy names the group's main page as its canonical URL
  (``spiral.group_url``), and only main pages go into the sitemap;
* the line above the title is a real path: home › class page › main
  page › this menu item, also written as BreadcrumbList JSON-LD;
* the foot of the page lists the other topics of the same class, so a
  teacher (and a crawler) can move sideways inside a class, not only up
  and down the spiral.
"""

from functools import lru_cache

from apps.resources.data.pack_pages import GROUPS, PACKS
from apps.resources.data.spiral import _first_grade, grade_label, group_url

_BY_KEY = {group['spec']['page_key'][len('pack_'):]: group for group in GROUPS}


def group_key(page_key):
    return page_key[len('pack_'):] if page_key.startswith('pack_') else ''


def main_path(page_key):
    """The canonical path of a pack page, or '' for other pages."""
    key = group_key(page_key)
    if key not in _BY_KEY:
        return ''
    return group_url(key)


def group_grade(page_key):
    """First class number the group is for (the class page it belongs to)."""
    key = group_key(page_key)
    if key not in _BY_KEY:
        return None
    return _first_grade(grade_label(_BY_KEY[key]['spec']))


def page_grade(spec):
    """The class the page shows in its badge (a split badge can move a
    pack page to another class), else the group's first class."""
    badge = spec.get('grade_badge') or ''
    digits = ''
    for ch in badge:
        if ch.isdigit():
            digits += ch
        elif digits:
            break
    if digits:
        return int(digits)
    return group_grade(spec['page_key'])


def group_grades(page_key):
    """Every class the group's label covers ('2–3 кл.' -> {2, 3})."""
    key = group_key(page_key)
    if key not in _BY_KEY:
        return set()
    import re
    numbers = [int(n) for n in re.findall(r'\d+', grade_label(_BY_KEY[key]['spec']))]
    if not numbers:
        return set()
    return set(range(min(numbers), max(numbers) + 1))


def breadcrumb(spec, page_title):
    """[(name, path or '')]: home, class page, main page, this page."""
    page_key = spec['page_key']
    grade = page_grade(spec)
    main = main_path(page_key)
    title = spec['title']
    trail = [('Башкы бет', '/')]
    if grade:
        trail.append((f'{grade}-класс', f'/{grade}-klass/'))
    page_title = ' '.join(str(page_title or '').split())
    if page_title and page_title != title:
        trail.append((title, main))
        trail.append((page_title, ''))
    else:
        trail.append((title, ''))
    return trail


def _group_order():
    """Groups of each class, in the order PACKS lists their first pack."""
    pack_rank = {key: index for index, key in enumerate(PACKS)}
    rows = []
    for key, group in _BY_KEY.items():
        rank = min(pack_rank[p] for p in group['packs'])
        rows.append((rank, key))
    return [key for _, key in sorted(rows)]


def same_grade_topics(page_key, grade=None):
    """Other pack pages of the class: [{'title', 'url'}], one per URL."""
    if grade is None:
        grade = group_grade(page_key)
    if grade is None:
        return []
    current = main_path(page_key)
    seen = {current}
    topics = []
    for key in _group_order():
        if grade not in group_grades('pack_' + key):
            continue
        url = group_url(key)
        if url in seen:
            continue
        seen.add(url)
        topics.append({'title': _BY_KEY[key]['spec']['title'], 'url': url})
    return topics


def pack_url(pack_key):
    """Main page of the group that shows exactly this pack (else any group
    that carries it); '' when none does."""
    fallback = ''
    for key, group in _BY_KEY.items():
        if pack_key not in group['packs']:
            continue
        if group['packs'] == [pack_key]:
            return group_url(key)
        fallback = fallback or group_url(key)
    return fallback


@lru_cache(maxsize=None)
def duplicate_paths():
    """Menu paths that show a pack whose main page is another URL."""
    from apps.resources.data.pack_pages import SLUG_PAGES
    paths = set()
    for slug, spec in SLUG_PAGES.items():
        if main_path(spec['page_key']) != f'/{slug}/':
            paths.add(f'/{slug}/')
    return frozenset(paths)


_THEME_PACKS = None
# Early bank themes written before the file carried a pack key.
_THEME_ALIASES = {
    '2-klass-100-ichinde-koshuu-kemituu': 'k100',
    '3-klass-kobeytuu-boluu-jadybaly': 'jadybal',
}


def theme_url(theme_slug):
    """Topic page of a question-bank theme (``bank_themes()`` ``slug``)."""
    global _THEME_PACKS
    if _THEME_PACKS is None:
        from apps.resources.question_bank import bank_themes
        _THEME_PACKS = {
            theme['slug']: theme.get('pack') or _THEME_ALIASES.get(theme['slug'], '')
            for theme in bank_themes()
        }
    pack = _THEME_PACKS.get(theme_slug or '')
    return pack_url(pack) if pack else ''
