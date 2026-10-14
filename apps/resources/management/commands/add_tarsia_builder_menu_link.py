from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem


class Command(BaseCommand):
    help = (
        "Idempotent: adds (or repoints) a 'Тарсия куруучу' MenuItem under the "
        "top-level 'Сандар' menu, pointing at the new interactive Tarsia "
        "builder tool (url_name='tarsia_builder'). Safe to re-run."
    )

    def handle(self, *args, **options):
        sandar = MenuItem.objects.filter(title='Сандар', parent__isnull=True).first()
        if not sandar:
            self.stdout.write(self.style.ERROR("No top-level 'Сандар' MenuItem found - nothing to attach to."))
            return

        item, created = MenuItem.objects.get_or_create(
            title='Тарсия куруучу',
            parent=sandar,
            defaults={'url_name': 'tarsia_builder'},
        )
        if not created:
            item.topic = None
            item.subtopic = None
            item.subsubtopic = None
            item.url_name = 'tarsia_builder'
            item.save()

        self.stdout.write(self.style.SUCCESS(
            f"{'Created' if created else 'Updated'} MenuItem {item.id} 'Тарсия куруучу' -> tarsia_builder"
        ))
