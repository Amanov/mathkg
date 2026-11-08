from django.db import migrations, models


# Schema only. The rows are loaded in 0081: on PostgreSQL the new index on
# theme_slug cannot be built in the same transaction as the inserted rows
# («cannot CREATE INDEX … because it has pending trigger events»).


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
    ]
