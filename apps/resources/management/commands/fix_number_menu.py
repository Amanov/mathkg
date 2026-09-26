from django.core.management.base import BaseCommand
from django.db import transaction

from apps.resources.models import MenuItem

from .import_reference_taxonomy import TAXONOMY

# The exact target order for the "Сандар" dropdown (a standard reference
# curriculum topic list, translated to Kyrgyz - see import_reference_taxonomy).
CANONICAL_ORDER = list(TAXONOMY['Сандар']['subtopics'].keys())

# Real, hand-built activity pages that predate the Topic/Subtopic system
# (see apps/resources/views/operations.py, onduktar.py) - keyed by the
# url_name their MenuItem leaf carries, mapped to the path (from Сандар's
# direct child down) of the canonical menu item they belong under. Found
# and reparented by url_name (not by whatever ad-hoc container title they
# currently sit under), so this works regardless of exactly how someone
# previously organized them. koshuu_1_digit/onedigitarithmetics nest one
# level deeper, under Decimals' own "Arithmetic: 1 Digit" sub-category,
# matching the reference site's actual depth - not as bare siblings of
# "Ондуктар" itself.
REAL_PAGES = {
    'four_basic_operations': ['Амалдардын тартиби'],
    'all_operations': ['Амалдардын тартиби'],
    'big4': ['Амалдардын тартиби'],
    'directed_numbers': ['Багытталган сандар'],
    'koshuu_1_digit': ['Ондуктар', 'Эсептөөлөр: 1 орундук сандар'],
    'onedigitarithmetics': ['Ондуктар', 'Эсептөөлөр: 1 орундук сандар'],
}

# 'directed_numbers' happened to carry the exact same title as the
# canonical subtopic it's being reparented under ("Багытталган сандар"
# under "Багытталган сандар" reads as a mistake in the dropdown) - give
# it a distinct label describing what it actually is (PPT + worksheets).
RENAMES = {
    'directed_numbers': 'Сабак материалдары',
}

# Old containers discovered directly on production, from before this
# taxonomy existed - every one of their children carries no url_name and
# no topic/subtopic/subsubtopic link, i.e. a plain "#" dead link with
# nothing behind it. Verified dead before removal, same as any other
# leftover this command cleans up - never deleted blindly.
DEAD_LEGACY_CONTAINERS = [
    ('Арифметика: 1 орундуу', ['Ондуктар']),
    ('Арифметика 1 жана 2 орундуу', ['Ондуктар']),
    ('Арифметика: бүтүн сан менен', ['Ондуктар']),
]

# Sub-subtopics that used to be part of the taxonomy but were dropped
# once the real reference list was confirmed (e.g. "Башка"/Other was a
# guess made before the full taxonomy was known) - removed only if 0
# Resources ended up attached to them in the meantime.
REMOVED_SUBSUBTOPICS = [
    ('Башка', ['Ондуктар']),
]


