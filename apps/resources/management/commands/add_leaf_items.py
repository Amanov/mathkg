from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# 4th-level worksheet-title items shown on the reference site, one tier
# below a sub-subtopic, in the reference's own order. Two of the 8 slots
# under Decimals > Arithmetic: 1 Digit already have real hand-built pages
# covering that exact operation (koshuu_1_digit = "Addition - 1-digit
# numbers", onedigitarithmetics = general 1-digit exercises) - those are
# given by url_name and reuse the existing MenuItem/real page rather than
# getting a redundant empty placeholder. The rest get their own real
# SubSubtopic (own slug, own title) so each has a distinctly-titled
# placeholder page. Keyed by (topic title, subtopic title, parent
# sub-subtopic title) -> ordered list of {'title', and either 'slug' (new
# placeholder) or 'url_name' (reuse an existing real page)}.
LEAF_ITEMS = {
    ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 орундук сандар'): [
        {'title': 'Кошуу (1 орундук сандар)', 'url_name': 'koshuu_1_digit'},
        {'title': '1 орундук ондуктарды кемитүү', 'slug': 'subtracting-1-digit'},
        {'title': '1 орундук ондуктарды кошуу жана кемитүү', 'slug': 'adding-subtracting-1-digit'},
        {'title': '1 орундук ондуктарды көбөйтүү', 'slug': 'multiplying-1-digit'},
        {'title': '1 орундук ондуктарды бөлүү', 'slug': 'dividing-1-digit'},
        {'title': '1 орундук ондуктарды көбөйтүү жана бөлүү', 'slug': 'multiplying-dividing-1-digit'},
        {'title': '1 орундук сандар менен көнүгүүлөр', 'url_name': 'onedigitarithmetics'},
        {'title': '1ден кичине ондукка бөлүү', 'slug': 'dividing-by-less-than-1'},
    ],
}

# Placeholder SubSubtopics created by an earlier version of this command
# for the 2 slots above that turned out to already have real pages
# (koshuu_1_digit, onedigitarithmetics) - removed so the real pages take
# their place instead of sitting alongside a redundant empty one.
STALE_SLUGS = ['adding-1-digit', 'arithmetic-with-1-digit']


class Command(BaseCommand):
    help = (
        "Adds 4th-level worksheet-title items (from the reference site, "
        "one tier below a sub-subtopic) in the reference's order. A slot "
        "that already has a real hand-built page (given by url_name) "
        "reuses that page instead of getting a redundant placeholder; "
        "everything else gets its own real, distinctly-named SubSubtopic. "
        "Also removes any stale placeholder this command previously "
        "created for a slot that turned out to already have real content "
        "(see STALE_SLUGS). See LEAF_ITEMS for what's covered. Idempotent "
        "- safe to re-run."
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

            self.stdout.write('--- Removing stale placeholders now covered by real pages ---')
            for slug in STALE_SLUGS:
                stale = SubSubtopic.objects.filter(subtopic=subtopic, slug=slug).first()
                if not stale:
                    continue
                if stale.resources.exists():
                    self.stdout.write(
                        f'  NOT removing "{stale.title}" - has real resources attached, '
                        f'check manually.'
                    )
                    continue
                MenuItem.objects.filter(subsubtopic=stale).delete()
                self.stdout.write(f'  Removed stale placeholder "{stale.title}"')
                stale.delete()

            self.stdout.write('--- Placing the 8 items in reference order ---')
            for order, item in enumerate(items, start=1):
                title = item['title']

                if 'url_name' in item:
                    try:
                        leaf = MenuItem.objects.get(url_name=item['url_name'])
                    except MenuItem.DoesNotExist:
                        self.stdout.write(f'  No menu item links to {item["url_name"]} - skipping.')
                        continue
                    except MenuItem.MultipleObjectsReturned:
                        self.stderr.write(
                            f'  Multiple menu items link to {item["url_name"]} - resolve manually first.'
                        )
                        continue
                    changed = (
                        leaf.parent_id != parent_menu.id or leaf.order != order
                        or leaf.topic_id or leaf.subtopic_id or leaf.subsubtopic_id
                    )
                    if changed:
                        leaf.parent = parent_menu
                        leaf.order = order
                        leaf.topic = None
                        leaf.subtopic = None
                        leaf.subsubtopic = None
                        leaf.save(update_fields=['parent', 'order', 'topic', 'subtopic', 'subsubtopic'])
                        self.stdout.write(f'  Positioned real page: {title} ({item["url_name"]})')
                    continue

                subsubtopic, created = SubSubtopic.objects.get_or_create(
                    subtopic=subtopic, title=title, defaults={'slug': item['slug']},
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
                if not created and (leaf.subsubtopic_id != subsubtopic.id or leaf.order != order):
                    leaf.subsubtopic = subsubtopic
                    leaf.order = order
                    leaf.save(update_fields=['subsubtopic', 'order'])
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f'  {verb} MenuItem: {parent_ss_title} > {title}')

        self.stdout.write(self.style.SUCCESS('Done.'))
