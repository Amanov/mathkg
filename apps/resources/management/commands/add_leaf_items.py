from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# 4th-level worksheet-title items shown on the reference site, one tier
# below a sub-subtopic. Each gets its own real SubSubtopic (title + slug)
# under the same Subtopic as its parent, so its placeholder page shows
# its own specific name (e.g. "1 орундук ондуктарды кошуу") instead of
# sharing the parent's page and title. Its MenuItem nests visually under
# the parent sub-subtopic's MenuItem, matching the reference's layout.
# Keyed by (topic title, subtopic title, parent sub-subtopic title) ->
# list of (leaf title, slug).
LEAF_ITEMS = {
    ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 орундук сандар'): [
        ('1 орундук ондуктарды кошуу', 'adding-1-digit'),
        ('1 орундук ондуктарды кемитүү', 'subtracting-1-digit'),
        ('1 орундук ондуктарды кошуу жана кемитүү', 'adding-subtracting-1-digit'),
        ('1 орундук ондуктарды көбөйтүү', 'multiplying-1-digit'),
        ('1 орундук ондуктарды бөлүү', 'dividing-1-digit'),
        ('1 орундук ондуктарды көбөйтүү жана бөлүү', 'multiplying-dividing-1-digit'),
        ('1 орундук ондуктар менен эсептөөлөр', 'arithmetic-with-1-digit'),
        ('1ден кичине ондукка бөлүү', 'dividing-by-less-than-1'),
    ],
}


class Command(BaseCommand):
    help = (
        "Adds 4th-level worksheet-title items (from the reference site, "
        "one tier below a sub-subtopic) as real, distinctly-named "
        "SubSubtopics - each gets its own placeholder page titled after "
        "its specific operation, nested visually under its parent "
        "sub-subtopic's menu item. See LEAF_ITEMS for what's covered. "
        "Idempotent - safe to re-run."
    )

    def handle(self, *args, **options):
        for (topic_title, subtopic_title, parent_ss_title), items in LEAF_ITEMS.items():
            try:
                parent_menu = MenuItem.objects.get(
                    title=parent_ss_title,
                    parent__title=subtopic_title,
                    parent__parent__title=topic_title,
                )
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'"{topic_title} > {subtopic_title} > {parent_ss_title}" not found - '
                    f'run import_reference_taxonomy / fix_number_menu first.'
                )
                continue
            except MenuItem.MultipleObjectsReturned:
                self.stderr.write(
                    f'Multiple menu items match "{topic_title} > {subtopic_title} > '
                    f'{parent_ss_title}" - resolve the duplicate first.'
                )
                continue

            subtopic = parent_menu.subtopic
            topic = parent_menu.topic
            if not subtopic or not topic:
                self.stderr.write(
                    f'"{parent_ss_title}" has no topic/subtopic link - '
                    f'run import_reference_taxonomy first.'
                )
                continue

            for order, (title, slug) in enumerate(items, start=1):
                subsubtopic, created = SubSubtopic.objects.get_or_create(
                    subtopic=subtopic, title=title, defaults={'slug': slug},
                )
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f'  {verb} SubSubtopic: {subtopic_title} > {title}')

                leaf, created = MenuItem.objects.get_or_create(
                    title=title, parent=parent_menu,
                    defaults={
                        'order': order, 'topic': topic,
                        'subtopic': subtopic, 'subsubtopic': subsubtopic,
                    },
                )
                if not created and leaf.subsubtopic_id != subsubtopic.id:
                    leaf.subsubtopic = subsubtopic
                    leaf.save(update_fields=['subsubtopic'])
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f'  {verb} MenuItem: {parent_ss_title} > {title}')

        self.stdout.write(self.style.SUCCESS('Done.'))
