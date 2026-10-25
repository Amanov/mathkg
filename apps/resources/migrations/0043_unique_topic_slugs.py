"""Merge duplicate topic and subtopic slugs.

The menu rebuild inserted a fresh sub-subtopic for every nested «Аралаш»
leaf. Those leaves share a single subtopic, so several rows used the
slug ``mixed``. ``/resources/topic/.../mixed/`` then called ``get()`` and
Django turned MultipleObjectsReturned into HTTP 500.

This keeps the oldest row in each duplicate group, points resources and
menu items at it, and deletes only the extra taxonomy rows. Resource
files are not deleted. The same pass covers every duplicate, not only
the three URLs that 500 today.

The unique constraints are not added here. Postgres defers the
foreign-key checks from the repoint and delete, and refuses
``ALTER TABLE`` while those trigger events are still pending. Doing both
in this migration rolled the whole transaction back, so 0043 was never
recorded and every boot ran it again. ``0045`` and ``0046`` add the
constraints after this migration has committed.

Reversing does not split the merged rows. That would need a record of
which copy each resource and menu item came from, and those copies were
never separate pages. ``0046`` and ``0045`` drop the constraints.
"""

from django.db import migrations


def _merge(rows, repoint):
    keep = rows[0]
    for dup in rows[1:]:
        for model, field in repoint:
            model.objects.filter(**{field: dup.pk}).update(**{field: keep.pk})
        dup.delete()


def merge_duplicate_slugs(apps, schema_editor):
    Subtopic = apps.get_model('personal', 'Subtopic')
    SubSubtopic = apps.get_model('personal', 'SubSubtopic')
    Resource = apps.get_model('personal', 'Resource')
    MenuItem = apps.get_model('personal', 'MenuItem')

    subtopics = {}
    for row in Subtopic.objects.all().order_by('pk'):
        subtopics.setdefault((row.topic_id, row.slug), []).append(row)
    for rows in subtopics.values():
        if len(rows) < 2:
            continue
        _merge(rows, (
            (SubSubtopic, 'subtopic_id'),
            (Resource, 'subtopic_id'),
            (MenuItem, 'subtopic_id'),
        ))

    # Repointing a subtopic can land two sub-subtopics on the same slug.
    subsubtopics = {}
    for row in SubSubtopic.objects.all().order_by('pk'):
        subsubtopics.setdefault((row.subtopic_id, row.slug), []).append(row)
    for rows in subsubtopics.values():
        if len(rows) < 2:
            continue
        _merge(rows, (
            (Resource, 'subsubtopic_id'),
            (MenuItem, 'subsubtopic_id'),
        ))


def unmerge_duplicate_slugs(apps, schema_editor):
    # See the module docstring. The merged rows stay merged.
    return


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0042_wave5_packs'),
    ]

    operations = [
        migrations.RunPython(merge_duplicate_slugs, unmerge_duplicate_slugs),
    ]
