from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# Final target list for Decimals > Arithmetic: 1 Digit, in reference
# order. Slot 1 (Adding) is the one real hand-built page (koshuu_1_digit)
# and is left untouched. Slots 2-8 are now real pages too (see
# apps/resources/views/onduktar_placeholders.py) sharing that page's
# visual design and short-URL convention, replacing the generic
# Topic/Subtopic placeholder pages an earlier version of this command
# created.
TARGET_ITEMS = [
    {'title': 'Кошуу (1 орундук сандар)', 'url_name': 'koshuu_1_digit'},
    {'title': 'Кемитүү — 1 орундуу сандар', 'url_name': 'subtracting_1_digit'},
    {'title': 'Кошуу жана кемитүү — 1 орундуу сандар', 'url_name': 'adding_subtracting_1_digit'},
    {'title': 'Көбөйтүү — 1 орундуу сандар', 'url_name': 'multiplying_1_digit'},
    {'title': 'Бөлүү — 1 орундуу сандар', 'url_name': 'dividing_1_digit'},
    {'title': 'Көбөйтүү жана бөлүү — 1 орундуу сандар', 'url_name': 'multiplying_dividing_1_digit'},
    {'title': 'Аралаш эсептөөлөр — 1 орундуу сандар', 'url_name': 'mixed_1_digit'},
    {'title': '1ден кичине ондукка бөлүү', 'url_name': 'dividing_by_less_than_1'},
]

# Old titles earlier versions of this command (and its predecessor,
# add_leaf_items.py) created as generic Topic/Subtopic SubSubtopic
# placeholders, now superseded by the real pages in TARGET_ITEMS above -
# removed if they hold 0 resources. Includes both the very first
# iteration's 2 titles (Adding/Arithmetic With, before they were known to
# duplicate real pages) and the second iteration's 6, so this cleans up
# fully regardless of which earlier version last ran on a given database.
STALE_SUBSUBTOPIC_TITLES = [
    '1 орундук ондуктарды кошуу',
    '1 орундук ондуктар менен эсептөөлөр',
    '1 орундук ондуктарды кемитүү',
    '1 орундук ондуктарды кошуу жана кемитүү',
    '1 орундук ондуктарды көбөйтүү',
    '1 орундук ондуктарды бөлүү',
    '1 орундук ондуктарды көбөйтүү жана бөлүү',
    '1ден кичине ондукка бөлүү',
]

PARENT = ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 орундук сандар')

# Doesn't correspond to any of the 8 target slots (slot 7 is "Mixed", not
# "Arithmetic With"/general exercises) - removed from the menu entirely
# per explicit instruction ("it will make my menu messy"). The real page
# itself (view, template, URL, any uploaded resources) is untouched -
# only its navigation entry is deleted.
DISPLACED_URL_NAME = 'onedigitarithmetics'


class Command(BaseCommand):
    help = (
        "Rebuilds Decimals > Arithmetic: 1 Digit as the reference's 8 "
        "items (Adding/Subtracting/Adding & Subtracting/Multiplying/"
        "Dividing/Multiplying & Dividing/Mixed/Dividing: Divisor <1). "
        "Adding (koshuu_1_digit) is the one real page and is untouched; "
        "the other 7 are now real pages too (see "
        "onduktar_placeholders.operation_placeholder_view) sharing its "
        "visual design and short-URL convention, replacing the earlier "
        "generic Topic/Subtopic placeholder pages this command used to "
        "create. Removes the now-stale SubSubtopic placeholders (only if "
        "0 resources attached) and removes onedigitarithmetics's menu "
        "entry entirely (the real page/content is untouched, only its "
        "navigation link is deleted) since it doesn't correspond to any "
        "of these 8 slots. Idempotent - safe to re-run."
    )

    def handle(self, *args, **options):
        topic_title, subtopic_title, parent_ss_title = PARENT
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
            return
        except MenuItem.MultipleObjectsReturned:
            self.stderr.write(f'Multiple menu items match "{parent_ss_title}" - resolve first.')
            return

        subtopic = parent_menu.subtopic

        self.stdout.write('--- Removing the displaced general-exercises menu entry ---')
        displaced_qs = MenuItem.objects.filter(url_name=DISPLACED_URL_NAME)
        removed = displaced_qs.count()
        if removed:
            displaced_qs.delete()
            self.stdout.write(
                f'  Removed {removed} menu item(s) linking to {DISPLACED_URL_NAME} '
                f'(the page itself is untouched).'
            )

        self.stdout.write('--- Removing stale generic placeholders ---')
        for title in STALE_SUBSUBTOPIC_TITLES:
            stale = SubSubtopic.objects.filter(subtopic=subtopic, title=title).first()
            if not stale:
                continue
            if stale.resources.exists():
                self.stdout.write(f'  NOT removing "{title}" - has resources attached, check manually.')
                continue
            MenuItem.objects.filter(subsubtopic=stale).delete()
            stale.delete()
            self.stdout.write(f'  Removed stale placeholder "{title}"')

        self.stdout.write('--- Placing the 8 items in reference order ---')
        for order, item in enumerate(TARGET_ITEMS, start=1):
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
