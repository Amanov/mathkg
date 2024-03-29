# Generated by Django 4.2 on 2023-08-29 18:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personal', '0002_delete_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='pdfFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ppt', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
            ],
        ),
    ]
