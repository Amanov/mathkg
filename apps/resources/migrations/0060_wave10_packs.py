"""Resource rows for five 6-класс packs: substitution, equations with the unknown on both sides, multiplying and dividing terms, ratio 1 : n and combining, questionnaires and two-way tables (see data/pack_pages.py)."""

from django.db import migrations

PREFIXES = [
    '6-klass-maanisin-eseptoo-', '6-klass-tendemeler-eki-tarap-', '6-klass-tamgaluu-kobeytuu-boluu-',
    '6-klass-katysh-1-n-', '6-klass-anketa-eki-tarap-tablica-',
]
SUFFIXES = [
    'sabak.pptx', 'oyun-1234.pptx', 'oyun-atyshuu.pptx', 'ish-barak.pdf', 'katany-tap.pdf', 'labirint.pdf',
    'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf', 'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf',
]
NAMES = [p + s for p in PREFIXES for s in SUFFIXES]


def _category(name):
    if name.endswith('.pptx'):
        return 'activity' if 'oyun' in name else 'presentation'
    return 'worksheet'


def forward(apps, schema_editor):
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


def backward(apps, schema_editor):
    apps.get_model('personal', 'Resource').objects.filter(title__in=NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0059_wave9_packs'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
