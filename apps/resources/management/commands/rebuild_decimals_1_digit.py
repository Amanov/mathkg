from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic

# Each entry rebuilds one sub-subtopic's children as a reference-ordered
# list of real pages (see apps/resources/views/onduktar_placeholders.py +
# templates/resources/onduktar/operation_placeholder.html - all share
# koshuu_1_digit's visual design and its short-URL convention instead of
# the long generic /resources/topic/number/... path). Add a new dict here
# for the next sub-subtopic that needs the same treatment; this command
# processes every group in one run.
GROUPS = [
    {
        # Slot 1 (Adding) is the one real hand-built page (koshuu_1_digit)
        # and is left untouched; slots 2-8 are real pages too now.
        'parent_path': ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 орундук сандар'),
        'target_items': [
            {'title': 'Кошуу (1 орундук сандар)', 'url_name': 'koshuu_1_digit'},
            {'title': 'Кемитүү — 1 орундуу сандар', 'url_name': 'subtracting_1_digit'},
            {'title': 'Кошуу жана кемитүү — 1 орундуу сандар', 'url_name': 'adding_subtracting_1_digit'},
            {'title': 'Көбөйтүү — 1 орундуу сандар', 'url_name': 'multiplying_1_digit'},
            {'title': 'Бөлүү — 1 орундуу сандар', 'url_name': 'dividing_1_digit'},
            {'title': 'Көбөйтүү жана бөлүү — 1 орундуу сандар', 'url_name': 'multiplying_dividing_1_digit'},
            {'title': 'Аралаш эсептөөлөр — 1 орундуу сандар', 'url_name': 'mixed_1_digit'},
            {'title': '1ден кичине ондукка бөлүү', 'url_name': 'dividing_by_less_than_1'},
        ],
        # Old titles earlier versions of this command (and its
        # predecessor, add_leaf_items.py) created as generic
        # Topic/Subtopic SubSubtopic placeholders, now superseded by the
        # real pages above - removed if they hold 0 resources.
        'stale_subsubtopic_titles': [
            '1 орундук ондуктарды кошуу',
            '1 орундук ондуктар менен эсептөөлөр',
            '1 орундук ондуктарды кемитүү',
            '1 орундук ондуктарды кошуу жана кемитүү',
            '1 орундук ондуктарды көбөйтүү',
            '1 орундук ондуктарды бөлүү',
            '1 орундук ондуктарды көбөйтүү жана бөлүү',
            '1ден кичине ондукка бөлүү',
        ],
        # Doesn't correspond to any of the 8 target slots (slot 7 is
        # "Mixed", not "Arithmetic With"/general exercises) - removed
        # from the menu entirely per explicit instruction ("it will make
        # my menu messy"). The real page itself (view, template, URL, any
        # uploaded resources) is untouched - only its navigation entry is
        # deleted.
        'displaced_url_names': ['onedigitarithmetics'],
    },
    {
        # None of these 8 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Ондуктар', 'Эсептөөлөр: 1 жана 2 орундук сандар'),
        'target_items': [
            {'title': 'Кошуу — 1 жана 2 орундук сандар', 'url_name': 'adding_1_2_digit'},
            {'title': 'Кемитүү — 1 жана 2 орундук сандар', 'url_name': 'subtracting_1_2_digit'},
            {'title': 'Кошуу жана кемитүү — 1 жана 2 орундук сандар', 'url_name': 'adding_subtracting_1_2_digit'},
            {'title': 'Көбөйтүү — 1 жана 2 орундук сандар', 'url_name': 'multiplying_1_2_digit'},
            {'title': 'Бөлүү — 1 жана 2 орундук сандар', 'url_name': 'dividing_1_2_digit'},
            {'title': 'Көбөйтүү жана бөлүү — 1 жана 2 орундук сандар', 'url_name': 'multiplying_dividing_1_2_digit'},
            {'title': '10, 100, 1000гө көбөйтүү жана бөлүү', 'url_name': 'multiplying_dividing_10_100_1000'},
            {'title': 'Аралаш эсептөөлөр — 1 жана 2 орундук сандар', 'url_name': 'mixed_1_2_digit'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 8 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Ондуктар', 'Эсептөөлөр: бүтүн сандар менен'),
        'target_items': [
            {'title': 'Кошуу — бүтүн сандар менен', 'url_name': 'adding_with_integers'},
            {'title': 'Кемитүү — бүтүн сандар менен', 'url_name': 'subtracting_with_integers'},
            {'title': 'Кошуу жана кемитүү — бүтүн сандар менен', 'url_name': 'adding_subtracting_with_integers'},
            {'title': 'Көбөйтүү — бүтүн сандар менен', 'url_name': 'multiplying_with_integers'},
            {'title': 'Бөлүү — бүтүн сандар менен', 'url_name': 'dividing_with_integers'},
            {'title': 'Көбөйтүү жана бөлүү — бүтүн сандар менен', 'url_name': 'multiplying_dividing_with_integers'},
            {'title': 'Аралаш эсептөөлөр — бүтүн сандар менен', 'url_name': 'mixed_with_integers'},
            {'title': 'Бөлүүчүсү 1ден кичине бөлүү — бүтүн сандар менен', 'url_name': 'dividing_divisor_less_than_1_with_integers'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # Unlike the previous 3 groups, all 9 of these are real, hand-built
        # pages (see apps/resources/views/ekvivalenttuuluk.py) - rewired
        # from a dead download_file URL scheme onto the current
        # download_resource system, not fresh placeholders.
        'parent_path': ('Сандар', 'Ондуктар', 'Эквиваленттүүлүк'),
        'target_items': [
            {'title': 'Ондуктарды бөлчөккө айландыруу', 'url_name': 'to_fractions'},
            {'title': 'Ондуктарды пайыздарга айландыруу', 'url_name': 'to_percentages'},
            {'title': 'Ондуктарды бөлчөккө жана пайызга айландыруу', 'url_name': 'to_both'},
            {'title': 'Кайталануучу ондуктарды бөлчөккө айландыруу', 'url_name': 'recurring_decimals_to_fractions'},
            {'title': 'Бөлчөктөрдү жана ондуктарды ортосунда айландыруу', 'url_name': 'with_fractions'},
            {'title': 'Бөлчөктөрдүн жана пайыздардын ортосунда айландыруу', 'url_name': 'with_percentages'},
            {'title': 'Бөлчөк, ондук жана пайыздык эквиваленттүүлүк', 'url_name': 'fdp'},
            {'title': 'Бөлчөктөрдү, ондуктарды жана пайыздарды иреттөө', 'url_name': 'fdp_ordering'},
            {'title': 'Бөлчөк, ондук, пайыздык жана катыштын эквиваленттүүлүгү', 'url_name': 'fdpr'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 5 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Ондуктар', 'Акча'),
        'target_items': [
            {'title': 'Сатып алуу: калькулятор менен', 'url_name': 'purchasing_calculator'},
            {'title': 'Сатып алуу: калькуляторсуз', 'url_name': 'purchasing_non_calculator'},
            {'title': 'Насыяга сатып алуу', 'url_name': 'hire_purchase'},
            {'title': 'Эсептер жана көчүрмөлөр', 'url_name': 'bills_and_statements'},
            {'title': 'Эмгек акы ставкалары', 'url_name': 'rates_of_pay'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # Neither of these 2 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Ондуктар', 'Мезгилдүү ондуктар'),
        'target_items': [
            {'title': 'Мезгилдүү ондуктарды иреттөө', 'url_name': 'recurring_decimals_ordering'},
            {'title': 'Мезгилдүү ондуктарды бөлчөккө айландыруу', 'url_name': 'recurring_converting_to_fractions'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 7 have a real hand-built page yet. "Сабак
        # материалдары" (directed_numbers_view - a real, general combined
        # page, not specific to any one of these 7 slots) sat as a sibling
        # of this parent under Багытталган сандар - doesn't correspond to
        # any of the 7 target slots, so its menu entry is removed the same
        # way onedigitarithmetics's was in the first group above; the page
        # itself is untouched.
        'parent_path': ('Сандар', 'Багытталган сандар', 'Эсептөөлөр'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'adding_directed'},
            {'title': 'Кемитүү', 'url_name': 'subtracting_directed'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'adding_subtracting_directed'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'multiplying_dividing_directed'},
            {'title': 'Аралаш эсептөөлөр', 'url_name': 'mixed_directed'},
            {'title': 'BIDMAS менен', 'url_name': 'with_bidmas_directed'},
            {'title': 'Татаал эсептөөлөр', 'url_name': 'complex_directed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': ['directed_numbers'],
    },
    {
        # None of these 10 have a real hand-built page yet. Note this
        # "Эквиваленттүүлүк" is the top-level Number topic (Topic ->
        # Subtopic "Эквиваленттүүлүк" -> SubSubtopic "Бөлчөктөрдү
        # айландыруу"/Converting Fractions), not the Ондуктар >
        # Эквиваленттүүлүк sub-subtopic rebuilt earlier - the parent_path
        # lookup below disambiguates by requiring the grandparent to be
        # Сандар directly (there are 4 different "Эквиваленттүүлүк" menu
        # items in the tree, each under a different parent).
        'parent_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөктөрдү айландыруу'),
        'target_items': [
            {'title': 'Ондукка айландыруу', 'url_name': 'fractions_to_decimals'},
            {'title': 'Ондукка айландыруу: калькулятор менен', 'url_name': 'fractions_to_decimals_calculator'},
            {'title': 'Пайызга айландыруу', 'url_name': 'fractions_to_percentages'},
            {'title': 'Пайызга айландыруу: калькулятор менен', 'url_name': 'fractions_to_percentages_calculator'},
            {'title': 'Катышка айландыруу', 'url_name': 'fractions_to_ratios'},
            {'title': 'Баарына айландыруу', 'url_name': 'fractions_to_all'},
            {'title': 'Ондуктар менен', 'url_name': 'fractions_with_decimals'},
            {'title': 'Пайыздар менен', 'url_name': 'fractions_with_percentages'},
            {'title': 'Катыштар менен', 'url_name': 'fractions_with_ratios'},
            {'title': 'Баары менен', 'url_name': 'fractions_with_all'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 7 have a real hand-built page yet. Content-wise
        # this overlaps a lot with Ондуктар > Эквиваленттүүлүк (built
        # earlier - to_fractions, to_percentages, etc.), but that's a
        # different SubSubtopic with its own url_names already positioned
        # in its own list; reusing those url_names here would make this
        # command fight over repositioning them out of that list, so this
        # gets its own distinct pages instead (same reasoning as
        # recurring_converting_to_fractions under Мезгилдүү ондуктар).
        # No FDP/FDP Ordering/FPR/FDPR items here - those are already
        # covered by this SubSubtopic's own siblings at the level above.
        'parent_path': ('Сандар', 'Эквиваленттүүлүк', 'Ондуктарды айландыруу'),
        'target_items': [
            {'title': 'Бөлчөккө айландыруу', 'url_name': 'decimals_to_fractions'},
            {'title': 'Пайызга айландыруу', 'url_name': 'decimals_to_percentages'},
            {'title': 'Бөлчөккө жана пайызга айландыруу', 'url_name': 'decimals_to_both'},
            {'title': 'Кайталануучу ондуктарды бөлчөккө айландыруу', 'url_name': 'decimals_recurring_to_fractions'},
            {'title': 'Бөлчөктөр менен', 'url_name': 'decimals_with_fractions'},
            {'title': 'Пайыздар менен', 'url_name': 'decimals_with_percentages'},
            {'title': 'Экөө менен тең', 'url_name': 'decimals_with_both'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 8 have a real hand-built page yet. Same
        # own-distinct-pages reasoning as Converting Decimals above - no
        # FDP-family items here either, for the same reason.
        'parent_path': ('Сандар', 'Эквиваленттүүлүк', 'Пайыздарды айландыруу'),
        'target_items': [
            {'title': 'Бөлчөккө айландыруу', 'url_name': 'percentages_to_fractions'},
            {'title': 'Ондукка айландыруу', 'url_name': 'percentages_to_decimals'},
            {'title': 'Катышка айландыруу', 'url_name': 'percentages_to_ratios'},
            {'title': 'Баарына айландыруу', 'url_name': 'percentages_to_all'},
            {'title': 'Бөлчөктөр менен', 'url_name': 'percentages_with_fractions'},
            {'title': 'Ондуктар менен', 'url_name': 'percentages_with_decimals'},
            {'title': 'Катыштар менен', 'url_name': 'percentages_with_ratios'},
            {'title': 'Баары менен', 'url_name': 'percentages_with_all'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 6 have a real hand-built page yet. Same
        # own-distinct-pages reasoning as the other Converting-X siblings.
        # No "To/With Decimals" or "To All" here, unlike the Fractions/
        # Percentages siblings - matches the reference's own narrower list
        # for Ratios.
        'parent_path': ('Сандар', 'Эквиваленттүүлүк', 'Катыштарды айландыруу'),
        'target_items': [
            {'title': 'Бөлчөккө айландыруу', 'url_name': 'ratios_to_fractions'},
            {'title': 'Пайызга айландыруу', 'url_name': 'ratios_to_percentages'},
            {'title': 'Бөлчөккө жана пайызга айландыруу', 'url_name': 'ratios_to_both'},
            {'title': 'Бөлчөктөр менен', 'url_name': 'ratios_with_fractions'},
            {'title': 'Пайыздар менен', 'url_name': 'ratios_with_percentages'},
            {'title': 'Экөө менен тең', 'url_name': 'ratios_with_both'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 4 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Болжолдоо жана тегеректөө', 'Тегеректөө'),
        'target_items': [
            {'title': 'Ондук орундар', 'url_name': 'rounding_decimal_places'},
            {'title': 'Маанилүү сандар', 'url_name': 'rounding_significant_figures'},
            {'title': 'Аралаш', 'url_name': 'rounding_mixed'},
            {'title': 'Бүтүн сандар', 'url_name': 'rounding_whole_numbers'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 3 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Болжолдоо жана тегеректөө', 'Ката аралыктары'),
        'target_items': [
            {'title': 'Ондук орундар жана маанилүү сандар', 'url_name': 'error_intervals_decimal_significant'},
            {'title': 'Эсептөөлөр', 'url_name': 'error_intervals_calculations'},
            {'title': 'Кесүү', 'url_name': 'error_intervals_truncation'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
]

# Canonical order fixes for a Subtopic's own direct children (a level up
# from the GROUPS above, which each rebuild the children *within* one of
# a subtopic's children). Production had drifted from the reference order
# in ways invisible to a fresh local dev DB, since nothing in this repo
# ever seeded these in this exact order before. Applied by exact title
# match under the named parent only - only the 'order' field changes,
# nothing is created, moved elsewhere, or deleted.
CHILD_ORDER_FIXES = [
    {
        # Money, then Recurring, then Ordering/Place Value swapped.
        'parent_path': ('Сандар', 'Ондуктар'),
        'order': [
            'Эсептөөлөр: 1 орундук сандар',
            'Эсептөөлөр: 1 жана 2 орундук сандар',
            'Эсептөөлөр: бүтүн сандар менен',
            'Эквиваленттүүлүк',
            'Акча',
            'Ондуктарды иреттөө',
            'Ондуктун орун наркы',
            'Мезгилдүү ондуктар',
        ],
    },
    {
        'parent_path': ('Сандар', 'Багытталган сандар'),
        'order': [
            'Эсептөөлөр',
            'Багытталган сандарды иреттөө',
        ],
    },
    {
        # Reference order: Approximating Calculations, Estimating Roots,
        # Estimation with Scale Drawings, Rounding, Error Intervals -
        # production had Rounding and Error Intervals ahead of the last
        # two (both pairs sharing a duplicate order value).
        'parent_path': ('Сандар', 'Болжолдоо жана тегеректөө'),
        'order': [
            'Эсептөөлөрдү болжолдоо',
            'Тамырларды болжолдоо',
            'Масштабдуу сүрөт менен болжолдоо',
            'Тегеректөө',
            'Ката аралыктары',
        ],
    },
]


class Command(BaseCommand):
    help = (
        "Rebuilds each sub-subtopic listed in GROUPS as its reference-"
        "ordered list of real pages (see "
        "onduktar_placeholders.operation_placeholder_view), replacing any "
        "generic Topic/Subtopic placeholder pages an earlier version of "
        "this command created for it. For each group: removes any "
        "'displaced_url_names' menu entries that don't correspond to any "
        "target slot; removes 'stale_subsubtopic_titles' placeholders "
        "(only if 0 resources attached); creates/repositions the target "
        "items in order; then removes any remaining child of this parent "
        "not among the target items (catches any other pre-existing menu "
        "entry, however it got there). In every case only the navigation "
        "entry is deleted - the underlying page/content is untouched. "
        "Idempotent - safe to re-run, and safe to run after adding a new "
        "group."
    )

    def handle(self, *args, **options):
        for group in GROUPS:
            topic_title, subtopic_title, parent_ss_title = group['parent_path']
            self.stdout.write(f'=== {" > ".join(group["parent_path"])} ===')
            try:
                parent_menu = MenuItem.objects.get(
                    title=parent_ss_title,
                    parent__title=subtopic_title,
                    parent__parent__title=topic_title,
                )
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'  "{" > ".join(group["parent_path"])}" not found - '
                    f'run import_reference_taxonomy / fix_number_menu first.'
                )
                continue
            except MenuItem.MultipleObjectsReturned:
                self.stderr.write(f'  Multiple menu items match "{parent_ss_title}" - resolve first.')
                continue

            subtopic = parent_menu.subtopic

            for url_name in group['displaced_url_names']:
                displaced_qs = MenuItem.objects.filter(url_name=url_name)
                removed = displaced_qs.count()
                if removed:
                    displaced_qs.delete()
                    self.stdout.write(
                        f'  Removed {removed} menu item(s) linking to {url_name} '
                        f'(the page itself is untouched).'
                    )

            for title in group['stale_subsubtopic_titles']:
                stale = SubSubtopic.objects.filter(subtopic=subtopic, title=title).first()
                if not stale:
                    continue
                if stale.resources.exists():
                    self.stdout.write(f'  NOT removing "{title}" - has resources attached, check manually.')
                    continue
                MenuItem.objects.filter(subsubtopic=stale).delete()
                stale.delete()
                self.stdout.write(f'  Removed stale placeholder "{title}"')

            for order, item in enumerate(group['target_items'], start=1):
                leaf, created = MenuItem.objects.get_or_create(
                    url_name=item['url_name'],
                    defaults={'title': item['title'], 'parent': parent_menu, 'order': order},
                )
                if created:
                    self.stdout.write(f'  Created: {item["title"]} ({item["url_name"]})')
                    continue
                changed = (
                    leaf.parent_id != parent_menu.id or leaf.order != order
                    or leaf.title != item['title']
                    or leaf.topic_id or leaf.subtopic_id or leaf.subsubtopic_id
                )
                if changed:
                    leaf.parent = parent_menu
                    leaf.order = order
                    leaf.title = item['title']
                    leaf.topic = None
                    leaf.subtopic = None
                    leaf.subsubtopic = None
                    leaf.save(update_fields=['parent', 'order', 'title', 'topic', 'subtopic', 'subsubtopic'])
                    self.stdout.write(f'  Positioned: {item["title"]} ({item["url_name"]})')

            # Anything still under this parent that isn't one of the target
            # items above is a leftover/duplicate (e.g. an old menu entry
            # never seeded by any command in this repo, so invisible to a
            # fresh local dev DB - only surfaced by running against
            # production's real, longer-lived menu state). Checked in
            # Python rather than a queryset .exclude(url_name__in=...),
            # since SQL's NULL handling makes exclude() silently skip rows
            # where url_name is NULL - exactly the shape a stale
            # subsubtopic-linked entry with no url_name takes. Only the
            # navigation entry is deleted; any underlying page/content is
            # untouched.
            target_url_names = {item['url_name'] for item in group['target_items']}
            for extra in MenuItem.objects.filter(parent=parent_menu):
                if extra.url_name not in target_url_names:
                    self.stdout.write(
                        f'  Removed extra menu item "{extra.title}" under this parent '
                        f'(any underlying page/content is untouched).'
                    )
                    extra.delete()

        for fix in CHILD_ORDER_FIXES:
            topic_title, subtopic_title = fix['parent_path']
            self.stdout.write(f'=== {topic_title} > {subtopic_title} (direct children order) ===')
            try:
                parent = MenuItem.objects.get(title=subtopic_title, parent__title=topic_title)
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'  "{topic_title} > {subtopic_title}" not found - '
                    f'run import_reference_taxonomy / fix_number_menu first.'
                )
                continue
            for order, title in enumerate(fix['order'], start=1):
                child = MenuItem.objects.filter(parent=parent, title=title).first()
                if not child:
                    continue
                if child.order != order:
                    child.order = order
                    child.save(update_fields=['order'])
                    self.stdout.write(f'  Reordered: {title} -> {order}')

        self.stdout.write(self.style.SUCCESS('Done.'))
