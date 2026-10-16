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
# Django's FileSystemStorage.get_alternative_name appends _ plus
# get_random_string(7) before the extension when the name is taken.
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
    if not root.is_dir():
        return None

    names = []
    for raw in (getattr(resource.file, 'name', '') or '', getattr(resource, 'title', '') or ''):
        base = _basename(raw)
        if base and base not in names:
            names.append(base)

    for name in names:
        path = root / name
        if path.is_file():
            return path

    seen = set()
    for name in names:
        stem = Path(name).stem
        ext = Path(name).suffix
        if not stem or not ext or (stem, ext) in seen:
            continue
        seen.add((stem, ext))
        matches = _suffixed_files(root, stem, ext)
        if len(matches) == 1:
            return matches[0]
    return None


def repair_four_basic_free_file(apps):
    """Point the stored free row at a file that exists. Never create a row.

    Title becomes the v2 filename only when no other row already has it.
    The file field changes only when that new path is a real file.
    """
    PageFreeDownload = apps.get_model('personal', 'PageFreeDownload')
    Resource = apps.get_model('personal', 'Resource')
    row = PageFreeDownload.objects.filter(page_key='four_basic_operations').first()
    if row is None or not row.resource_id:
        return []
    resource = Resource.objects.filter(pk=row.resource_id).first()
    if resource is None:
        return []
    return repair_stored_file(resource, CANONICAL_FREE_FILE)


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


def _basename(name):
    name = str(name).replace('\\', '/').rsplit('/', 1)[-1].strip()
    if not name or name in ('.', '..') or '/' in name or '\\' in name:
        return ''
    return name


def _suffixed_files(root, stem, ext):
    prefix = stem + '_'
    found = []
    for path in root.iterdir():
        if not path.is_file() or path.suffix != ext or not path.name.startswith(prefix):
            continue
        middle = path.name[len(prefix):-len(ext)]
        if SUFFIX.fullmatch(middle):
            found.append(path)
    return found
