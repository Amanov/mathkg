"""Write «МААРА» onto pack PDFs already stored on the media volume.

The git copies already contain the corrected word. ``_copy_bundled`` only
writes a file when that path is missing, and the Railway volume hides
git ``media/``. A PDF already on the volume would keep «МАРА».

This migration rewrites a volume file only when its sha256 is still the
old bytes in ``data/finish_word_manifest.json``. Those old bytes are the
result of ``0051_refresh_pack_pdf``. The rewrite is written only when the
result hash is the recorded new hash. A missing file stays missing. Any
other hash stays as it is. Running again is a no-op.

There is no ``ALTER TABLE`` and no ORM write.

``0052_bar_to_x_lesson`` is on main. This migration follows it, so the
graph has one leaf.

Reversing does not restore the old text and does not delete files.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations


def forward(apps, schema_editor):
    from apps.resources.finish_word import refresh_finish_media

    refresh_finish_media(Path(settings.MEDIA_ROOT))


def backward(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0052_bar_to_x_lesson'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
