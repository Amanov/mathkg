"""Point the four_basic_operations free file at bytes that exist.

0026 and 0027 set the file column to a path. They did not copy the
file onto the media volume, and they matched rows by the old filename
title, not by id. This pass starts from the stored free-download row
for that page. It sets the title to the v2 filename when that title is
free, and it points `file` at a real file under resources/files/ when
one is already there. A missing file is left alone.
"""

from django.db import migrations


def repair(apps, schema_editor):
    from apps.resources.resource_files import repair_four_basic_free_file
    repair_four_basic_free_file(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0027_point_four_basic_free_file_at_v2'),
    ]

    operations = [
        migrations.RunPython(repair, migrations.RunPython.noop),
    ]
