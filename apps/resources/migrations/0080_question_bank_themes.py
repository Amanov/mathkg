from django.db import migrations, models


def load(apps, schema_editor):
    from apps.resources.question_bank import load_question_bank

    load_question_bank(apps.get_model('personal', 'Question'), apps.get_model('personal', 'Topic'))


def unload(apps, schema_editor):
    apps.get_model('personal', 'Question').objects.filter(sample_key__startswith='bank-').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0079_print_copies_a5_a6'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='theme',
            field=models.CharField(blank=True, help_text='Сайттагы пакеттин аты, мисалы «Ондук бөлчөктөрдү кошуу жана кемитүү». Мугалим тест түзгөндө ушул аталышты тандайт.', max_length=200, verbose_name='Бөлүм'),
        ),
        migrations.AddField(
            model_name='question',
            name='theme_slug',
            field=models.SlugField(blank=True, max_length=120, verbose_name='Бөлүмдүн ачкычы'),
        ),
        migrations.RunPython(load, unload),
    ]
