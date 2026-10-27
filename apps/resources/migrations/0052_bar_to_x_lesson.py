"""Add the «Тилкеден x ке» explanation deck.

Creates the Resource row and, when the volume path is empty, copies the
bundled file there. An existing file is left as it is, so an admin upload
is not replaced. There is no ALTER TABLE.

Reversing removes the row and does not delete the file.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations

NAME = 'bar-to-x-sabak.pptx'


def forward(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    if Resource.objects.filter(title=NAME).exists():
        Resource.objects.filter(title=NAME).update(is_active=True)
    else:
        Resource.objects.create(
            title=NAME,
            file=f'resources/files/{NAME}',
            category='presentation',
            is_active=True,
        )
    bundled = Path(__file__).resolve().parents[1] / 'bundled_files' / NAME
    if not bundled.is_file():
        return
    root = Path(settings.MEDIA_ROOT) / 'resources' / 'files'
    root.mkdir(parents=True, exist_ok=True)
    dest = root / NAME
    if not dest.exists():
        dest.write_bytes(bundled.read_bytes())


def backward(apps, schema_editor):
    apps.get_model('personal', 'Resource').objects.filter(title=NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0050_refresh_kyrgyz_text'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
