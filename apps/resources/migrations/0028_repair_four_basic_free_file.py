"""Point four_basic_operations back at the v2 lesson.

The page looks the file up by the exact title amaldar_tartibi_ozun_tuz_v2.pptx.
After 0026/0027 the stored free row could fall out of that lookup, and the
next visit then picked a different file. This pins the v2 row again and
copies the bundled deck onto MEDIA_ROOT when that path is empty.
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
