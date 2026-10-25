"""One slug per subtopic, after the 0043 dedupe has committed.

Separate from 0045 so each ALTER TABLE is its own transaction.
A database that already has the constraint skips the ALTER.
"""

from django.db import migrations, models

from apps.resources.migrations._constraint_ops import add_if_missing, drop_if_present

CONSTRAINT = models.UniqueConstraint(
    fields=['subtopic', 'slug'],
    name='personal_subsubtopic_subtopic_slug_uniq',
)


def forwards(apps, schema_editor):
    add_if_missing(apps, schema_editor, 'SubSubtopic', CONSTRAINT)


def backwards(apps, schema_editor):
    drop_if_present(apps, schema_editor, 'SubSubtopic', CONSTRAINT)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0045_subtopic_topic_slug_uniq'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddConstraint(model_name='subsubtopic', constraint=CONSTRAINT),
            ],
            database_operations=[
                migrations.RunPython(forwards, backwards),
            ],
        ),
    ]
