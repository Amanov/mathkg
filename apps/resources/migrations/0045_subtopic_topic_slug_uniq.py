"""One slug per topic, after the 0043 dedupe has committed.

See 0043. This is its own migration so Postgres runs the ALTER TABLE
after the deferred foreign-key triggers from that dedupe have fired.
A database that already has the constraint (the old combined 0043)
skips the ALTER.
"""

from django.db import migrations, models

from apps.resources.migrations._constraint_ops import add_if_missing, drop_if_present

CONSTRAINT = models.UniqueConstraint(
    fields=['topic', 'slug'],
    name='personal_subtopic_topic_slug_uniq',
)


def forwards(apps, schema_editor):
    add_if_missing(apps, schema_editor, 'Subtopic', CONSTRAINT)


def backwards(apps, schema_editor):
    drop_if_present(apps, schema_editor, 'Subtopic', CONSTRAINT)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0044_wave6_packs'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddConstraint(model_name='subtopic', constraint=CONSTRAINT),
            ],
            database_operations=[
                migrations.RunPython(forwards, backwards),
            ],
        ),
    ]
