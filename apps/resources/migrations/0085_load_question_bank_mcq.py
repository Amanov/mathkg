from django.db import migrations


def load(apps, schema_editor):
    """Add the multiple-choice questions built from each pack's domino cards (loading is idempotent)."""
    from apps.resources.question_bank import load_question_bank

    load_question_bank(apps.get_model('personal', 'Question'), apps.get_model('personal', 'Topic'))


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0084_load_question_bank_wave18'),
    ]

    operations = [
        migrations.RunPython(load, migrations.RunPython.noop),
    ]
