"""Download rows for the bridge topic pages.

Page copy stays in data/bridge/pages/. The PDFs and PPTX stay in
bundled_files/ and are copied onto MEDIA_ROOT the first time someone
downloads them. This does not add a model, a menu entry, or a column.
"""

from django.db import migrations


def add_resources(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    from apps.resources.bridge_pages import sync_bridge_resources

    sync_bridge_resources(Resource, refresh_media=False)


def remove_resources(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    from apps.resources.bridge_pages import referenced_filenames

    Resource.objects.filter(title__in=referenced_filenames()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0033_hide_template_derived_files'),
    ]

    operations = [
        migrations.RunPython(add_resources, remove_resources),
    ]