class Command(BaseCommand):
    help = (
        "Cleans up the live 'Сандар' nav dropdown to match the canonical "
        "reference taxonomy exactly. Run import_reference_taxonomy first "
        "(it creates the canonical subtopics/sub-subtopics if they don't "
        "exist yet - this command only reorders/reparents/removes, it "
        "doesn't create the canonical items itself). Concretely: "
        "(1) forces the canonical subtopics into the reference order; "
        "(2) reparents the real hand-built activity pages under their "
        "correct canonical subtopic (or sub-subtopic) by url_name, "
        "wherever they currently sit, and clears any topic/subtopic/"
        "subsubtopic link on them that would otherwise silently shadow "
        "their url_name and route visitors to a different generic page; "
        "(3) removes specific legacy containers found on production whose "
        "every child is a verified dead link; (4) removes sub-subtopics "
        "dropped from the taxonomy that still have 0 resources attached; "
        "(5) removes leftover ad-hoc top-level items under Сандар once "
        "step 2 has emptied them of children. Anything that still holds "
        "unrecognized real content after these steps is left alone and "
        "reported, never deleted blindly. Use --dry-run to preview with "
        "no changes saved. Safe to re-run."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Print what would change without saving anything.",
        )

    def handle(self, *args, **options):
        dry = options['dry_run']

        try:
            sandar = MenuItem.objects.get(title='Сандар', parent__isnull=True)
        except MenuItem.DoesNotExist:
            self.stderr.write('No root "Сандар" menu item found - nothing to do.')
            return

        canonical_items = {}
        for title in CANONICAL_ORDER:
            try:
                canonical_items[title] = MenuItem.objects.get(title=title, parent=sandar)
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'Canonical subtopic "{title}" has no MenuItem under Сандар yet - '
                    f'run "python manage.py import_reference_taxonomy" first.'
                )
                return
            except MenuItem.MultipleObjectsReturned:
                self.stderr.write(
                    f'Multiple MenuItems titled "{title}" directly under Сандар - '
                    f'resolve the duplicate manually first.'
                )
                return

        with transaction.atomic():

            self.stdout.write('--- Reordering canonical subtopics ---')
            for order, title in enumerate(CANONICAL_ORDER, start=1):
                item = canonical_items[title]
                if item.order != order:
                    self.stdout.write(f'  {title}: order {item.order} -> {order}')
                    if not dry:
                        item.order = order
                        item.save(update_fields=['order'])

            self.stdout.write('--- Reparenting real activity pages ---')
            for url_name, path in REAL_PAGES.items():
                try:
                    leaf = MenuItem.objects.get(url_name=url_name)
                except MenuItem.DoesNotExist:
                    self.stdout.write(f'  No menu item links to {url_name} - skipping.')
                    continue
                except MenuItem.MultipleObjectsReturned:
                    self.stderr.write(
                        f'  Multiple menu items link to {url_name} - resolve manually first.'
                    )
                    continue

                target_parent = canonical_items[path[0]]
                try:
                    for title in path[1:]:
                        target_parent = target_parent.children.get(title=title)
                except MenuItem.DoesNotExist:
                    self.stderr.write(
                        f'  Can\'t find "{" > ".join(path)}" for {url_name} - '
                        f'run import_reference_taxonomy first, then retry.'
                    )
                    continue

                new_title = RENAMES.get(url_name, leaf.title)
                moved = leaf.parent_id != target_parent.id
                renamed = new_title != leaf.title
                # A leaf like this must resolve via url_name alone - if it also
                # carries a topic/subtopic/subsubtopic link (e.g. from a since-
                # removed feature), that link wins over url_name and silently
                # routes visitors to a different, generic page instead of this
                # real one. Always clear it.
                shadowed = leaf.subsubtopic_id or leaf.subtopic_id or leaf.topic_id
                if moved or renamed or shadowed:
                    action = []
                    if moved:
                        action.append(f'moved under "{" > ".join(path)}"')
                    if renamed:
                        action.append(f'renamed to "{new_title}"')
                    if shadowed:
                        action.append('cleared a topic/subtopic link that was shadowing it')
                    self.stdout.write(f'  "{leaf.title}" ({url_name}): {", ".join(action)}')
                    if not dry:
                        leaf.parent = target_parent
                        leaf.title = new_title
                        leaf.topic = None
                        leaf.subtopic = None
                        leaf.subsubtopic = None
                        leaf.save(update_fields=['parent', 'title', 'topic', 'subtopic', 'subsubtopic'])

            self.stdout.write('--- Removing known-dead legacy containers ---')
            for title, path in DEAD_LEGACY_CONTAINERS:
                parent = canonical_items.get(path[0])
                for step in path[1:]:
                    parent = parent.children.filter(title=step).first() if parent else None
                node = parent.children.filter(title=title).first() if parent else None
                if not node:
                    continue
                children = list(node.children.all())
                alive = [
                    c for c in children
                    if c.url_name or c.topic_id or c.subtopic_id or c.subsubtopic_id or c.children.exists()
                ]
                if alive:
                    self.stdout.write(
                        f'  NOT removing "{title}" - has real content in '
                        f'{[c.title for c in alive]}, check manually.'
                    )
                    continue
                self.stdout.write(f'  Removing "{title}" and its {len(children)} dead link(s)')
                if not dry:
                    node.delete()

            self.stdout.write('--- Removing sub-subtopics dropped from the taxonomy ---')
            for title, path in REMOVED_SUBSUBTOPICS:
                parent = canonical_items.get(path[0])
                for step in path[1:]:
                    parent = parent.children.filter(title=step).first() if parent else None
                node = parent.children.filter(title=title).first() if parent else None
                if not node:
                    continue
                resource_count = node.subsubtopic.resources.count() if node.subsubtopic else 0
                if resource_count:
                    self.stdout.write(
                        f'  NOT removing "{title}" - {resource_count} resource(s) attached, '
                        f'check manually.'
                    )
                    continue
                self.stdout.write(f'  Removing "{title}" (0 resources attached)')
                if not dry:
                    node.delete()

            self.stdout.write('--- Removing emptied leftover items ---')
            stale = MenuItem.objects.filter(parent=sandar).exclude(title__in=CANONICAL_ORDER)
            for item in stale:
                children_left = list(item.children.values_list('title', flat=True))
                if children_left:
                    self.stdout.write(
                        f'  NOT removing "{item.title}" - still has children {children_left}, '
                        f'check manually.'
                    )
                    continue
                self.stdout.write(f'  Removing "{item.title}" (now empty)')
                if not dry:
                    item.delete()

            if dry:
                transaction.set_rollback(True)

        self.stdout.write(self.style.SUCCESS(
            'Dry run complete - nothing saved.' if dry else 'Done.'
        ))
