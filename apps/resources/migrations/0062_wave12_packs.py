"""Resource rows for five grade 8–9 algebra packs: square roots, algebraic fractions, inequalities, quadratic function, sequences and progressions (see data/pack_pages.py)."""

from django.db import migrations

PREFIXES = [
    '8-klass-kvadrat-tamyr-', '8-klass-algebralyk-bolchoktor-', '8-klass-barabarsyzdyktar-',
    '9-klass-kvadrattyk-funkciya-', '9-klass-progressiyalar-',
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
        ('personal', '0061_wave11_packs'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
