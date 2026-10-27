"""Refresh Kyrgyz wording already stored on the media volume.

The git and bundled copies already contain the corrected sentences.
``_copy_bundled`` only writes a file when that path is missing, and the
Railway volume hides git ``media/``. A deck already on the volume would
keep the old wording.

This migration rewrites a volume file only when its sha256 is still the
old bytes in ``data/deck_kyrgyz_manifest.json``. The rewrite is the same
in-place text edit. It is written only when the result hash is the
recorded new hash. A missing file stays missing. Any other hash (an
admin upload, or a deck this pass did not change) stays as it is.
Running again is a no-op.

There is no ``ALTER TABLE`` and no ORM write. Migration 0043 failed on
Postgres because a data change and ``ALTER TABLE`` shared one
transaction. This migration is a file rewrite in its own step.

``0049`` runs first and brings a volume file up to the previous text
fix. The old hash here is that result, so the two steps do not skip
each other.

Reversing does not restore the old sentences and does not delete files.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations


def forward(apps, schema_editor):
    from apps.resources.kyrgyz_text import refresh_kyrgyz_media

    refresh_kyrgyz_media(Path(settings.MEDIA_ROOT))


def backward(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0049_refresh_deck_text'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
