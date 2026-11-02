"""Rename stored topic titles. Slugs and url names stay as they are.

The page address is the slug or the url_name, not the title. This
updates the title text only, on the menu and on topic rows that still
have the old title.
"""

from django.db import migrations


# url_name, previous title, new title. Two different pages can share
# the word IGCSE, so those rows are matched by url_name.
BY_URL = (
    ('geometry_angles_circle_theorems_alternate_segment', 'Алмашма сегмент', 'Сегмент'),
    ('surds_rationalising_without_conjugates', 'Рационалдаштыруу: коньюгатасыз', 'Рационалдаштыруу: түйүндөшсүз'),
    ('with_bidmas_directed', 'BIDMAS менен', 'Амалдардын тартиби менен'),
    ('multiplying_dividing_10_100_1000', '10, 100, 1000гө көбөйтүү жана бөлүү', '10, 100, 1000ге көбөйтүү жана бөлүү'),
    ('integers_multiplying_dividing_10_100_1000', '10, 100, 1000гө көбөйтүү жана бөлүү', '10, 100, 1000ге көбөйтүү жана бөлүү'),
    ('big4', 'Big 4 таймашы', 'Төрт амал таймашы'),
    ('algebra_sequences_linear_summing', 'Суммалоо (IGCSE)', 'Суммалоо'),
    ('geometry_angles_circle_theorems_intersecting_chords', 'Кесилишкен хордалар (IGCSE)', 'Кесилишкен хордалар'),
    ('data_representing_venn_diagrams_sets_with_notation_igcse', 'Жыйындар белгилөө менен (IGCSE)', 'Жыйындар белгилөө менен: татаал'),
    ('algebra_functions_igcse', 'IGCSE', 'Аралаш функциялар'),
    ('algebra_graphs_abstract_transformations_gcse', 'GCSE', 'Жылдыруу жана чагылдыруу'),
    ('algebra_graphs_abstract_transformations_igcse', 'IGCSE', 'Графикти чоюу'),
)

# Titles that belong to one page. Also covers the label these rows had
# before migration 0054 wrote IGCSE over ЖРТ.
BY_TITLE = (
    ('Алмашма сегмент', 'Сегмент'),
    ('Рационалдаштыруу: коньюгатасыз', 'Рационалдаштыруу: түйүндөшсүз'),
    ('Текст маселелер: тилке модели менен', 'Тексттик маселелер: тилке модели менен'),
    ('10, 100, 1000гө көбөйтүү жана бөлүү', '10, 100, 1000ге көбөйтүү жана бөлүү'),
    ('Big 4 таймашы', 'Төрт амал таймашы'),
    ('BIDMAS менен', 'Амалдардын тартиби менен'),
    ('Суммалоо (IGCSE)', 'Суммалоо'),
    ('Суммалоо (ЖРТ)', 'Суммалоо'),
    ('Кесилишкен хордалар (IGCSE)', 'Кесилишкен хордалар'),
    ('Кесилишкен хордалар (ЖРТ)', 'Кесилишкен хордалар'),
    ('Жыйындар белгилөө менен (IGCSE)', 'Жыйындар белгилөө менен: татаал'),
    ('Жыйындар белгилөө менен (ЖРТ)', 'Жыйындар белгилөө менен: татаал'),
)

TITLE_MODELS = ('Topic', 'Subtopic', 'SubSubtopic', 'MenuItem')


def _fill_empty_russian(apps, title):
    from apps.resources.data.russian_names import RUSSIAN_NAMES

    russian = RUSSIAN_NAMES.get(title, '')
    if not russian:
        return
    for model_name in ('Topic', 'Subtopic', 'SubSubtopic'):
        model = apps.get_model('personal', model_name)
        model.objects.filter(title=title, title_ru='').update(title_ru=russian)


def forward(apps, schema_editor):
    MenuItem = apps.get_model('personal', 'MenuItem')
    for url_name, _old, new in BY_URL:
        MenuItem.objects.filter(url_name=url_name).update(title=new)
        _fill_empty_russian(apps, new)
    for old, new in BY_TITLE:
        for model_name in TITLE_MODELS:
            model = apps.get_model('personal', model_name)
            model.objects.filter(title=old).update(title=new)
        _fill_empty_russian(apps, new)


def backward(apps, schema_editor):
    MenuItem = apps.get_model('personal', 'MenuItem')
    for url_name, old, _new in BY_URL:
        MenuItem.objects.filter(url_name=url_name).update(title=old)
    for old, new in BY_TITLE:
        for model_name in TITLE_MODELS:
            model = apps.get_model('personal', model_name)
            model.objects.filter(title=new).update(title=old)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0064_topic_title_ru'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
