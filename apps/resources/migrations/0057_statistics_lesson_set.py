"""Resource rows for the statistics lesson set.

Files keep the names from the pack and live in bundled_files. The
download view copies one onto the volume when that path is empty.
"""

from django.db import migrations

NAMES = [
    'statistika-sabak-mathkg.pptx',
    'stat-OobaJokBalkim.pptx',
    'stat-OobaJokBalkim.pdf',
    'stat-Korsot.pptx',
    'stat-Korsot.pdf',
    'stat-KadamKadam-A4.pdf',
    'stat-KadamKadam-A4.docx',
    'stat-KadamKadam-Jooptor-A4.pdf',
    'stat-KadamKadam-Jooptor-A4.docx',
    'stat-KoddoAch-A4.pdf',
    'stat-KoddoAch-A4.docx',
    'stat-KoddoAch-Jooptor-A4.pdf',
    'stat-KoddoAch-Jooptor-A4.docx',
    'stat-Bekemdoo-A4.pdf',
    'stat-Bekemdoo-A4.docx',
    'stat-Bekemdoo-Jooptor-A4.pdf',
    'stat-Bekemdoo-Jooptor-A4.docx',
    'stat-Labirint-A4.pdf',
    'stat-Labirint-2bet-A4.pdf',
    'stat-Labirint-Jooptor-A4.pdf',
    'stat-Labirint.pptx',
    'stat-KenchIzdoo.pptx',
    'stat-KenchIzdoo.pdf',
    'stat-Kartochka-A4.pdf',
    'stat-Kartochka-A4.docx',
    'stat-Kartochka-Jooptor-A4.pdf',
    'stat-Kartochka-Jooptor-A4.docx',
    'stat-Blokbaster.pptx',
    'stat-Blokbaster.pdf',
    'stat-MugalimUchun-A4.pdf',
    'stat-MugalimUchun-A4.docx',
    'stat-SabaktyIzildoo-A4.pdf',
    'stat-SabaktyIzildoo-A4.docx',
    'answer-verification.txt',
]


def _category(name):
    if name.endswith('.pptx'):
        return 'presentation'
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
    apps.get_model('personal', 'Resource').objects.filter(title__in=NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0056_missing_continuum_topics'),
    ]

    operations = [
        migrations.RunPython(add_rows, remove_rows),
    ]
