from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# Сандар > Амалдардын тартиби > Big 4 таймашы (url_name='big4') pointed at
# a timer-game page with no real content behind it. Per explicit request,
# swapped for Эсептөөлөр ("operations with directed numbers") - matching
# the reference design, which breaks that same category down further into
# per-operation children. Our content isn't split that way yet (the 20
# activities link_directed_numbers_arithmetic linked are generic, not
# tagged by which operation they drill), so these 7 are placeholder
# leaves (no page behind them yet) rather than guessed-at links to the
# one existing page under 7 different labels.
OLD_TITLE = 'Big 4 таймашы'
OLD_URL_NAME = 'big4'
PARENT_TITLE = 'Амалдардын тартиби'
NEW_TITLE = 'Эсептөөлөр'
NEW_ORDER = 21

CHILDREN = [
    'Кошуу',
    'Кемитүү',
    'Кошуу жана кемитүү',
    'Көбөйтүү жана бөлүү',
    'Аралаш амалдар',
    'Амалдардын тартиби менен',
    'Татаал',
]


class Command(BaseCommand):
    help = (
        "One-off menu fix: removes the 'Big 4 таймашы' leaf under "
        "Сандар > Амалдардын тартиби and replaces it with an 'Эсептөөлөр' "
        "branch carrying 7 placeholder children (Кошуу, Кемитүү, ...), "
        "matching the reference design's Arithmetic breakdown. Idempotent "
        "- safe to re-run."
    )

    def handle(self, *args, **options):
        parent = MenuItem.objects.get(title=PARENT_TITLE, parent__title='Сандар', parent__parent__isnull=True)

        deleted, _ = MenuItem.objects.filter(title=OLD_TITLE, url_name=OLD_URL_NAME, parent=parent).delete()
        if deleted:
            self.stdout.write(f"Removed: {PARENT_TITLE} > {OLD_TITLE}")
        else:
            self.stdout.write(f"Not found (already removed?): {PARENT_TITLE} > {OLD_TITLE}")

        subsubtopic = SubSubtopic.objects.select_related('subtopic', 'subtopic__topic').get(
            title='Эсептөөлөр', subtopic__title='Багытталган сандар', subtopic__topic__title='Сандар',
        )

        branch, created = MenuItem.objects.get_or_create(
            parent=parent,
            topic=subsubtopic.subtopic.topic,
            subtopic=subsubtopic.subtopic,
            subsubtopic=subsubtopic,
            defaults={'title': NEW_TITLE, 'order': NEW_ORDER},
        )
        if not created and branch.title != NEW_TITLE:
            branch.title = NEW_TITLE
            branch.save(update_fields=['title'])
        verb = 'Created' if created else 'Already exists'
        self.stdout.write(f"{verb}: {PARENT_TITLE} > {branch.title}")

        for order, title in enumerate(CHILDREN, start=1):
            leaf, created = MenuItem.objects.get_or_create(
                title=title, parent=branch, defaults={'order': order},
            )
            verb = 'Created' if created else 'Already exists'
            self.stdout.write(f"  {verb}: {branch.title} > {leaf.title}")

        self.stdout.write(self.style.SUCCESS('Done.'))
