"""Bridge topic pages: learning-path rows, downloadable files, menu links.

Page copy and filenames live in data/bridge/pages/. The files themselves
live in bundled_files/bridge/ and are copied onto MEDIA_ROOT the first
time someone downloads them. Grade bands and prev/next links come from
the continuum CSVs.
"""

from django.db import migrations, models


def load_continuum(apps, schema_editor):
    TopicContinuum = apps.get_model('personal', 'TopicContinuum')
    from apps.resources.continuum import load_topic_continuum

    load_topic_continuum(TopicContinuum)


def unload_continuum(apps, schema_editor):
    TopicContinuum = apps.get_model('personal', 'TopicContinuum')
    TopicContinuum.objects.all().delete()


def add_resources_and_menu(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    MenuItem = apps.get_model('personal', 'MenuItem')
    from apps.resources.bridge_menu import apply_bridge_menu
    from apps.resources.bridge_pages import sync_bridge_resources

    sync_bridge_resources(Resource, refresh_media=False)
    apply_bridge_menu(MenuItem)


def remove_resources_and_menu(apps, schema_editor):
    Resource = apps.get_model('personal', 'Resource')
    MenuItem = apps.get_model('personal', 'MenuItem')
    from apps.resources.bridge_pages import referenced_filenames

    Resource.objects.filter(title__in=referenced_filenames()).delete()
    MenuItem.objects.filter(url_name__in=[
        'san_kuramy',
        'on_kozonoktuu_ramka',
        'bar_model_part_whole',
        'bar_model_comparison',
        'word_problems_bar_model',
        'before_after',
        'bar_to_x',
        'balance_method',
        'algebra_tiles',
        'heuristics',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0032_directed_numbers_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicContinuum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('href', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('grade_band', models.CharField(blank=True, max_length=40)),
                ('school_level', models.CharField(blank=True, max_length=40)),
                ('prev_href', models.CharField(blank=True, max_length=255)),
                ('next_href', models.CharField(blank=True, max_length=255)),
                ('path_name', models.CharField(blank=True, max_length=300)),
            ],
            options={
                'verbose_name': 'Окуу жолу',
                'verbose_name_plural': 'Окуу жолдору',
                'ordering': ['href'],
            },
        ),
        migrations.RunPython(load_continuum, unload_continuum),
        migrations.RunPython(add_resources_and_menu, remove_resources_and_menu),
    ]
