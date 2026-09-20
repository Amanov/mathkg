from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem

# Shared by both directions so "what --undo removes" can never drift from
# "what running the command without it added".
BRANCHES = [
    {
        'title': 'Бүтүн сандар менен амалдар',
        'order': 3,
        'children': [
            ('Багытталган сандар', 'directed_numbers'),
            ('Төрт амал', 'four_basic_operations'),
            ('Аралаш амалдар', 'all_operations'),
            ('Big 4 таймашы', 'big4'),
        ],
    },
    {
        'title': 'Ондуктар менен эсептөө',
        'order': 4,
        'children': [
            ('Кошуу (1 орундук сандар)', 'koshuu_1_digit'),
            ('1 орундук сандар менен көнүгүүлөр', 'onedigitarithmetics'),
        ],
    },
]


class Command(BaseCommand):
    help = (
        "Adds a third nesting level under the 'Сандар' nav menu (a real "
        "sub-submenu), proving out the flyout template/CSS/JS - which "
        "already supports unlimited depth - with actual working links "
        "instead of the placeholder single-level children it had before. "
        "Idempotent: re-running it won't create duplicates. Pass --undo "
        "to remove exactly what this command adds, leaving 'Сандар' "
        "itself and everything else in the menu untouched."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--undo', action='store_true',
            help="Remove the branches this command adds, instead of adding them.",
        )

    def handle(self, *args, **options):
        if options['undo']:
            self.undo()
        else:
            self.apply()

    def apply(self):
        sandar, created = MenuItem.objects.get_or_create(
            title='Сандар', parent=None, defaults={'order': 1}
        )
        if created:
            self.stdout.write('Created root menu item "Сандар" (it should already have existed).')

        for branch in BRANCHES:
            subtopic, created = MenuItem.objects.get_or_create(
                title=branch['title'], parent=sandar,
                defaults={'order': branch['order']},
            )
            verb = 'Created' if created else 'Already exists'
            self.stdout.write(f"{verb}: Сандар > {subtopic.title}")

            for order, (title, url_name) in enumerate(branch['children'], start=1):
                leaf, created = MenuItem.objects.get_or_create(
                    title=title, parent=subtopic,
                    defaults={'order': order, 'url_name': url_name},
                )
                if not created and leaf.url_name != url_name:
                    leaf.url_name = url_name
                    leaf.save(update_fields=['url_name'])
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f"  {verb}: {subtopic.title} > {leaf.title} -> {url_name}")

        self.stdout.write(self.style.SUCCESS('Done.'))

    def undo(self):
        # Deleting each subtopic branch cascades to its children
        # (MenuItem.parent is on_delete=CASCADE) - "Сандар" itself and
        # everything else in the menu (Пропорция, Алгебра, Геометрия,
        # Дата, Ыктымалдуулук, the existing Кошуу/Кемитүү) is never
        # touched, since only these two exact titles are looked up.
        removed_any = False
        for branch in BRANCHES:
            deleted, _ = MenuItem.objects.filter(
                title=branch['title'], parent__title='Сандар', parent__parent__isnull=True,
            ).delete()
            if deleted:
                removed_any = True
                self.stdout.write(f"Removed: Сандар > {branch['title']} (and its children)")
            else:
                self.stdout.write(f"Not found (already removed?): Сандар > {branch['title']}")

        if removed_any:
            self.stdout.write(self.style.SUCCESS('Undo complete.'))
        else:
            self.stdout.write('Nothing to undo.')
