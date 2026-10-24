"""Grade packs on the «даярдалууда» pages (2026-10-24).

Adds Resource rows for six grade packs (perimeter and area, angles,
fractions-decimals-percentages, ratio, expressions and equations, data and
averages). Their files ship in apps/resources/bundled_files/ and
data/pack_pages.py lists the pages each pack fills.
"""

from django.db import migrations

PREFIXES = [
    '5-klass-perimetr-jana-ayant-',
    '5-klass-burchtar-',
    '6-klass-bolchok-ondu-procent-',
    '6-klass-katysh-',
    '6-klass-tamgaluu-tuyuntmalar-tendemeler-',
    '6-klass-maalymat-diagramma-orto-maani-',
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
        ('personal', '0033_hide_template_derived_files'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
