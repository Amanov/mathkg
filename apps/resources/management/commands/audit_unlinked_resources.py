import os
import re

from django.core.management.base import BaseCommand

from apps.resources.models import Resource

# Non-content files that sometimes end up as Resource rows by mistake
# (editor/OS artifacts, blank starter templates, raw screenshots) - flagged
# separately so they don't clutter the real grouping below.
JUNK_PATTERNS = (
    re.compile(r"^\.DS_Store$", re.I),
    re.compile(r"^0?Template$", re.I),
    re.compile(r"Screenshot$", re.I),
)


def _group_key(title):
    """Buckets a title by its leading 1-2 topic tokens, ignoring the
    trailing activity-type/size-variant noise (KatanyTap, TarsiaKurak,
    A4/A5/A6, a random upload suffix, " copy", ...). Not a perfect
    classifier - it's a triage aid, so titles are also kept per-group for
    a human to sanity-check."""
    stem = os.path.splitext(title)[0]
    stem = re.sub(r"\s*-\s*", "_", stem)
    stem = re.sub(r"\s+", "_", stem)
    stem = re.sub(r"_copy$", "", stem, flags=re.I)
    stem = re.sub(r"_[A-Za-z0-9]{6,8}$", "", stem)  # random upload suffix
    stem = re.sub(r"_?A[4-7]$", "", stem)  # print-size variant
    tokens = [t for t in stem.split("_") if t]
    if not tokens:
        return stem or title
    return "_".join(tokens[:2])


class Command(BaseCommand):
    help = (
        "Read-only report on Resource rows not yet linked to a Topic/"
        "Subtopic/Sub-subtopic - files already uploaded and sitting on the "
        "server with real content, just not yet classified. Default output "
        "groups the ~hundreds of titles by inferred topic prefix so the "
        "shape of what's there is visible at a glance; pass --full for the "
        "old flat list instead. Makes no changes - safe to run anytime, "
        "including on production."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--full", action="store_true",
            help="Print the flat, ungrouped title list instead of grouping by inferred topic.",
        )
        parser.add_argument(
            "--examples", type=int, default=3,
            help="How many example titles to print per group (default 3).",
        )

    def handle(self, *args, **options):
        total = Resource.objects.count()
        linked = Resource.objects.filter(subtopic__isnull=False).count()
        unlinked = list(Resource.objects.filter(subtopic__isnull=True).order_by("title"))

        self.stdout.write(f"Total Resource rows: {total}")
        self.stdout.write(f"Linked to a Subtopic (visible on a page): {linked}")
        self.stdout.write(f"Not linked to anything yet: {len(unlinked)}")

        if not unlinked:
            return

        self.stdout.write("")

        if options["full"]:
            self.stdout.write("Unlinked titles (file already uploaded, just needs Topic/Subtopic/Sub-subtopic set):")
            for r in unlinked:
                has_image = "image" if r.image else "no-image"
                self.stdout.write(f"  [{r.id}] {r.title} ({r.category or 'no-category'}, {has_image})")
            return

        junk = [r for r in unlinked if any(p.search(os.path.splitext(r.title)[0]) for p in JUNK_PATTERNS)]
        real = [r for r in unlinked if r not in junk]

        groups = {}
        for r in real:
            groups.setdefault(_group_key(r.title), []).append(r)

        self.stdout.write(f"Grouped into {len(groups)} inferred topic buckets (pass --full for the flat list):")
        self.stdout.write("")
        n = options["examples"]
        for key, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            self.stdout.write(f"[{len(items)}] {key}")
            for r in items[:n]:
                self.stdout.write(f"    {r.title}")
            if len(items) > n:
                self.stdout.write(f"    ... and {len(items) - n} more")

        if junk:
            self.stdout.write("")
            self.stdout.write(f"Likely junk / not real content ({len(junk)}):")
            for r in junk:
                self.stdout.write(f"  [{r.id}] {r.title}")
