from django.core.management.base import BaseCommand

from apps.resources.models import Resource, SubSubtopic

# Багытталган сандар > Эсептөөлөр ("operations with directed numbers") -
# the menu ("Сандар > Багытталган сандар > Эсептөөлөр") already linked here,
# but no Resource row was ever tagged with this Topic/Subtopic/Sub-subtopic,
# so the page rendered with zero cards. The actual activity files
# (Bingo, XO, Labirinth, Tarsia Kurak, Katany Tap, Kazyna Izdoo, Katary
# MN Tort, 1234, Jenil-Orto-Oor) were uploaded and exist on disk/DB under
# "4-Amal...BagyttalganSandar..." titles, just never classified - same gap
# `audit_unlinked_resources` reports for hundreds of other files site-wide.
# This is the one canonical (non-duplicate-suffixed) title per activity;
# the many "_<randomsuffix>" rows alongside them are leftover duplicates
# from the Railway Volume incident (see docs/deployment-notes.md) and are
# deliberately left untouched/unlinked.
RESOURCE_IDS = [
    461, 174, 1561, 1243, 498, 1253, 3493, 1186, 960, 674,
    399, 690, 533, 754, 1408, 588, 743, 692, 700, 902,
]


class Command(BaseCommand):
    help = (
        "One-off data fix: links the real 'operations with directed "
        "numbers' activity files to Сандар > Багытталган сандар > "
        "Эсептөөлөр so that menu page actually shows content. Idempotent "
        "- safe to re-run."
    )

    def handle(self, *args, **options):
        subsubtopic = SubSubtopic.objects.select_related(
            "subtopic", "subtopic__topic"
        ).get(id=243)
        topic = subsubtopic.subtopic.topic
        subtopic = subsubtopic.subtopic

        resources = Resource.objects.filter(id__in=RESOURCE_IDS)
        found_ids = set(resources.values_list("id", flat=True))
        missing = set(RESOURCE_IDS) - found_ids
        if missing:
            self.stdout.write(self.style.WARNING(
                f"{len(missing)} expected resource id(s) not found, skipping: {sorted(missing)}"
            ))

        updated = resources.update(
            topic=topic, subtopic=subtopic, subsubtopic=subsubtopic, is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Linked {updated} resource(s) to {topic.title} > {subtopic.title} > {subsubtopic.title}."
        ))
