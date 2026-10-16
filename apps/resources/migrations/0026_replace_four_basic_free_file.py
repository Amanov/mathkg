"""Point the 1-2-3-4 resource at the new order-of-operations file.

The file itself is already in media/resources/files/, the same place as
the other resource files. The Resource row keeps its id, so the stored
PageFreeDownload for this page still points at it.
"""

from django.db import migrations

OLD_TITLE = '4-amal-1234.pptx'
NEW_TITLE = 'amaldar_tartibi_ozun_tuz.pptx'
REL_PATH = f'resources/files/{NEW_TITLE}'


def replace_file(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    # Keep the same row id so PageFreeDownload still points here.
    updated = Resource.objects.filter(title=OLD_TITLE).update(
        title=NEW_TITLE, file=REL_PATH, is_active=True,
    )
    if not updated:
        Resource.objects.filter(title=NEW_TITLE).update(file=REL_PATH, is_active=True)


def restore_old_title(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    Resource.objects.filter(title=NEW_TITLE).update(
        title=OLD_TITLE,
        file=f'resources/files/{OLD_TITLE}',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0025_pagefreedownload'),
    ]

    operations = [
        migrations.RunPython(replace_file, restore_old_title),
    ]
