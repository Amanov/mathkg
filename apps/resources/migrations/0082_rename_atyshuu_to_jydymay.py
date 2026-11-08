"""Rename the «Атышуу» team game to «Жыдымай» (2026-11-08).

«Атышуу» sounds like a fight with weapons; «Жыдымай» is the word for
being out of the game. The decks were renamed in
apps/resources/bundled_files/ (*-oyun-jydymay.pptx, title slide edited).
Pointing the rows at the new names also means the download view copies
the edited deck onto the media volume instead of serving the old copy
that is already there.
"""

from django.db import migrations

OLD, NEW = 'oyun-atyshuu', 'oyun-jydymay'


def _rename(apps, old, new):
    Resource = apps.get_model('personal', 'Resource')
    for row in Resource.objects.filter(title__contains=old):
        title = row.title.replace(old, new)
        if Resource.objects.filter(title=title).exclude(pk=row.pk).exists():
            # A fresh database can already hold a row under the new name
            # (an earlier migration reads the current page data). Keep that
            # one and retire the duplicate instead of deleting its history.
            if row.is_active:
                row.is_active = False
                row.save(update_fields=['is_active'])
            continue
        row.title = title
        row.file.name = (row.file.name or '').replace(old, new)
        row.save(update_fields=['title', 'file'])


def forward(apps, schema_editor):
    _rename(apps, OLD, NEW)


def backward(apps, schema_editor):
    _rename(apps, NEW, OLD)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0081_load_question_bank'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
