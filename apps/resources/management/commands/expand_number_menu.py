from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem


class Command(BaseCommand):
    help = (
        "Adds a third nesting level under the 'Сандар' nav menu (a real "
        "sub-submenu), proving out the flyout template/CSS/JS - which "
        "already supports unlimited depth - with actual working links "
        "instead of the placeholder single-level children it had before. "
        "Idempotent: re-running it won't create duplicates."
    )

    def handle(self, *args, **options):
        sandar, created = MenuItem.objects.get_or_create(
            title='Сандар', parent=None, defaults={'order': 1}
        )
        if created:
            self.stdout.write('Created root menu item "Сандар" (it should already have existed).')

        branches = [
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

        for branch in branches:
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
