"""Refresh lesson-deck wording already stored on the media volume.

Three text fixes are in the git copies and in ``bundled_files``:

* «Турдуу пикирлер учун» → «Түрдүү пикирлер үчүн»
* grade chips and Cambridge labels removed from pack slides
* leftover English buttons and mottoes translated

``_copy_bundled`` only copies a deck when that path is missing, and the
Railway volume hides the git ``media/`` tree. A file already on the
volume would keep the old wording. This migration rewrites a volume file
only when its sha256 is still the old bytes recorded in
``data/deck_text_manifest.json``. The rewrite is the same in-place text
edit, and it is written only if the result hash is the recorded new hash.

Missing files are left missing. A file an admin has replaced (any other
hash) is left alone. Running again is a no-op: updated files no longer
match the old hash.

There is no ``ALTER TABLE`` and no ORM write. Postgres rejected 0043
because a data change and ``ALTER TABLE`` shared one transaction; this
migration is data on disk only, in its own migration, so that cannot recur.

Reversing does not restore the old sentences and does not delete files.
Putting the previous bytes back would overwrite a deck edited after this
ran. The forward step is safe to leave in place.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations


def forward(apps, schema_editor):
    from apps.resources.deck_text import refresh_media

    refresh_media(Path(settings.MEDIA_ROOT))


def backward(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0048_wave8_packs'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
