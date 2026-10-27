"""Rename IGCSE menu labels that were stored as ЖРТ.

The page heading comes from the placeholder title, not the database.
The navigation label is a MenuItem title. This updates those five rows
when they still have the old title. It does not add or remove rows, and
there is no ALTER TABLE.

Grades are not stored on a model. This migration does not touch them.

It depends on 0051_refresh_pack_pdf, the leaf on main. Draft PRs #41
and #42 add 0052_bar_to_x_lesson and 0053_refresh_finish_word, both also
depending on 0051. After those land, repoint this migration so it
depends on 0052 and 0053 and the graph has one leaf again.
"""

from django.db import migrations


# (url_name, old title, new title). Only a row that still has the old
# title is renamed, so a later edit is left alone.
RENAMES = (
    ('algebra_functions_igcse', 'ЖРТ', 'IGCSE'),
    ('algebra_graphs_abstract_transformations_igcse', 'ЖРТ', 'IGCSE'),
    ('data_representing_venn_diagrams_sets_with_notation_igcse',
     'Жыйындар белгилөө менен (ЖРТ)', 'Жыйындар белгилөө менен (IGCSE)'),
    ('algebra_sequences_linear_summing', 'Суммалоо (ЖРТ)', 'Суммалоо (IGCSE)'),
    ('geometry_angles_circle_theorems_intersecting_chords',
     'Кесилишкен хордалар (ЖРТ)', 'Кесилишкен хордалар (IGCSE)'),
)


def _rename(apps, forward):
    MenuItem = apps.get_model('personal', 'MenuItem')
    for url_name, old, new in RENAMES:
        source, target = (old, new) if forward else (new, old)
        MenuItem.objects.filter(url_name=url_name, title=source).update(title=target)


def forward(apps, schema_editor):
    _rename(apps, True)


def backward(apps, schema_editor):
    _rename(apps, False)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0051_refresh_pack_pdf'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
