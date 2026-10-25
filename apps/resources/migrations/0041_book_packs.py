"""Resource rows for the earlier book-topic packs that data/pack_pages.py now
puts on more pages."""

from django.db import migrations

SUFFIXES = [
    'sabak.pptx', 'oyun-1234.pptx', 'oyun-atyshuu.pptx', 'ish-barak.pdf', 'katany-tap.pdf', 'labirint.pdf',
    'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf', 'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf',
]
PACKS = [
    ('2-klass-100-ichinde-', '-v2'), ('3-klass-jadybal-', '-v2'), ('6-klass-bolunuu-belgileri-', '-v2'),
    ('1-klass-10-ichinde-kemituu-', ''), ('2-klass-kobeytuu-2-3-4-', ''), ('3-klass-mamycha-koshuu-kemituu-', ''),
    ('3-klass-sandyn-bolugu-', ''), ('4-klass-million-ichinde-', ''), ('5-klass-kadimki-bolchoktor-', ''),
    ('6-klass-proporciya-procent-', ''), ('6-klass-jonokoy-kobeytuuchuler-', ''),
]
NAMES = [p + s.replace('.', tail + '.') for p, tail in PACKS for s in SUFFIXES]


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
    # Some of these rows came from earlier migrations (0031, 0032), so
    # reversing this one leaves them all in place.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0040_five_packs'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
