"""One slug per topic, and one slug per subtopic.

The menu rebuild inserted a fresh sub-subtopic for every nested «Аралаш»
leaf. Those leaves share a single subtopic, so several rows used the
slug ``mixed``. ``/resources/topic/.../mixed/`` then called ``get()`` and
Django turned MultipleObjectsReturned into HTTP 500.

This keeps the oldest row in each duplicate group, points resources and
menu items at it, and deletes only the extra taxonomy rows. Resource
files are not deleted. The same pass covers every duplicate, not only
the three URLs that 500 today.

Reversing drops the unique constraints and leaves the merged rows in
place. Splitting them again would need a record of which copy each
resource and menu item came from, and those copies were never separate
pages.
"""

from django.db import migrations, models


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
        migrations.AddConstraint(
            model_name='subtopic',
            constraint=models.UniqueConstraint(
                fields=['topic', 'slug'],
                name='personal_subtopic_topic_slug_uniq',
            ),
        ),
        migrations.AddConstraint(
            model_name='subsubtopic',
            constraint=models.UniqueConstraint(
                fields=['subtopic', 'slug'],
                name='personal_subsubtopic_subtopic_slug_uniq',
            ),
        ),
    ]
