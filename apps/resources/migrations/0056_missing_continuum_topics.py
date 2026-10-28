"""Open two continuum links that had no topic row.

grade-tags.csv sends teachers to these paths. The rows were never
created, so the links 404'd. The pages stay empty until they have
files. Nothing is renamed.

Depends on 0054 so it can merge beside another migration that also
follows 0054.
"""

from django.db import migrations

PATHS = (
    ('proportion', 'Пропорция', 'percentages-non-calculator', 'Пайыздар: калькуляторсуз',
     'mixed', 'Аралаш'),
    ('algebra', 'Алгебра', 'manipulation', 'Өзгөртүп түзүү',
     'manipulation-proofs', 'Далилдөөлөр'),
)


def forward(apps, schema_editor):
    Topic = apps.get_model('personal', 'Topic')
    Subtopic = apps.get_model('personal', 'Subtopic')
    SubSubtopic = apps.get_model('personal', 'SubSubtopic')
    for topic_slug, topic_title, sub_slug, sub_title, ss_slug, ss_title in PATHS:
        topic, _created = Topic.objects.get_or_create(
            slug=topic_slug, defaults={'title': topic_title},
        )
        subtopic, _created = Subtopic.objects.get_or_create(
            topic=topic, slug=sub_slug, defaults={'title': sub_title},
        )
        SubSubtopic.objects.get_or_create(
            subtopic=subtopic, slug=ss_slug, defaults={'title': ss_title},
        )


def backward(apps, schema_editor):
    Topic = apps.get_model('personal', 'Topic')
    Subtopic = apps.get_model('personal', 'Subtopic')
    SubSubtopic = apps.get_model('personal', 'SubSubtopic')
    for topic_slug, _topic_title, sub_slug, _sub_title, ss_slug, _ss_title in PATHS:
        topic = Topic.objects.filter(slug=topic_slug).first()
        if topic is None:
            continue
        subtopic = Subtopic.objects.filter(topic=topic, slug=sub_slug).first()
        if subtopic is None:
            continue
        SubSubtopic.objects.filter(subtopic=subtopic, slug=ss_slug).delete()
        if not subtopic.subsubtopics.exists():
            subtopic.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0054_igcse_menu_titles'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
