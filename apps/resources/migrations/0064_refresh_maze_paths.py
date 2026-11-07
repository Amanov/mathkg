"""Replace maze PDFs on the media volume when they still have the old route.

Git already has the new routes. ``_copy_bundled`` only writes a file when
that path is missing, and the Railway volume hides git ``media/``. A maze
already on the volume would keep the shared path and, on the later packs,
«МАРЕ».

The file is replaced only when its sha256 is still ``old`` in
``data/maze_path_manifest.json``. Any other hash is left alone. Running
again is a no-op. There is no ``ALTER TABLE`` and no ORM write.
"""

import os
from pathlib import Path

from django.conf import settings
from django.db import migrations


def forward(apps, schema_editor):
    import json

    from apps.resources.generators.maze_build import sha256_bytes

    root = Path(settings.MEDIA_ROOT)
    bundled = Path(__file__).resolve().parents[1] / 'bundled_files'
    manifest = json.loads(
        (Path(__file__).resolve().parents[1] / 'data' / 'maze_path_manifest.json').read_text(encoding='utf-8')
    )
    totals = {'updated': 0, 'already': 0, 'missing': 0, 'foreign': 0}
    for relative, entry in manifest.items():
        path = root / relative
        source = bundled / Path(relative).name
        if not source.is_file():
            totals['missing'] += 1
            continue
        if not path.is_file():
            totals['missing'] += 1
            continue
        current = sha256_bytes(path.read_bytes())
        if current == entry['new']:
            totals['already'] += 1
            continue
        if current != entry['old']:
            totals['foreign'] += 1
            continue
        payload = source.read_bytes()
        if sha256_bytes(payload) != entry['new']:
            totals['foreign'] += 1
            continue
        temporary = path.with_name(path.name + '.maze-tmp')
        try:
            temporary.write_bytes(payload)
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()
        totals['updated'] += 1
    print('maze paths: ' + ' '.join(f'{name}={count}' for name, count in totals.items()))


def backward(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0063_wave13_packs'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
