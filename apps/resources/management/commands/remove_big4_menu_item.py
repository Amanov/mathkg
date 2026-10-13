from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem

# swap_big4_for_directed_numbers_ops.py's delete only matched an exact
# (title, url_name, parent) combination - on production the leftover row
# apparently didn't match all three (order the earlier commands were run
# in, or a stray duplicate), so "Big 4 таймашы" stayed in the menu
# alongside the new "Багытталган сандар" item instead of being replaced
# by it. This is the standalone cleanup: removes any MenuItem matching by
# url_name OR title, wherever it sits in the tree. Idempotent.


class Command(BaseCommand):
    help = (
        "Removes any leftover 'Big 4 таймашы' (url_name='big4') menu "
        "item(s), regardless of where they sit in the tree. Idempotent - "
        "safe to re-run."
    )

    def handle(self, *args, **options):
        stale = MenuItem.objects.filter(url_name='big4') | MenuItem.objects.filter(title='Big 4 таймашы')
        stale_ids = list(stale.distinct().values_list('id', flat=True))

        if not stale_ids:
            self.stdout.write('Nothing to remove - no Big 4 menu item found.')
            return

        for item in MenuItem.objects.filter(id__in=stale_ids).select_related('parent'):
            parent_title = item.parent.title if item.parent else '(root)'
            self.stdout.write(f"Removing: {parent_title} > {item.title} (id={item.id})")

        # .delete() can't run on a .distinct() queryset (the OR above needs
        # it to de-dupe rows matched by both filters) - re-filter by the
        # already-resolved ids instead, a plain queryset .delete() allows.
        deleted, _ = MenuItem.objects.filter(id__in=stale_ids).delete()
        self.stdout.write(self.style.SUCCESS(f'Removed {deleted} menu item(s).'))
