"""Rename IGCSE menu labels that were stored as ЖРТ.

The page heading comes from the placeholder title, not the database.
The navigation label is a MenuItem title. This updates those five rows
when they still have the old title. It does not add or remove rows, and
there is no ALTER TABLE.

Grades are not stored on a model. This migration does not touch them.

0052_bar_to_x_lesson is on main. 0053_refresh_finish_word follows it
on the finish-word pull request. This migration follows 0053, so once
that pull request merges the graph has one leaf. It does not include
that pull request's other files.
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
        ('personal', '0053_refresh_finish_word'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
