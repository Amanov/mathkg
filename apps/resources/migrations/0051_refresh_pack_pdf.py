"""Refresh pack-PDF wording already stored on the media volume.

The git and bundled copies already contain the corrected text. ``_copy_bundled``
only writes a file when that path is missing, and the Railway volume hides
git ``media/``. A PDF already on the volume would keep the old wording.

This migration rewrites a volume file only when its sha256 is still the
old bytes in ``data/pack_pdf_manifest.json``. The rewrite keeps the drawing
and replaces text runs. It is written only when the result hash is the
recorded new hash. A missing file stays missing. Any other hash stays as
it is. Running again is a no-op.

There is no ``ALTER TABLE`` and no ORM write.

Reversing does not restore the old text and does not delete files.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations


def forward(apps, schema_editor):
    from apps.resources.pack_pdf import refresh_pdf_media

    refresh_pdf_media(Path(settings.MEDIA_ROOT))


def backward(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0050_refresh_kyrgyz_text'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
