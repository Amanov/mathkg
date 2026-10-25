"""Create a subtopic or sub-subtopic without repeating its slug.

A subtopic slug is unique for one topic. A sub-subtopic slug is unique
for one subtopic. The menu rebuild used to insert a new row for every
nested «Аралаш» leaf. Those leaves sit on the same subtopic, so several
rows shared the slug ``mixed`` and the topic page raised
MultipleObjectsReturned (HTTP 500).
"""

from apps.resources.models import SubSubtopic, Subtopic


def get_or_create_subtopic(topic, slug, title, extra_defaults=None):
    return _scoped(Subtopic, {'topic': topic}, slug, title, extra_defaults)


def get_or_create_subsubtopic(subtopic, slug, title, extra_defaults=None):
    return _scoped(SubSubtopic, {'subtopic': subtopic}, slug, title, extra_defaults)


def _scoped(model, parent, slug, title, extra_defaults):
    """Return the row for this parent and slug, creating it only if needed.

    A row with the same title under this parent is reused too, so a
    second run of the import does not insert a copy under a new slug.
    """
    row = model.objects.filter(**parent, slug=slug).order_by('pk').first()
    if row is not None:
        return row, False
    row = model.objects.filter(**parent, title=title).order_by('pk').first()
    if row is not None:
        return row, False
    defaults = {'title': title}
    if extra_defaults:
        defaults.update(extra_defaults)
    return model.objects.get_or_create(**parent, slug=slug, defaults=defaults)
