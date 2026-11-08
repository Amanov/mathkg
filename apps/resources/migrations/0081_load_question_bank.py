from django.db import migrations


def load(apps, schema_editor):
    from apps.resources.question_bank import load_question_bank

    load_question_bank(apps.get_model('personal', 'Question'), apps.get_model('personal', 'Topic'))


def unload(apps, schema_editor):
    apps.get_model('personal', 'Question').objects.filter(sample_key__startswith='bank-').delete()


class Migration(migrations.Migration):
    """Load the question bank after 0080 has committed its columns and index."""

    dependencies = [
        ('personal', '0080_question_bank_themes'),
    ]

    operations = [
        migrations.RunPython(load, unload),
    ]
