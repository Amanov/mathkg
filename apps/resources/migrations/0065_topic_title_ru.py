"""Optional Russian name stored for search metadata. Pages stay in Kyrgyz."""

from django.db import migrations, models


def fill_russian_names(apps, schema_editor):
    from apps.resources.data.russian_names import RUSSIAN_NAMES

    for model_name in ('Topic', 'Subtopic', 'SubSubtopic'):
        model = apps.get_model('personal', model_name)
        for row in model.objects.all().iterator():
            russian = RUSSIAN_NAMES.get(row.title, '')
            if russian and not row.title_ru:
                row.title_ru = russian
                row.save(update_fields=['title_ru'])


def clear_russian_names(apps, schema_editor):
    for model_name in ('Topic', 'Subtopic', 'SubSubtopic'):
        apps.get_model('personal', model_name).objects.update(title_ru='')


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0064_refresh_maze_paths'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='title_ru',
            field=models.CharField(
                blank=True,
                help_text='Издөө үчүн гана. Барактын өзү кыргызча бойдон калат.',
                max_length=200,
                verbose_name='Орусча аталыш',
            ),
        ),
        migrations.AddField(
            model_name='subtopic',
            name='title_ru',
            field=models.CharField(
                blank=True,
                help_text='Издөө үчүн гана. Барактын өзү кыргызча бойдон калат.',
                max_length=200,
                verbose_name='Орусча аталыш',
            ),
        ),
        migrations.AddField(
            model_name='subsubtopic',
            name='title_ru',
            field=models.CharField(
                blank=True,
                help_text='Издөө үчүн гана. Барактын өзү кыргызча бойдон калат.',
                max_length=200,
                verbose_name='Орусча аталыш',
            ),
        ),
        migrations.RunPython(fill_russian_names, clear_russian_names),
    ]
