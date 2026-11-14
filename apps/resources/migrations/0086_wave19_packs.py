"""Resource rows for four grade 1–2 packs (2026-11-14): grade 1 numbers to 20, grade 1 adding and subtracting
within 20, grade 2 money (som and change), grade 2 multiplying by 5 and 10. See data/pack_pages.py.
The pupil print sheets also get their A5 and A6 copies, as in 0079."""

from django.db import migrations

PREFIXES = [
    '1-klass-20-ichindegi-sandar-', '1-klass-20-ichinde-koshuu-kemituu-', '2-klass-akcha-som-',
    '2-klass-5ke-10go-kobotuu-',
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
        ('personal', '0085_load_question_bank_mcq'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
