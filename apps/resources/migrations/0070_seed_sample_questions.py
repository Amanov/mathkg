from django.db import migrations


def seed(apps, schema_editor):
    from apps.resources.sample_questions import seed_sample_questions

    Question = apps.get_model('personal', 'Question')
    Topic = apps.get_model('personal', 'Topic')
    seed_sample_questions(Question, Topic)


def unseed(apps, schema_editor):
    Question = apps.get_model('personal', 'Question')
    Topic = apps.get_model('personal', 'Topic')
    Question.objects.filter(sample_key__startswith='ulgu-').delete()
    for slug in ('ulgu-bolchoktor', 'ulgu-onduktar'):
        topic = Topic.objects.filter(slug=slug).first()
        if topic is not None and not Question.objects.filter(topic=topic).exists():
            topic.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0069_question_bank'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
