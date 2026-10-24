"""Hide the site's older files that were built on goteachmaths templates.

An audit of the site's materials (2026-10-19) found that the files the site
had before our own packs (the «4-Amal…», «BaardykAmaldar…», «Onduktar_…»,
«Ekvivalenettuuluk_…», «KalkulyatorKoldonuu_…» and «Algebra-OneStepVar1Side…»
sets) follow goteachmaths templates. The owner chose to take them off the
site (2026-10-24). Their rows are only marked inactive, so the files stay in
storage and the change can be reversed.
"""

from django.db import migrations
from django.db.models import Q

PREFIXES = [
    '4-amal',
    'baardykamaldar',
    'onduktar_',
    'ekvivalenettuuluk_',
    'kalkulyatorkoldonuu_',
    'algebra-onestepvar1side',
]


def _matching(Resource):
    query = Q()
    for prefix in PREFIXES:
        query |= Q(title__istartswith=prefix)
    return Resource.objects.filter(query)


def hide(apps, schema_editor):
    _matching(apps.get_model('personal', 'Resource')).update(is_active=False)


def show(apps, schema_editor):
    _matching(apps.get_model('personal', 'Resource')).update(is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0032_directed_numbers_page'),
    ]

    operations = [
        migrations.RunPython(hide, show),
    ]
