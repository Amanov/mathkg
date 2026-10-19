"""Resource rows for the two replaced 5-класс «Төрт амал» files.

The games deck moves to v6 (the tarsia pieces now match on every shared
edge) and «Ката карталары» gives way to a real «Катаны тап» sheet. Both
ship in apps/resources/bundled_files/ like the rest of 0029.
"""

from django.db import migrations

NAMES = {
    '5-klass-oyundar-aktivduuluktor-v6.pptx': 'activity',
    '5-klass-katany-tap.pdf': 'worksheet',
}


def add_rows(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    for name, category in NAMES.items():
        if Resource.objects.filter(title=name).exists():
            Resource.objects.filter(title=name).update(is_active=True)
            continue
        Resource.objects.create(
            title=name,
            file=f'resources/files/{name}',
            category=category,
            is_active=True,
        )


def remove_rows(apps, schema_editor):
    # 0029 builds its list from the live data module, so on a fresh
    # database it already made these rows; leave them in place.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0029_four_basic_grade_resources'),
    ]

    operations = [
        migrations.RunPython(add_rows, remove_rows),
    ]
