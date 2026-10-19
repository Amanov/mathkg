"""/directed_numbers/ in the «Төрт амал» layout (2026-10-19).

Adds Resource rows for the three new grade packs (their files ship in
apps/resources/bundled_files/) and points the menu leaf Сандар ›
Амалдардын тартиби › «Багытталган сандар» at that page instead of the
Эсептөөлөр sub-subtopic page, whose activities the new page now lists.
"""

from django.db import migrations

PREFIXES = [
    '5-klass-butun-sandar-koshuu-kemituu-',
    '5-klass-butun-sandar-kobeytuu-boluu-',
    '6-klass-bagyttalgan-sandar-amaldardyn-tartibi-',
]
SUFFIXES = [
    'sabak.pptx', 'oyun-1234.pptx', 'oyun-atyshuu.pptx', 'ish-barak.pdf', 'katany-tap.pdf', 'labirint.pdf',
    'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf', 'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf',
]
NAMES = [p + s for p in PREFIXES for s in SUFFIXES]
LEAF = {'title': 'Багытталган сандар', 'parent__title': 'Амалдардын тартиби', 'parent__parent__title': 'Сандар'}


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
    MenuItem = apps.get_model('personal', 'MenuItem')
    MenuItem.objects.filter(**LEAF).update(
        url_name='directed_numbers', topic=None, subtopic=None, subsubtopic=None,
    )


def backward(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    Resource.objects.filter(title__in=NAMES).delete()
    MenuItem = apps.get_model('personal', 'MenuItem')
    SubSubtopic = apps.get_model('personal', 'SubSubtopic')
    target = SubSubtopic.objects.filter(
        title='Эсептөөлөр', subtopic__title='Багытталган сандар', subtopic__topic__title='Сандар',
    ).select_related('subtopic').first()
    if target:
        MenuItem.objects.filter(**LEAF).update(
            url_name='', topic_id=target.subtopic.topic_id, subtopic_id=target.subtopic_id, subsubtopic=target,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0031_grade_topic_page_resources'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
