"""Resource rows for the grade-level «Төрт амал» materials (1–5-класс).

The files ship in apps/resources/bundled_files/. The download view copies
a bundled file onto MEDIA_ROOT the first time it is asked for, so the
rows only need the path the copy will land at.
"""

from django.db import migrations

from apps.resources.data.four_basic_operations_grades import (
    GRADE_ITEMS,
    GRADE_TEACHER_FILES,
)

GAMES = ('oyun', '1234', 'bingo', 'penalti', 'oyundar')


def _category(name):
    if name.endswith('.pptx'):
        return 'activity' if any(word in name for word in GAMES) else 'presentation'
    return 'worksheet'


def _names():
    names = []
    for _section, item in GRADE_ITEMS:
        names += [name for _label, name in item['files']]
    names += [name for _grade, _subtopic, name in GRADE_TEACHER_FILES]
    return list(dict.fromkeys(names))


def add_rows(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    for name in _names():
        if Resource.objects.filter(title=name).exists():
            Resource.objects.filter(title=name).update(is_active=True)
            continue
        Resource.objects.create(
            title=name,
            file=f'resources/files/{name}',
            category=_category(name),
            is_active=True,
        )


def remove_rows(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    Resource.objects.filter(title__in=_names()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0028_repair_four_basic_free_file'),
    ]

    operations = [
        migrations.RunPython(add_rows, remove_rows),
    ]
