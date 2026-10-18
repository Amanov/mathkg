"""Open a resource file, including when the stored path is missing.

Migrations 0026 and 0027 wrote a path into the database. On Railway the
volume at /app/media hides the copy that arrived in git, so that path
can be empty. An admin upload can also land beside it under Django's
collision name (``name_AbCdEf1.pptx``) while the field still names the
missing path. This module only looks inside ``resources/files/`` and
never invents a path that is not already on disk.
"""

import logging
import re
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

FILES_PREFIX = 'resources/files/'
CANONICAL_FREE_FILE = 'amaldar_tartibi_ozun_tuz_v2.pptx'
KNOWN_TITLES = (
    CANONICAL_FREE_FILE,
    'amaldar_tartibi_ozun_tuz.pptx',
    '4-amal-1234.pptx',
)
BUNDLED_DIR = Path(__file__).resolve().parent / 'bundled_files'
PAGE_KEY = 'four_basic_operations'
# Django's FileSystemStorage.get_alternative_name appends _ plus
# get_random_string(7) before the extension when the name is taken.
# The same shape also matches real activity names in this library
# (Jydymai, KondumA, BoluuXO, Orunduk, ...). Those names are reused
# across many files; a collision suffix is not.
SUFFIX = re.compile(r'^[A-Za-z0-9]{7}$')


def open_resource_file(resource):
    """Return a binary handle for this resource's download.

    Tries the stored name first. If that file is missing or unreadable,
    looks for the title's filename, then for exactly one collision-suffix
    sibling. When a fallback file is found, the stored name is updated
    so the next request and the admin "Currently" link use it.
    """
    stored = getattr(resource.file, 'name', '') or ''
    if stored:
        try:
            return resource.file.open('rb')
        except (FileNotFoundError, OSError, ValueError):
            logger.error(
                'Resource file missing on disk: resource_id=%s, file=%s',
                resource.pk, stored,
            )

    path = locate_resource_file(resource)
    if path is None:
        raise FileNotFoundError(stored or getattr(resource, 'title', ''))

    rel = FILES_PREFIX + path.name
    if stored != rel:
        resource.file.name = rel
        resource.save(update_fields=['file'])
        logger.error(
            'Resource %s file field pointed at %s; serving and storing %s',
            resource.pk, stored, rel,
        )
    return path.open('rb')


def locate_resource_file(resource):
    """A file under resources/files/ that matches this row, or None."""
    root = Path(settings.MEDIA_ROOT) / 'resources' / 'files'
    names = []
    for raw in (getattr(resource.file, 'name', '') or '', getattr(resource, 'title', '') or ''):
        base = _basename(raw)
        if base and base not in names:
            names.append(base)

    if root.is_dir():
        for name in names:
            path = root / name
            if path.is_file():
                return path

        reused = _reused_name_tokens(root)
        seen = set()
        for name in names:
            stem = Path(name).stem
            ext = Path(name).suffix
            if not stem or not ext or (stem, ext) in seen:
                continue
            seen.add((stem, ext))
            matches = _suffixed_files(root, stem, ext, reused)
            if len(matches) == 1:
                return matches[0]

    for name in names:
        bundled = BUNDLED_DIR / name
        if bundled.is_file():
            return _copy_bundled(bundled)
    return None


def repair_four_basic_free_file(apps):
    """Point four_basic_operations at the v2 lesson and keep that choice.

    Finds the row by the v2 file name or the older filenames, sets its
    title to the name the page looks up, copies the bundled deck onto
    MEDIA_ROOT when that path is empty, and pins the free-download row.
    Does not rename whatever resource the page currently gives away.
    """
    PageFreeDownload = apps.get_model('personal', 'PageFreeDownload')
    Resource = apps.get_model('personal', 'Resource')
    resource = _v2_resource(Resource)
    if resource is None:
        return []
    changed = repair_stored_file(resource, CANONICAL_FREE_FILE)
    row = PageFreeDownload.objects.filter(page_key=PAGE_KEY).first()
    if row is None:
        PageFreeDownload.objects.create(
            page_key=PAGE_KEY, resource_id=resource.pk, pinned=True,
        )
        changed.append('free')
    elif row.resource_id != resource.pk or not row.pinned:
        row.resource_id = resource.pk
        row.pinned = True
        row.save(update_fields=['resource', 'pinned'])
        changed.append('free')
    return changed


def _v2_resource(Resource):
    from django.db.models import Q

    rows = list(
        Resource.objects.filter(
            Q(title__in=KNOWN_TITLES) | Q(file__endswith=CANONICAL_FREE_FILE),
        ).order_by('id')
    )
    for resource in rows:
        if _basename(getattr(resource.file, 'name', '')) == CANONICAL_FREE_FILE:
            return resource
    for resource in rows:
        if resource.title == CANONICAL_FREE_FILE:
            return resource
    return rows[0] if rows else None


def repair_stored_file(resource, canonical_title):
    changed = []
    current_ok = _stored_file_opens(resource)
    if canonical_title and resource.title != canonical_title:
        taken = resource.__class__.objects.filter(
            title=canonical_title,
        ).exclude(pk=resource.pk).exists()
        if not taken:
            resource.title = canonical_title
            changed.append('title')
    if not current_ok:
        path = locate_resource_file(resource)
        if path is not None:
            rel = FILES_PREFIX + path.name
            if resource.file.name != rel:
                resource.file.name = rel
                changed.append('file')
    if changed:
        resource.save(update_fields=changed)
    return changed


def _stored_file_opens(resource):
    name = getattr(resource.file, 'name', '') or ''
    if not name:
        return False
    try:
        handle = resource.file.open('rb')
    except (FileNotFoundError, OSError, ValueError):
        return False
    handle.close()
    return True


def _copy_bundled(bundled):
    """Place the shipped deck on MEDIA_ROOT when that path is empty."""
    root = Path(settings.MEDIA_ROOT) / 'resources' / 'files'
    try:
        root.mkdir(parents=True, exist_ok=True)
        dest = root / bundled.name
        if not dest.exists():
            dest.write_bytes(bundled.read_bytes())
        if dest.is_file():
            return dest
    except OSError:
        logger.error('Could not copy bundled resource file onto MEDIA_ROOT: %s', bundled.name)
    return bundled


def _basename(name):
    name = str(name).replace('\\', '/').rsplit('/', 1)[-1].strip()
    if not name or name in ('.', '..') or '/' in name or '\\' in name:
        return ''
    return name


def _reused_name_tokens(root):
    """7-character filename pieces that belong to more than one file.

    Django's collision suffix is a one-off random string. Activity names
    such as Jydymai or KondumA are the same length and alphabet, but they
    are shared by many files. Treating a shared name as a collision would
    serve that other file and, in open_resource_file, store the wrong path.
    """
    counts = {}
    for path in root.iterdir():
        if not path.is_file():
            continue
        seen_in_file = set()
        for part in path.stem.split('_'):
            if SUFFIX.fullmatch(part):
                seen_in_file.add(part.lower())
        for key in seen_in_file:
            counts[key] = counts.get(key, 0) + 1
    return {key for key, count in counts.items() if count > 1}


def _suffixed_files(root, stem, ext, reused):
    prefix = stem + '_'
    found = []
    for path in root.iterdir():
        if not path.is_file() or path.suffix != ext or not path.name.startswith(prefix):
            continue
        middle = path.name[len(prefix):-len(ext)]
        if SUFFIX.fullmatch(middle) and middle.lower() not in reused:
            found.append(path)
    return found
