"""Resource rows for the files that three topic pages add (2026-10-19).

/koshuu-1-digit/, /integers-adding-subtracting-1-2-digit/ and
/hcf-lcm-prime-factorisation-mixed/ now use the «Төрт амал» layout. Their
new files ship in apps/resources/bundled_files/; the download view copies
one onto MEDIA_ROOT the first time it is asked for.
"""

from django.db import migrations

NAMES = [
    'koshuu-1-digit-LessonDeck.pptx',
    'koshuu-1-digit-print.pdf',
    'integers-adding-subtracting-1-2-digit-LessonDeck.pptx',
    '2-klass-100-ichinde-klassta-koldonuu-v2.pdf',
    '6-klass-jonokoy-kobeytuuchuler-sabak.pptx',
    '6-klass-jonokoy-kobeytuuchuler-oyun-1234.pptx',
    '6-klass-jonokoy-kobeytuuchuler-oyun-atyshuu.pptx',
    '6-klass-jonokoy-kobeytuuchuler-ish-barak.pdf',
    '6-klass-jonokoy-kobeytuuchuler-katany-tap.pdf',
    '6-klass-jonokoy-kobeytuuchuler-labirint.pdf',
    '6-klass-jonokoy-kobeytuuchuler-domino.pdf',
    '6-klass-jonokoy-kobeytuuchuler-karta-sorttoo.pdf',
    '6-klass-jonokoy-kobeytuuchuler-cifra-tabyshmagy.pdf',
    '6-klass-jonokoy-kobeytuuchuler-klassta-koldonuu.pdf',
    '6-klass-jonokoy-kobeytuuchuler-mugalim-kartasy.pdf',
]
GAMES = ('oyun',)


def _category(name):
    if name.endswith('.pptx'):
        return 'activity' if any(word in name for word in GAMES) else 'presentation'
    return 'worksheet'


def add_rows(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    for name in NAMES:
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
    Resource.objects.filter(title__in=NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0030_four_basic_grade5_fixes'),
    ]

    operations = [
        migrations.RunPython(add_rows, remove_rows),
    ]
