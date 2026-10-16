"""One stable free file per topic page.

Pages call choose_free_resource with the files they actually offer.
The first call stores a random choice; later calls return that same
file. A pinned row is an admin override and is left alone.
"""

import random

from django.db import IntegrityError, transaction

from apps.resources.models import PageFreeDownload


def choose_free_resource(page_key, candidates):
    """Return the page's free Resource, or None when the page has no files."""
    ordered = []
    seen = set()
    for resource in candidates:
        if not resource or not resource.is_active or resource.id in seen:
            continue
        seen.add(resource.id)
        ordered.append(resource)
    if not ordered:
        return None

    with transaction.atomic():
        row = (
            PageFreeDownload.objects.select_for_update()
            .filter(page_key=page_key)
            .first()
        )
        if row is None:
            choice = random.choice(ordered)
            try:
                PageFreeDownload.objects.create(page_key=page_key, resource=choice)
            except IntegrityError:
                row = PageFreeDownload.objects.select_for_update().get(page_key=page_key)
            else:
                return choice
        if row.pinned and row.resource_id:
            return row.resource
        if row.resource_id in seen:
            return row.resource
        choice = random.choice(ordered)
        row.resource = choice
        row.pinned = False
        row.save(update_fields=['resource', 'pinned'])
        return choice


def is_free_resource(resource_id):
    if not resource_id:
        return False
    return PageFreeDownload.objects.filter(resource_id=resource_id).exists()


def operation_page_context(page_key, sections, resources):
    """Copy operation-page sections and mark the one free file.

    The source section lists are module constants, so this returns new
    dicts instead of editing them.
    """
    candidates = []
    seen = set()
    for section in sections:
        for block in section['blocks']:
            for name in block['files']:
                resource = resources.get(name)
                if resource and resource.id not in seen:
                    seen.add(resource.id)
                    candidates.append(resource)
    free = choose_free_resource(page_key, candidates)
    free_id = free.id if free else None
    annotated = []
    for section in sections:
        blocks = []
        for block in section['blocks']:
            resolved = []
            has_locked = False
            for name in block['files']:
                resource = resources.get(name)
                is_free = bool(resource and free_id and resource.id == free_id)
                # A missing file is still not the free one, so the block
                # keeps the register/renew wall it already showed.
                if not is_free:
                    has_locked = True
                resolved.append({'name': name, 'resource': resource, 'free': is_free})
            blocks.append({**block, 'resolved_files': resolved, 'has_locked': has_locked})
        annotated.append({**section, 'blocks': blocks})
    return annotated, free_id
