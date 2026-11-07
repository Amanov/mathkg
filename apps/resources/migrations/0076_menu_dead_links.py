"""Give the five menu leaves that link nowhere the same page as their twins
elsewhere in the menu (2026-11-07 menu audit)."""

from django.db import migrations

# (title, parent title) -> url_name, or (topic, subtopic, subsubtopic) slugs.
TARGETS = {
    ('Сызыктарды өлчөө', 'Өлчөмдөр'): ('number', 'measures', 'measuring-lines'),
    ('Шкаланы окуу', 'Өлчөмдөр'): ('number', 'measures', 'reading-scales'),
    ('Аянт жана көлөм бирдиктерин алмаштыруу', 'Өлчөмдөр'): 'compound_area_volume_conversion',
    ('Бөлчөк, пайыз жана катыш эквиваленттүүлүгү', 'Эквиваленттүүлүк'): 'fractions_equiv_fpr',
    ('Бөлчөк, ондук, пайыз жана катыш эквиваленттүүлүгү', 'Эквиваленттүүлүк'): 'fractions_equiv_fdpr',
}


def forward(apps, schema_editor):
    MenuItem = apps.get_model('personal', 'MenuItem')
    SubSubtopic = apps.get_model('personal', 'SubSubtopic')
    dead = MenuItem.objects.filter(
        url_name__isnull=True, topic__isnull=True, subtopic__isnull=True, subsubtopic__isnull=True,
        children__isnull=True,
    ).select_related('parent')
    for item in dead:
        target = TARGETS.get((item.title, item.parent.title if item.parent else None))
        if target is None:
            continue
        if isinstance(target, str):
            item.url_name = target
        else:
            leaf = SubSubtopic.objects.filter(
                slug=target[2], subtopic__slug=target[1],
                subtopic__topic__slug__in=[target[0], 'sandar-local'],
            ).select_related('subtopic__topic').first()
            if leaf is None:
                continue
            item.topic, item.subtopic, item.subsubtopic = leaf.subtopic.topic, leaf.subtopic, leaf
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0075_wave15_packs'),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop),
    ]
