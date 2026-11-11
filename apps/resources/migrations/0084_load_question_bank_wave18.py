from django.db import migrations


def load(apps, schema_editor):
    """Add the four wave-18 packs' questions to the test maker (loading is idempotent)."""
    from apps.resources.question_bank import load_question_bank

    load_question_bank(apps.get_model('personal', 'Question'), apps.get_model('personal', 'Topic'))


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0083_wave18_packs'),
    ]

    operations = [
        migrations.RunPython(load, migrations.RunPython.noop),
    ]
