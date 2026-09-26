from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem

# 4th-level worksheet-title items shown on the reference site, one tier
# below a sub-subtopic. There's no model level below SubSubtopic, so each
# of these shares its parent's SubSubtopic (and therefore its placeholder
# page) rather than getting a distinct page of its own - honest about
# there being no distinct content yet, while still showing the full
# planned breakdown from the reference instead of a dead "#" link.
# Keyed by (topic title, subtopic title, subsubtopic title).
LEAF_ITEMS = {
    ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 орундук сандар'): [
        '1 орундук ондуктарды кошуу',
        '1 орундук ондуктарды кемитүү',
        '1 орундук ондуктарды кошуу жана кемитүү',
        '1 орундук ондуктарды көбөйтүү',
        '1 орундук ондуктарды бөлүү',
        '1 орундук ондуктарды көбөйтүү жана бөлүү',
        '1 орундук ондуктар менен эсептөөлөр',
        '1ден кичине ондукка бөлүү',
    ],
}


class Command(BaseCommand):
    help = (
        "Adds 4th-level worksheet-title menu items (from the reference "
        "site, one tier below a sub-subtopic) as pure navigation labels "
        "sharing their parent's SubSubtopic - so they resolve to the same "
        "placeholder page rather than being dead links, since no distinct "
        "content exists for them yet. See LEAF_ITEMS for what's covered. "
        "Idempotent - safe to re-run."
    )

    def handle(self, *args, **options):
        for (topic_title, subtopic_title, subsubtopic_title), titles in LEAF_ITEMS.items():
            try:
                parent = MenuItem.objects.get(
                    title=subsubtopic_title,
                    parent__title=subtopic_title,
                    parent__parent__title=topic_title,
                )
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'"{topic_title} > {subtopic_title} > {subsubtopic_title}" not found - '
                    f'run import_reference_taxonomy / fix_number_menu first.'
                )
                continue
            except MenuItem.MultipleObjectsReturned:
                self.stderr.write(
                    f'Multiple menu items match "{topic_title} > {subtopic_title} > '
                    f'{subsubtopic_title}" - resolve the duplicate first.'
                )
                continue

            for order, title in enumerate(titles, start=1):
                leaf, created = MenuItem.objects.get_or_create(
                    title=title, parent=parent,
                    defaults={
                        'order': order,
                        'topic': parent.topic,
                        'subtopic': parent.subtopic,
                        'subsubtopic': parent.subsubtopic,
                    },
                )
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f'  {verb}: {subsubtopic_title} > {title}')

        self.stdout.write(self.style.SUCCESS('Done.'))
