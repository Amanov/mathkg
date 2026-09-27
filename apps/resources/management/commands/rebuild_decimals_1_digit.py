from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# Each entry rebuilds one sub-subtopic's children as a reference-ordered
# list of real pages (see apps/resources/views/onduktar_placeholders.py +
# templates/resources/onduktar/operation_placeholder.html - all share
# koshuu_1_digit's visual design and its short-URL convention instead of
# the long generic /resources/topic/number/... path). Add a new dict here
# for the next sub-subtopic that needs the same treatment; this command
# processes every group in one run.
GROUPS = [
    {
        # Slot 1 (Adding) is the one real hand-built page (koshuu_1_digit)
        # and is left untouched; slots 2-8 are real pages too now.
        'parent_path': ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 орундук сандар'),
        'target_items': [
            {'title': 'Кошуу (1 орундук сандар)', 'url_name': 'koshuu_1_digit'},
            {'title': 'Кемитүү — 1 орундуу сандар', 'url_name': 'subtracting_1_digit'},
            {'title': 'Кошуу жана кемитүү — 1 орундуу сандар', 'url_name': 'adding_subtracting_1_digit'},
            {'title': 'Көбөйтүү — 1 орундуу сандар', 'url_name': 'multiplying_1_digit'},
            {'title': 'Бөлүү — 1 орундуу сандар', 'url_name': 'dividing_1_digit'},
            {'title': 'Көбөйтүү жана бөлүү — 1 орундуу сандар', 'url_name': 'multiplying_dividing_1_digit'},
            {'title': 'Аралаш эсептөөлөр — 1 орундуу сандар', 'url_name': 'mixed_1_digit'},
            {'title': '1ден кичине ондукка бөлүү', 'url_name': 'dividing_by_less_than_1'},
        ],
        # Old titles earlier versions of this command (and its
        # predecessor, add_leaf_items.py) created as generic
        # Topic/Subtopic SubSubtopic placeholders, now superseded by the
        # real pages above - removed if they hold 0 resources.
        'stale_subsubtopic_titles': [
            '1 орундук ондуктарды кошуу',
            '1 орундук ондуктар менен эсептөөлөр',
            '1 орундук ондуктарды кемитүү',
            '1 орундук ондуктарды кошуу жана кемитүү',
            '1 орундук ондуктарды көбөйтүү',
            '1 орундук ондуктарды бөлүү',
            '1 орундук ондуктарды көбөйтүү жана бөлүү',
            '1ден кичине ондукка бөлүү',
        ],
        # Doesn't correspond to any of the 8 target slots (slot 7 is
        # "Mixed", not "Arithmetic With"/general exercises) - removed
        # from the menu entirely per explicit instruction ("it will make
        # my menu messy"). The real page itself (view, template, URL, any
        # uploaded resources) is untouched - only its navigation entry is
        # deleted.
        'displaced_url_names': ['onedigitarithmetics'],
    },
    {
        # None of these 8 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 жана 2 орундук сандар'),
        'target_items': [
            {'title': 'Кошуу — 1 жана 2 орундук сандар', 'url_name': 'adding_1_2_digit'},
            {'title': 'Кемитүү — 1 жана 2 орундук сандар', 'url_name': 'subtracting_1_2_digit'},
            {'title': 'Кошуу жана кемитүү — 1 жана 2 орундук сандар', 'url_name': 'adding_subtracting_1_2_digit'},
            {'title': 'Көбөйтүү — 1 жана 2 орундук сандар', 'url_name': 'multiplying_1_2_digit'},
            {'title': 'Бөлүү — 1 жана 2 орундук сандар', 'url_name': 'dividing_1_2_digit'},
            {'title': 'Көбөйтүү жана бөлүү — 1 жана 2 орундук сандар', 'url_name': 'multiplying_dividing_1_2_digit'},
            {'title': '10, 100, 1000гө көбөйтүү жана бөлүү', 'url_name': 'multiplying_dividing_10_100_1000'},
            {'title': 'Аралаш эсептөөлөр — 1 жана 2 орундук сандар', 'url_name': 'mixed_1_2_digit'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
]


class Command(BaseCommand):
    help = (
        "Rebuilds each sub-subtopic listed in GROUPS as its reference-"
        "ordered list of real pages (see "
        "onduktar_placeholders.operation_placeholder_view), replacing any "
        "generic Topic/Subtopic placeholder pages an earlier version of "
        "this command created for it. For each group: removes any "
        "'displaced_url_names' menu entries that don't correspond to any "
        "target slot (the real page/content itself is untouched, only "
        "its navigation link is deleted); removes 'stale_subsubtopic_"
        "titles' placeholders (only if 0 resources attached); then "
        "creates/repositions the target items in order. Idempotent - "
        "safe to re-run, and safe to run after adding a new group."
    )

    def handle(self, *args, **options):
        for group in GROUPS:
            topic_title, subtopic_title, parent_ss_title = group['parent_path']
            self.stdout.write(f'=== {" > ".join(group["parent_path"])} ===')
            try:
                parent_menu = MenuItem.objects.get(
                    title=parent_ss_title,
                    parent__title=subtopic_title,
                    parent__parent__title=topic_title,
                )
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'  "{" > ".join(group["parent_path"])}" not found - '
                    f'run import_reference_taxonomy / fix_number_menu first.'
                )
                continue
            except MenuItem.MultipleObjectsReturned:
                self.stderr.write(f'  Multiple menu items match "{parent_ss_title}" - resolve first.')
                continue

            subtopic = parent_menu.subtopic

            for url_name in group['displaced_url_names']:
                displaced_qs = MenuItem.objects.filter(url_name=url_name)
                removed = displaced_qs.count()
                if removed:
                    displaced_qs.delete()
                    self.stdout.write(
                        f'  Removed {removed} menu item(s) linking to {url_name} '
                        f'(the page itself is untouched).'
                    )

            for title in group['stale_subsubtopic_titles']:
                stale = SubSubtopic.objects.filter(subtopic=subtopic, title=title).first()
                if not stale:
                    continue
                if stale.resources.exists():
                    self.stdout.write(f'  NOT removing "{title}" - has resources attached, check manually.')
                    continue
                MenuItem.objects.filter(subsubtopic=stale).delete()
                stale.delete()
                self.stdout.write(f'  Removed stale placeholder "{title}"')

            for order, item in enumerate(group['target_items'], start=1):
                leaf, created = MenuItem.objects.get_or_create(
                    url_name=item['url_name'],
                    defaults={'title': item['title'], 'parent': parent_menu, 'order': order},
                )
                if created:
                    self.stdout.write(f'  Created: {item["title"]} ({item["url_name"]})')
                    continue
                changed = (
                    leaf.parent_id != parent_menu.id or leaf.order != order
                    or leaf.title != item['title']
                    or leaf.topic_id or leaf.subtopic_id or leaf.subsubtopic_id
                )
                if changed:
                    leaf.parent = parent_menu
                    leaf.order = order
                    leaf.title = item['title']
                    leaf.topic = None
                    leaf.subtopic = None
                    leaf.subsubtopic = None
                    leaf.save(update_fields=['parent', 'order', 'title', 'topic', 'subtopic', 'subsubtopic'])
                    self.stdout.write(f'  Positioned: {item["title"]} ({item["url_name"]})')

        self.stdout.write(self.style.SUCCESS('Done.'))
