"""Resource rows for four packs: 6-класс percent, 4-класс unit conversion, 3-класс data collecting, 5-класс Venn diagrams (see data/pack_pages.py)."""

from django.db import migrations

PREFIXES = [
    '6-klass-payyz-', '4-klass-birdikterdi-almashtyruu-', '3-klass-maalymat-chogultuu-', '5-klass-venn-diagrammalary-',
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
        ('personal', '0046_subsubtopic_subtopic_slug_uniq'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
