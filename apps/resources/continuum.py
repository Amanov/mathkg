"""Learning-path order and grade bands, loaded from the continuum CSVs.

``learning-paths.csv`` gives every topic href a previous and next page.
``grade-tags.csv`` gives the 12-year grade band («5 кл.»). ``load_topic_continuum``
writes both into ``TopicContinuum``. The topic-page nav reads that table.
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / 'data' / 'continuum'


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


def load_topic_continuum(model):
    """Upsert one row per href. ``model`` is ``TopicContinuum`` or a migration stand-in."""
    paths = {row['href']: row for row in _rows('learning-paths.csv')}
    grades = {row['href']: row for row in _rows('grade-tags.csv')}
    hrefs = sorted(set(paths) | set(grades))
    if not hrefs:
        raise RuntimeError('continuum CSVs did not contain any topics')
    for href in hrefs:
        path = paths.get(href, {})
        grade = grades.get(href, {})
        title = clean_title(path.get('title') or grade.get('title') or href)
        model.objects.update_or_create(
            href=href,
            defaults={
                'title': title[:300],
                'grade_band': (grade.get('grade_band') or '')[:40],
                'school_level': (grade.get('school_level') or '')[:40],
                'prev_href': (path.get('prev_href') or '')[:255],
                'next_href': (path.get('next_href') or '')[:255],
                'path_name': (path.get('path_name') or '')[:300],
            },
        )
    return len(hrefs)


def continuum_for_path(path):
    """Nav context for this request path, or None when the path is not a topic."""
    from django.db.utils import OperationalError, ProgrammingError

    from apps.resources.models import TopicContinuum

    if not path:
        return None
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path += '/'
    try:
        row = TopicContinuum.objects.filter(href=path).first()
    except (OperationalError, ProgrammingError):
        return None
    if row is None:
        return None

    def neighbor(href):
        if not href:
            return None
        other = TopicContinuum.objects.filter(href=href).only('title').first()
        return {'href': href, 'title': other.title if other else href}

    return {
        'grade_band': row.grade_band,
        'path_label': path_label(row.path_name),
        'prev': neighbor(row.prev_href),
        'next': neighbor(row.next_href),
    }
