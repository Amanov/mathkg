from django.db import migrations


def load(apps, schema_editor):
    """Load the questions of the four grade 1–2 packs added in 0086 (loading is idempotent)."""
    from apps.resources.question_bank import load_question_bank

    load_question_bank(apps.get_model('personal', 'Question'), apps.get_model('personal', 'Topic'))


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0086_wave19_packs'),
    ]

    operations = [
        migrations.RunPython(load, migrations.RunPython.noop),
    ]
