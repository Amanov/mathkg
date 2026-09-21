from django.core.management.base import BaseCommand

from apps.resources.models import Resource


class Command(BaseCommand):
    help = (
        "Read-only report: how many Resource rows exist in total, how many "
        "are already linked to a Topic/Subtopic/Sub-subtopic (and therefore "
        "visible on a real page), and the full title list of the ones that "
        "aren't linked to anything yet - files already uploaded and sitting "
        "on the server with real content, just not yet classified. Makes no "
        "changes; safe to run anytime, including on production."
    )

    def handle(self, *args, **options):
        total = Resource.objects.count()
        linked = Resource.objects.filter(subtopic__isnull=False).count()
        unlinked = Resource.objects.filter(subtopic__isnull=True).order_by("title")

        self.stdout.write(f"Total Resource rows: {total}")
        self.stdout.write(f"Linked to a Subtopic (visible on a page): {linked}")
        self.stdout.write(f"Not linked to anything yet: {unlinked.count()}")

        if unlinked.exists():
            self.stdout.write("")
            self.stdout.write("Unlinked titles (file already uploaded, just needs Topic/Subtopic/Sub-subtopic set):")
            for r in unlinked:
                has_image = "image" if r.image else "no-image"
                self.stdout.write(f"  [{r.id}] {r.title} ({r.category or 'no-category'}, {has_image})")
