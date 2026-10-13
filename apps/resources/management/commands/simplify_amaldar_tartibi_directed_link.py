from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# Reverses swap_big4_for_directed_numbers_ops.py's "Эсептөөлөр" branch (7
# placeholder children with nothing behind them yet) per explicit request:
# Сандар > Амалдардын тартиби should instead have a plain 3rd item titled
# "Багытталган сандар" - a flat cross-link straight to the real, already-
# populated Сандар > Багытталган сандар > Эсептөөлөр page (the same one
# link_directed_numbers_arithmetic filled with real activities), not a new
# placeholder subtree. Сандар > Багытталган сандар > Эсептөөлөр itself is
# untouched - this only changes what sits under Амалдардын тартиби.
PARENT_TITLE = 'Амалдардын тартиби'
OLD_BRANCH_TITLE = 'Эсептөөлөр'
NEW_LEAF_TITLE = 'Багытталган сандар'

# Final order under Амалдардын тартиби: Төрт амал, Багытталган сандар,
# Аралаш амалдар.
FINAL_ORDER = ['Төрт амал', NEW_LEAF_TITLE, 'Аралаш амалдар']


class Command(BaseCommand):
    help = (
        "Replaces the 'Эсептөөлөр' placeholder branch under Сандар > "
        "Амалдардын тартиби with a single flat leaf 'Багытталган сандар' "
        "linking to the real, already-populated Эсептөөлөр page under "
        "Сандар > Багытталган сандар. Idempotent - safe to re-run."
    )

    def handle(self, *args, **options):
        parent = MenuItem.objects.get(
            title=PARENT_TITLE, parent__title='Сандар', parent__parent__isnull=True,
        )

        deleted, _ = MenuItem.objects.filter(title=OLD_BRANCH_TITLE, parent=parent).delete()
        if deleted:
            self.stdout.write(f"Removed: {PARENT_TITLE} > {OLD_BRANCH_TITLE} (and its placeholder children)")
        else:
            self.stdout.write(f"Not found (already removed?): {PARENT_TITLE} > {OLD_BRANCH_TITLE}")

        subsubtopic = SubSubtopic.objects.select_related('subtopic', 'subtopic__topic').get(
            title='Эсептөөлөр', subtopic__title='Багытталган сандар', subtopic__topic__title='Сандар',
        )

        leaf, created = MenuItem.objects.get_or_create(
            parent=parent,
            topic=subsubtopic.subtopic.topic,
            subtopic=subsubtopic.subtopic,
            subsubtopic=subsubtopic,
            defaults={'title': NEW_LEAF_TITLE, 'order': 2},
        )
        if not created and leaf.title != NEW_LEAF_TITLE:
            leaf.title = NEW_LEAF_TITLE
            leaf.save(update_fields=['title'])
        verb = 'Created' if created else 'Already exists'
        self.stdout.write(f"{verb}: {PARENT_TITLE} > {leaf.title} -> {leaf.get_resolved_url()}")

        for order, title in enumerate(FINAL_ORDER, start=1):
            updated = MenuItem.objects.filter(parent=parent, title=title).update(order=order)
            if updated:
                self.stdout.write(f"  Order {order}: {title}")

        self.stdout.write(self.style.SUCCESS('Done.'))
