from django.core.management.base import BaseCommand
from django.db import transaction

from apps.resources.models import MenuItem

from .import_reference_taxonomy import TAXONOMY

# The exact target order for the "Сандар" dropdown (a standard reference
# curriculum topic list, translated to Kyrgyz - see import_reference_taxonomy).
CANONICAL_ORDER = list(TAXONOMY['Сандар']['subtopics'].keys())

# Real, hand-built activity pages that predate the Topic/Subtopic system
# (see apps/resources/views/operations.py, onduktar.py) - keyed by the
# url_name their MenuItem leaf carries, mapped to the canonical subtopic
# they belong under. Found and reparented by url_name (not by whatever
# ad-hoc container title they currently sit under), so this works
# regardless of exactly how someone previously organized them.
REAL_PAGES = {
    'four_basic_operations': 'Амалдардын тартиби',
    'all_operations': 'Амалдардын тартиби',
    'big4': 'Амалдардын тартиби',
    'directed_numbers': 'Багытталган сандар',
    'koshuu_1_digit': 'Ондуктар',
    'onedigitarithmetics': 'Ондуктар',
}

# 'directed_numbers' happened to carry the exact same title as the
# canonical subtopic it's being reparented under ("Багытталган сандар"
# under "Багытталган сандар" reads as a mistake in the dropdown) - give
# it a distinct label describing what it actually is (PPT + worksheets).
RENAMES = {
    'directed_numbers': 'Сабак материалдары',
}


class Command(BaseCommand):
    help = (
        "Cleans up the live 'Сандар' nav dropdown to match the canonical "
        "reference taxonomy exactly. Run import_reference_taxonomy first "
        "(it creates the 14 canonical subtopics if they don't exist yet - "
        "this command only reorders/reparents/removes, it doesn't create "
        "the canonical items itself). Concretely: (1) forces the 14 "
        "canonical subtopics into the reference order; (2) reparents the "
        "real hand-built activity pages under their correct canonical "
        "subtopic by url_name, wherever they currently sit; (3) removes "
        "leftover ad-hoc top-level items under Сандар (duplicates, old "
        "containers like 'Бүтүн сандар менен амалдар') once reparenting "
        "step 2 has emptied them of children - anything that still has "
        "children afterwards is left alone and reported, not deleted. "
        "Use --dry-run to preview with no changes saved. Safe to re-run."
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
            for url_name, canonical_title in REAL_PAGES.items():
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
                target_parent = canonical_items[canonical_title]
                new_title = RENAMES.get(url_name, leaf.title)
                moved = leaf.parent_id != target_parent.id
                renamed = new_title != leaf.title
                if moved or renamed:
                    action = []
                    if moved:
                        action.append(f'moved under "{canonical_title}"')
                    if renamed:
                        action.append(f'renamed to "{new_title}"')
                    self.stdout.write(f'  "{leaf.title}" ({url_name}): {", ".join(action)}')
                    if not dry:
                        leaf.parent = target_parent
                        leaf.title = new_title
                        leaf.save(update_fields=['parent', 'title'])

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
