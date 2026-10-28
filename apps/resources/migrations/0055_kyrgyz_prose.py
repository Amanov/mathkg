"""Kyrgyz prose in decks already stored on the media volume.

Decimals use a comma, thousands a narrow space, multiple-choice letters
are А Б В Г, «маселени чеч» is «маселени чыгар», «студент» is «окуучу»,
and «иреттөө» is «ирээттөө». «Чечет» (decides) and «чечүүчү суроо» stay.

Git copies already contain the new sentences. The Railway volume hides
git ``media/``, so a deck already on the volume would keep the old
wording. This rewrites a volume file only when its sha256 is still the
old bytes in ``data/kyrgyz_prose_manifest.json``. The rewrite is the
same in-place text edit, and it is written only when the result hash is
the recorded new hash. A missing file stays missing. Any other hash
stays as it is. Running again is a no-op.

Menu labels that still use the old wording are renamed in place. There
is no ``ALTER TABLE``.

Reversing does not restore the old sentences and does not delete files.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations


# Exact MenuItem titles. A later edit of the same row is left alone.
TITLE_RENAMES = (
    ('Теңдемелерди чечүү', 'Теңдемелерди чыгаруу'),
    ('Кесилишүү аркылуу чечүү', 'Кесилишүү аркылуу чыгаруу'),
    ('Маселе чечүү ыкмалары', 'Маселе чыгаруу ыкмалары'),
    ('Маселе чечүү', 'Маселе чыгаруу'),
    ('Ондуктарды иреттөө', 'Ондуктарды ирээттөө'),
    ('Мезгилдүү ондуктарды иреттөө', 'Мезгилдүү ондуктарды ирээттөө'),
    ('Багытталган сандарды иреттөө', 'Багытталган сандарды ирээттөө'),
    ('Салыштыруу жана иреттөө', 'Салыштыруу жана ирээттөө'),
    ('Бүтүн сандардын орун наркы жана иреттөө', 'Бүтүн сандардын орун наркы жана ирээттөө'),
    ('Бөлчөктөрдү, ондуктарды жана пайыздарды иреттөө', 'Бөлчөктөрдү, ондуктарды жана пайыздарды ирээттөө'),
)


def _rename_titles(apps, forward):
    MenuItem = apps.get_model('personal', 'MenuItem')
    for old, new in TITLE_RENAMES:
        source, target = (old, new) if forward else (new, old)
        MenuItem.objects.filter(title=source).update(title=target)


def forward(apps, schema_editor):
    from apps.resources.kyrgyz_text import refresh_prose_media

    _rename_titles(apps, True)
    refresh_prose_media(Path(settings.MEDIA_ROOT))


def backward(apps, schema_editor):
    _rename_titles(apps, False)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0054_igcse_menu_titles'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
