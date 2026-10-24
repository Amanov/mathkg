"""Grade band and previous/next topic for the bridge pages, read from CSV.

The files are the continuum tables. Only the bridge topic view calls
``continuum_for_href``, so other pages do not show this nav or badge.
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / 'data' / 'continuum'

_CACHE = None


def _rows(name):
    path = DATA_DIR / name
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def clean_title(title):
    return (title or '').replace(' [ЖАҢЫ]', '').strip()


def path_label(name):
    """Kyrgyz path name, without the English gloss in parentheses."""
    name = (name or '').strip()
    if ' (' in name:
        name = name.split(' (', 1)[0]
    return name.strip()


def _index():
    global _CACHE
    if _CACHE is None:
        paths = {row['href']: row for row in _rows('learning-paths.csv')}
        grades = {row['href']: row for row in _rows('grade-tags.csv')}
        _CACHE = (paths, grades)
    return _CACHE


def continuum_for_href(href):
    """Grade badge and neighbours for one public path, or None."""
    if not href:
        return None
    if not href.startswith('/'):
        href = '/' + href
    if not href.endswith('/'):
        href += '/'
    paths, grades = _index()
    path = paths.get(href)
    grade = grades.get(href)
    if path is None and grade is None:
        return None

    def neighbor(other_href):
        other_href = (other_href or '').strip()
        if not other_href:
            return None
        other = paths.get(other_href) or grades.get(other_href) or {}
        return {'href': other_href, 'title': clean_title(other.get('title') or other_href)}

    path = path or {}
    grade = grade or {}
    return {
        'grade_band': (grade.get('grade_band') or '').strip(),
        'path_label': path_label(path.get('path_name') or ''),
        'prev': neighbor(path.get('prev_href')),
        'next': neighbor(path.get('next_href')),
    }
