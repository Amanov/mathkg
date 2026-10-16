"""Point the order-of-operations resource at the Kyrgyz v2 file.

The new bytes live at media/resources/files/amaldar_tartibi_ozun_tuz_v2.pptx.
The Resource row keeps its id, so the stored PageFreeDownload for this
page still points at it.
"""

from django.db import migrations

OLD_TITLE = 'amaldar_tartibi_ozun_tuz.pptx'
NEW_TITLE = 'amaldar_tartibi_ozun_tuz_v2.pptx'
REL_PATH = f'resources/files/{NEW_TITLE}'


def point_at_v2(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    updated = Resource.objects.filter(title=OLD_TITLE).update(
        title=NEW_TITLE, file=REL_PATH, is_active=True,
    )
    if not updated:
        Resource.objects.filter(title=NEW_TITLE).update(file=REL_PATH, is_active=True)


def restore_previous_file(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    Resource.objects.filter(title=NEW_TITLE).update(
        title=OLD_TITLE,
        file=f'resources/files/{OLD_TITLE}',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0026_replace_four_basic_free_file'),
    ]

    operations = [
        migrations.RunPython(point_at_v2, restore_previous_file),
    ]
