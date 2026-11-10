"""Resource rows for four packs that fill the last empty class-page topics (2026-11-10): grade 9 coordinates
(perpendicular lines, dividing a segment in a ratio), grade 8 filling graphs, grade 7 data types, sampling and
composite bar charts, grade 8 algebra (three brackets, proof, trial and improvement). See data/pack_pages.py.
The pupil print sheets also get their A5 and A6 copies, as in 0079."""

from django.db import migrations

PREFIXES = [
    '9-klass-koordinattar-metodu-', '8-klass-toltuu-grafikteri-', '7-klass-maalymat-tandoo-',
    '8-klass-algebra-dalildoo-',
]
SUFFIXES = [
    'sabak.pptx', 'oyun-1234.pptx', 'oyun-jydymay.pptx', 'ish-barak.pdf', 'katany-tap.pdf', 'labirint.pdf',
    'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf', 'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf',
]
PRINT = ['ish-barak', 'katany-tap', 'labirint', 'cifra-tabyshmagy', 'domino', 'karta-sorttoo']
NAMES = [p + s for p in PREFIXES for s in SUFFIXES]
COPIES = [f'{p}{s}-{size}.pdf' for p in PREFIXES for s in PRINT for size in ('a5', 'a6')]


def _category(name):
    if name.endswith('.pptx'):
        return 'activity' if 'oyun' in name else 'presentation'
    return 'worksheet'


def forward(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    for name in NAMES + COPIES:
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
    apps.get_model('personal', 'Resource').objects.filter(title__in=NAMES + COPIES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0082_rename_atyshuu_to_jydymay'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
