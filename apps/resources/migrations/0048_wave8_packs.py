"""Resource rows for four packs: 4-класс rounding and multi-digit ×÷, 5-класс ×÷ by 10, 100, 1000, 6-класс direct and inverse proportion (see data/pack_pages.py)."""

from django.db import migrations

PREFIXES = [
    '4-klass-tegerektoo-boljoldoo-', '4-klass-kop-orunduu-kobeytuu-boluu-', '5-klass-10-100-1000-', '6-klass-tuz-teskeri-proporciya-',
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
        ('personal', '0047_wave7_packs'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
