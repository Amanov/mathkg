from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, SubSubtopic, Subtopic

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
    {
        # None of these 3 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Бөлүүчүлөр, эселиктер жана жөнөкөй сандар', 'Эң чоң орток бөлүүчү жана эң кичине орток эселик: тизмелөө менен'),
        'target_items': [
            {'title': 'Эң чоң орток бөлүүчү', 'url_name': 'hcf_listing'},
            {'title': 'Эң кичине орток эселик', 'url_name': 'lcm_listing'},
            {'title': 'Аралаш', 'url_name': 'hcf_lcm_listing_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 3 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Бөлүүчүлөр, эселиктер жана жөнөкөй сандар', 'Эң чоң орток бөлүүчү жана эң кичине орток эселик: жөнөкөй көбөйтүүчүлөргө ажыратуу менен'),
        'target_items': [
            {'title': 'Эң чоң орток бөлүүчү', 'url_name': 'hcf_prime_factorisation'},
            {'title': 'Эң кичине орток эселик', 'url_name': 'lcm_prime_factorisation'},
            {'title': 'Аралаш', 'url_name': 'hcf_lcm_prime_factorisation_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 8 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Бөлчөктөр', 'Эсептөөлөр: бирдик бөлчөктөр'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'unit_fractions_adding'},
            {'title': 'Кемитүү', 'url_name': 'unit_fractions_subtracting'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'unit_fractions_adding_subtracting'},
            {'title': 'Көбөйтүү', 'url_name': 'unit_fractions_multiplying'},
            {'title': 'Бөлүү', 'url_name': 'unit_fractions_dividing'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'unit_fractions_multiplying_dividing'},
            {'title': 'Бүтүн сандар менен', 'url_name': 'unit_fractions_with_integers'},
            {'title': 'Аралаш', 'url_name': 'unit_fractions_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 9 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Бөлчөктөр', 'Эсептөөлөр: бирдик эмес бөлчөктөр'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'non_unit_fractions_adding'},
            {'title': 'Кемитүү', 'url_name': 'non_unit_fractions_subtracting'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'non_unit_fractions_adding_subtracting'},
            {'title': 'Көбөйтүү', 'url_name': 'non_unit_fractions_multiplying'},
            {'title': 'Бөлүү', 'url_name': 'non_unit_fractions_dividing'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'non_unit_fractions_multiplying_dividing'},
            {'title': 'Кыскартуу менен', 'url_name': 'non_unit_fractions_with_cancelling'},
            {'title': 'Бүтүн сандар менен', 'url_name': 'non_unit_fractions_with_integers'},
            {'title': 'Аралаш', 'url_name': 'non_unit_fractions_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 13 have a real hand-built page yet. This
        # "Эквиваленттүүлүк" is Бөлчөктөр's own (parent_path disambiguates
        # by requiring the grandparent to be Сандар and the parent to be
        # Бөлчөктөр specifically - there are 4 different "Эквиваленттүүлүк"
        # menu items in the tree). Overlaps content-wise with the
        # top-level Эквиваленттүүлүк topic's "Converting Fractions" (built
        # earlier), but gets its own distinct pages for the same reason as
        # every other cross-referenced duplicate this session: reusing a
        # url_name across two GROUPS entries makes this command fight over
        # repositioning it out of whichever group ran second.
        'parent_path': ('Сандар', 'Бөлчөктөр', 'Эквиваленттүүлүк'),
        'target_items': [
            {'title': 'Ондукка айландыруу', 'url_name': 'fractions_equiv_to_decimals'},
            {'title': 'Ондукка айландыруу: калькулятор менен', 'url_name': 'fractions_equiv_to_decimals_calculator'},
            {'title': 'Пайызга айландыруу', 'url_name': 'fractions_equiv_to_percentages'},
            {'title': 'Пайызга айландыруу: калькулятор менен', 'url_name': 'fractions_equiv_to_percentages_calculator'},
            {'title': 'Катышка айландыруу', 'url_name': 'fractions_equiv_to_ratios'},
            {'title': 'Баарына айландыруу', 'url_name': 'fractions_equiv_to_all'},
            {'title': 'Ондуктар менен', 'url_name': 'fractions_equiv_with_decimals'},
            {'title': 'Пайыздар менен', 'url_name': 'fractions_equiv_with_percentages'},
            {'title': 'Катыштар менен', 'url_name': 'fractions_equiv_with_ratios'},
            {'title': 'Бөлчөк, ондук жана пайыздык эквиваленттүүлүк', 'url_name': 'fractions_equiv_fdp'},
            {'title': 'Бөлчөктөрдү, ондуктарды жана пайыздарды иреттөө', 'url_name': 'fractions_equiv_fdp_ordering'},
            {'title': 'Бөлчөк, пайыз жана катыш эквиваленттүүлүгү', 'url_name': 'fractions_equiv_fpr'},
            {'title': 'Бөлчөк, ондук, пайыз жана катыш эквиваленттүүлүгү', 'url_name': 'fractions_equiv_fdpr'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 4 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Бөлчөктөр', 'Барабар бөлчөктөр'),
        'target_items': [
            {'title': 'Жөнөкөйлөтүү', 'url_name': 'equivalent_fractions_simplifying'},
            {'title': 'Салыштыруу жана иреттөө', 'url_name': 'equivalent_fractions_comparing_ordering'},
            {'title': 'Барабарсыздык белгилери менен салыштыруу', 'url_name': 'equivalent_fractions_comparing_inequality'},
            {'title': 'Эсептөөлөр менен', 'url_name': 'equivalent_fractions_with_calculations'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # None of these 2 have a real hand-built page yet.
        'parent_path': ('Сандар', 'Бөлчөктөр', 'Туюнтуу'),
        'target_items': [
            {'title': 'Чоңдук', 'url_name': 'expressing_quantity'},
            {'title': 'Өзгөрүү', 'url_name': 'expressing_change'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Даражалар" already exists as the "Indices" sub-subtopic (slug
        # 'indices') - it just had no children yet.
        'parent_path': ('Сандар', 'Даражалар жана тамырлар', 'Даражалар'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'indices_introduction'},
            {'title': 'Квадрат сандар', 'url_name': 'indices_square_numbers'},
            {'title': 'Куб сандар', 'url_name': 'indices_cube_numbers'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'indices_multiplying_dividing'},
            {'title': 'Терс даража', 'url_name': 'indices_negative'},
            {'title': 'Бөлчөк даража', 'url_name': 'indices_fractional'},
            {'title': 'Терс бөлчөк даража', 'url_name': 'indices_negative_fractional'},
            {'title': 'Кашалар менен', 'url_name': 'indices_with_brackets'},
            {'title': 'Аралаш', 'url_name': 'indices_mixed'},
            {'title': 'Даражалар менен теңдемелер', 'url_name': 'indices_equations'},
            {'title': 'Тескери сандар', 'url_name': 'indices_reciprocals'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Тамырларды эсептөө" already exists as the "Evaluating Roots"
        # sub-subtopic (slug 'evaluating-roots') - it just had no children
        # yet.
        'parent_path': ('Сандар', 'Даражалар жана тамырлар', 'Тамырларды эсептөө'),
        'target_items': [
            {'title': 'Тамырларды болжолдоо', 'url_name': 'evaluating_roots_estimating'},
            {'title': 'Квадрат', 'url_name': 'evaluating_roots_square'},
            {'title': 'Квадрат жана куб', 'url_name': 'evaluating_roots_square_cube'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Тамырлар менен эсептөөлөр" already exists as the "Surds"
        # sub-subtopic (slug 'surds') - it just had no children yet.
        'parent_path': ('Сандар', 'Даражалар жана тамырлар', 'Тамырлар менен эсептөөлөр'),
        'target_items': [
            {'title': 'Жөнөкөйлөтүү', 'url_name': 'surds_simplifying'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'surds_multiplying_dividing'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'surds_adding_subtracting'},
            {'title': 'Кашаны ачуу', 'url_name': 'surds_expanding_brackets'},
            {'title': 'Рационалдаштыруу: коньюгатасыз', 'url_name': 'surds_rationalising_without_conjugates'},
            {'title': 'Бөлүүчүнү рационалдаштыруу', 'url_name': 'surds_rationalising_denominators'},
            {'title': 'Аралаш', 'url_name': 'surds_mixed'},
            {'title': 'Пифагор менен', 'url_name': 'surds_with_pythagoras'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Эсептөөлөр: 1 жана 2 орундук" already exists as a Бүтүн сандар
        # sub-subtopic - it just had no children yet. Same 8-slot shape as
        # Ондуктар's own "1 жана 2 орундук сандар" group above, but these
        # are whole-number (not decimal) questions, so distinct url_names.
        'parent_path': ('Сандар', 'Бүтүн сандар', 'Эсептөөлөр: 1 жана 2 орундук'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'integers_adding_1_2_digit'},
            {'title': 'Кемитүү', 'url_name': 'integers_subtracting_1_2_digit'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'integers_adding_subtracting_1_2_digit'},
            {'title': 'Көбөйтүү', 'url_name': 'integers_multiplying_1_2_digit'},
            {'title': 'Бөлүү', 'url_name': 'integers_dividing_1_2_digit'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'integers_multiplying_dividing_1_2_digit'},
            {'title': '10, 100, 1000гө көбөйтүү жана бөлүү', 'url_name': 'integers_multiplying_dividing_10_100_1000'},
            {'title': 'Аралаш', 'url_name': 'integers_mixed_1_2_digit'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Эсептөөлөр: 2 жана 3 орундук" already exists as a Бүтүн сандар
        # sub-subtopic - it just had no children yet. Same shape as the
        # group above minus the "10, 100, 1000" slot (reference doesn't
        # show that shortcut at this digit size).
        'parent_path': ('Сандар', 'Бүтүн сандар', 'Эсептөөлөр: 2 жана 3 орундук'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'integers_adding_2_3_digit'},
            {'title': 'Кемитүү', 'url_name': 'integers_subtracting_2_3_digit'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'integers_adding_subtracting_2_3_digit'},
            {'title': 'Көбөйтүү', 'url_name': 'integers_multiplying_2_3_digit'},
            {'title': 'Бөлүү', 'url_name': 'integers_dividing_2_3_digit'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'integers_multiplying_dividing_2_3_digit'},
            {'title': 'Аралаш', 'url_name': 'integers_mixed_2_3_digit'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Эсептөөлөр: ондуктар менен" already exists as a Бүтүн сандар
        # sub-subtopic - it just had no children yet. Same 8-slot shape as
        # Ондуктар's own "бүтүн сандар менен" group above (Adding through
        # Mixed plus "Dividing: Divisor <1"), but here it's integers
        # combined with decimals, so distinct url_names.
        'parent_path': ('Сандар', 'Бүтүн сандар', 'Эсептөөлөр: ондуктар менен'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'integers_adding_with_decimals'},
            {'title': 'Кемитүү', 'url_name': 'integers_subtracting_with_decimals'},
            {'title': 'Кошуу жана кемитүү', 'url_name': 'integers_adding_subtracting_with_decimals'},
            {'title': 'Көбөйтүү', 'url_name': 'integers_multiplying_with_decimals'},
            {'title': 'Бөлүү', 'url_name': 'integers_dividing_with_decimals'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'integers_multiplying_dividing_with_decimals'},
            {'title': 'Аралаш', 'url_name': 'integers_mixed_with_decimals'},
            {'title': 'Бөлүүчүсү 1ден кичине бөлүү', 'url_name': 'integers_dividing_divisor_less_than_1_with_decimals'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Турмуштук маселелер" already exists as a Бүтүн сандар
        # sub-subtopic - it just had no children yet.
        'parent_path': ('Сандар', 'Бүтүн сандар', 'Турмуштук маселелер'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'integers_real_life_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'integers_real_life_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Татаал өлчөмдөр" (Compound) already exists as an Өлчөмдөр
        # sub-subtopic - it just had no children yet. Its own "Area &
        # Volume Conversion" child shares a display name with the
        # top-level Measures sibling of the same name (a genuine
        # duplicate on the reference site, not a mistake) - distinct
        # url_name, own chevron/children left for a future screenshot.
        # "Ылдамдык, аралык жана убакыт" (Speed, Distance & Time) is NOT
        # listed here even though it's a direct child - PROMOTE_LEAVES
        # below turned it into its own category with 4 children, which
        # this list's simple flat-leaf model can't represent, so it owns
        # that item's lifecycle now (see 'promoted_titles').
        'parent_path': ('Сандар', 'Өлчөмдөр', 'Татаал өлчөмдөр'),
        'target_items': [
            {'title': 'Аянт жана көлөм бирдиктерин алмаштыруу', 'url_name': 'compound_area_volume_conversion'},
            {'title': 'Тыгыздык, масса жана көлөм', 'url_name': 'compound_density_mass_volume'},
            {'title': 'Жумуш-сааттар', 'url_name': 'compound_work_hours'},
            {'title': 'Калктын калыңдыгы', 'url_name': 'compound_population_density'},
            {'title': 'Басым, күч жана аянт', 'url_name': 'compound_pressure_force_area'},
            {'title': 'Эмгек акы ставкалары', 'url_name': 'compound_rates_of_pay'},
        ],
        'promoted_titles': ['Ылдамдык, аралык жана убакыт'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Акча" already exists as an Өлчөмдөр sub-subtopic - it just had
        # no children yet. Same 5 slots as Ондуктар's own "Акча" group
        # above, but distinct url_names (measures_money_* prefix) since
        # this is a separate topic.
        'parent_path': ('Сандар', 'Өлчөмдөр', 'Акча'),
        'target_items': [
            {'title': 'Сатып алуу: калькулятор менен', 'url_name': 'measures_money_purchasing_calculator'},
            {'title': 'Сатып алуу: калькуляторсуз', 'url_name': 'measures_money_purchasing_non_calculator'},
            {'title': 'Насыяга сатып алуу', 'url_name': 'measures_money_hire_purchase'},
            {'title': 'Эсептер жана көчүрмөлөр', 'url_name': 'measures_money_bills_statements'},
            {'title': 'Эмгек акы ставкалары', 'url_name': 'measures_money_rates_of_pay'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Масштабдуу сүрөттөр" already exists as an Өлчөмдөр sub-subtopic
        # - it just had no children yet.
        'parent_path': ('Сандар', 'Өлчөмдөр', 'Масштабдуу сүрөттөр'),
        'target_items': [
            {'title': 'Узундуктар', 'url_name': 'scale_drawings_lengths'},
            {'title': 'Болжолдоо', 'url_name': 'scale_drawings_estimation'},
            {'title': 'Багыттар менен', 'url_name': 'scale_drawings_with_bearings'},
            {'title': 'Аянттар', 'url_name': 'scale_drawings_areas'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Өлчөө системалары" already exists as an Өлчөмдөр sub-subtopic -
        # it just had no children yet.
        'parent_path': ('Сандар', 'Өлчөмдөр', 'Өлчөө системалары'),
        'target_items': [
            {'title': 'Империялык система', 'url_name': 'systems_of_measurement_imperial'},
            {'title': 'Метрикалык система', 'url_name': 'systems_of_measurement_metric'},
            {'title': 'Аралаш', 'url_name': 'systems_of_measurement_mixed'},
            {'title': 'Айландыруу коэффициенттери', 'url_name': 'systems_of_measurement_conversion_factors'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # The top-level "Аянт жана көлөм бирдиктерин алмаштыруу" sibling
        # (distinct from Compound's own child of the same name) already
        # exists as an Өлчөмдөр sub-subtopic - it just had no children yet.
        'parent_path': ('Сандар', 'Өлчөмдөр', 'Аянт жана көлөм бирдиктерин алмаштыруу'),
        'target_items': [
            {'title': 'Аянт', 'url_name': 'area_volume_conversion_area'},
            {'title': 'Көлөм', 'url_name': 'area_volume_conversion_volume'},
            {'title': 'Аралаш', 'url_name': 'area_volume_conversion_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Убакыт" already exists as an Өлчөмдөр sub-subtopic - it just
        # had no children yet.
        'parent_path': ('Сандар', 'Өлчөмдөр', 'Убакыт'),
        'target_items': [
            {'title': 'Саатты окуу', 'url_name': 'time_reading_clocks'},
            {'title': 'Күндөр, айлар жана жылдар', 'url_name': 'time_days_months_years'},
            {'title': 'Жүрүш тартиби', 'url_name': 'time_timetables'},
            {'title': 'Эсептөөлөр', 'url_name': 'time_calculations'},
            {'title': 'Айландыруу', 'url_name': 'time_converting'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Көбөйтүү жана бөлүү" already exists as a Стандарттык форма
        # sub-subtopic - it just had no children yet.
        'parent_path': ('Сандар', 'Стандарттык форма', 'Көбөйтүү жана бөлүү'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'standard_form_multiplying_dividing_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'standard_form_multiplying_dividing_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Айландыруу" already exists as a Стандарттык форма sub-subtopic
        # - it just had no children yet.
        'parent_path': ('Сандар', 'Стандарттык форма', 'Айландыруу'),
        'target_items': [
            {'title': 'Жөнөкөйдөн стандарттык формага', 'url_name': 'standard_form_converting_ordinary_to_standard'},
            {'title': 'Стандарттык формадан жөнөкөйгө', 'url_name': 'standard_form_converting_standard_to_ordinary'},
            {'title': 'Аралаш', 'url_name': 'standard_form_converting_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Түз жана тескери пропорция" already exists as a direct child
        # of the root Пропорция topic (2-tuple parent_path, see the
        # resolution logic above) - it just had no children yet.
        'parent_path': ('Пропорция', 'Түз жана тескери пропорция'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'direct_inverse_introduction'},
            {'title': 'Түз пропорция', 'url_name': 'direct_inverse_direct'},
            {'title': 'Тескери пропорция', 'url_name': 'direct_inverse_inverse'},
            {'title': 'Аралаш', 'url_name': 'direct_inverse_mixed'},
            {'title': 'Графиктерди аныктоо', 'url_name': 'direct_inverse_identifying_graphs'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Графиктер" (renamed from "Айландыруу графиктери" - see
        # CHILD_ORDER_FIXES's ('Пропорция',) entry - only had 0 children
        # either way). Referenced here by its final/renamed title, so on
        # a from-scratch run this entry doesn't find it until the rename
        # runs (GROUPS runs before CHILD_ORDER_FIXES) - settles on a
        # second run, same as other cross-mechanism dependencies here.
        'parent_path': ('Пропорция', 'Графиктер'),
        'target_items': [
            {'title': 'Пропорционалдуу графиктерди аныктоо', 'url_name': 'graphs_identifying_proportional'},
            {'title': 'Айландыруу графиктери', 'url_name': 'graphs_conversion_graphs'},
            {'title': 'Баа мамилелери', 'url_name': 'graphs_cost_relationships'},
            {'title': 'Тереңдик-убакыт', 'url_name': 'graphs_depth_time'},
            {'title': 'Көлөм-убакыт', 'url_name': 'graphs_volume_time'},
            {'title': 'Аралаш', 'url_name': 'graphs_mixed'},
            {'title': 'Аралык-убакыт: туруктуу ылдамдыктар', 'url_name': 'graphs_distance_time_constant_speeds'},
            {'title': 'Аралык-убакыт: өзгөрмө ылдамдыктар', 'url_name': 'graphs_distance_time_variable_speeds'},
            {'title': 'Ылдамдык-убакыт', 'url_name': 'graphs_velocity_time'},
            {'title': 'Аралаш: аралык жана ылдамдык', 'url_name': 'graphs_mixed_distance_velocity'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Айландыруу графиктери" (Conversion Graphs) already exists as
        # a Графиктер sub-subtopic - it just had no children yet.
        'parent_path': ('Пропорция', 'Графиктер', 'Айландыруу графиктери'),
        'target_items': [
            {'title': 'Окуу', 'url_name': 'graphs_conversion_reading'},
            {'title': 'Тургузуу жана окуу', 'url_name': 'graphs_conversion_plotting_reading'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Баа мамилелери" (Cost Relationships) already exists as a
        # Графиктер sub-subtopic - it just had no children yet.
        'parent_path': ('Пропорция', 'Графиктер', 'Баа мамилелери'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'graphs_cost_introduction'},
            {'title': 'Теңдемелер менен', 'url_name': 'graphs_cost_with_equations'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Аралык-убакыт: туруктуу ылдамдыктар" (Distance-Time: Constant
        # Speeds) already exists as a Графиктер sub-subtopic - it just
        # had no children yet.
        'parent_path': ('Пропорция', 'Графиктер', 'Аралык-убакыт: туруктуу ылдамдыктар'),
        'target_items': [
            {'title': 'Окуу', 'url_name': 'graphs_distance_time_reading'},
            {'title': 'Тургузуу жана окуу', 'url_name': 'graphs_distance_time_plotting_reading'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Ылдамдык-убакыт" (Velocity-Time) already exists as a
        # Графиктер sub-subtopic - it just had no children yet.
        'parent_path': ('Пропорция', 'Графиктер', 'Ылдамдык-убакыт'),
        'target_items': [
            {'title': 'Аралык', 'url_name': 'graphs_velocity_time_distance'},
            {'title': 'Ылдамдануу', 'url_name': 'graphs_velocity_time_acceleration'},
            {'title': 'Аралаш', 'url_name': 'graphs_velocity_time_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Туюнтуу" already exists as a chevron-bearing SubSubtopic under
        # Пайыздар: калькулятор менен (see import_reference_taxonomy.py) -
        # it just had no children yet. New url_names (not reused from
        # Сандар > Бөлчөктөр > Туюнтуу's own "Чоңдук"/"Өзгөрүү" pages)
        # since these cover the percentage version of the same generic
        # titles, not the same pages.
        'parent_path': ('Пропорция', 'Пайыздар: калькулятор менен', 'Туюнтуу'),
        'target_items': [
            {'title': 'Бөлчөктөрдү айландыруу', 'url_name': 'percentages_expressing_converting_fractions'},
            {'title': 'Чоңдук', 'url_name': 'percentages_expressing_quantity'},
            {'title': 'Өзгөрүү', 'url_name': 'percentages_expressing_change'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Чоңдуктун пайызы" already exists as a chevron-bearing
        # SubSubtopic under Пайыздар: калькулятор менен (see
        # import_reference_taxonomy.py) - it just had no children yet.
        # Reference: Integer, Decimal, Reverse, FPR of Quantities (the
        # last one - expressing a quantity as a fraction, percentage or
        # ratio of another - translated as a short noun phrase rather
        # than spelled out, matching this file's usual title length).
        'parent_path': ('Пропорция', 'Пайыздар: калькулятор менен', 'Чоңдуктун пайызы'),
        'target_items': [
            {'title': 'Бүтүн сан', 'url_name': 'percentages_quantity_integer'},
            {'title': 'Ондук бөлчөк', 'url_name': 'percentages_quantity_decimal'},
            {'title': 'Тескери', 'url_name': 'percentages_quantity_reverse'},
            {'title': 'Бөлчөк, пайыз жана катыш', 'url_name': 'percentages_quantity_fpr'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Көбөйтүү жана азайтуу" already exists as a chevron-bearing
        # SubSubtopic under Пайыздар: калькулятор менен - it just had no
        # children yet. Reference (7 items): Increase, Decrease, Mixed,
        # Simple Interest, Using a Multiplier, Reverse, Marginal Tax.
        'parent_path': ('Пропорция', 'Пайыздар: калькулятор менен', 'Көбөйтүү жана азайтуу'),
        'target_items': [
            {'title': 'Көбөйтүү', 'url_name': 'percentages_incdec_increase'},
            {'title': 'Азайтуу', 'url_name': 'percentages_incdec_decrease'},
            {'title': 'Аралаш', 'url_name': 'percentages_incdec_mixed'},
            {'title': 'Жөнөкөй пайыз', 'url_name': 'percentages_incdec_simple_interest'},
            {'title': 'Көбөйтүүчү менен', 'url_name': 'percentages_incdec_using_multiplier'},
            {'title': 'Тескери', 'url_name': 'percentages_incdec_reverse'},
            {'title': 'Чектик салык', 'url_name': 'percentages_incdec_marginal_tax'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Кайталанма пайыздык өзгөрүү" already exists as a chevron-
        # bearing SubSubtopic under Пайыздар: калькулятор менен - it just
        # had no children yet. Reference (5 items): Increase & Compound
        # Interest, Decrease, Increase & Decrease, Reverse, Mixed.
        'parent_path': ('Пропорция', 'Пайыздар: калькулятор менен', 'Кайталанма пайыздык өзгөрүү'),
        'target_items': [
            {'title': 'Көбөйтүү жана татаал пайыз', 'url_name': 'percentages_repeated_change_increase_compound_interest'},
            {'title': 'Азайтуу', 'url_name': 'percentages_repeated_change_decrease'},
            {'title': 'Көбөйтүү жана азайтуу', 'url_name': 'percentages_repeated_change_increase_decrease'},
            {'title': 'Тескери', 'url_name': 'percentages_repeated_change_reverse'},
            {'title': 'Аралаш', 'url_name': 'percentages_repeated_change_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Туюнтуу" already exists as a chevron-bearing SubSubtopic under
        # Пайыздар: калькуляторсуз - it just had no children yet.
        # Reference gives it 3 children: Converting Fractions (itself
        # chevron-bearing - not a flat leaf like its Calculator-side
        # namesake), Quantity, Change. "Converting Fractions" is mirrored
        # in via MIRROR_NODES below (same underlying content as Сандар >
        # Эквиваленттүүлүк > Бөлчөктөрдү айландыруу, same reasoning as
        # Барабардык's own mirror) rather than built here, so it's
        # protected from this entry's own pruning via 'promoted_titles'.
        'parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Туюнтуу'),
        'target_items': [
            {'title': 'Чоңдук', 'url_name': 'percentages_noncalc_expressing_quantity'},
            {'title': 'Өзгөрүү', 'url_name': 'percentages_noncalc_expressing_change'},
        ],
        'promoted_titles': ['Бөлчөктөрдү айландыруу'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Чоңдуктун пайызы" already exists as a chevron-bearing
        # SubSubtopic under Пайыздар: калькуляторсуз - it just had no
        # children yet. Reference (6 items): 10s, 5s, Integer & Decimal,
        # Reverse, FPR of Quantities, FPR: With Frequency Trees.
        'parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Чоңдуктун пайызы'),
        'target_items': [
            {'title': '10дор менен', 'url_name': 'percentages_noncalc_quantity_10s'},
            {'title': '5тер менен', 'url_name': 'percentages_noncalc_quantity_5s'},
            {'title': 'Бүтүн сан жана ондук бөлчөк', 'url_name': 'percentages_noncalc_quantity_integer_decimal'},
            {'title': 'Тескери', 'url_name': 'percentages_noncalc_quantity_reverse'},
            {'title': 'Бөлчөк, пайыз жана катыш', 'url_name': 'percentages_noncalc_quantity_fpr'},
            {'title': 'Бөлчөк, пайыз жана катыш: жыштык дарактары менен', 'url_name': 'percentages_noncalc_quantity_fpr_frequency_trees'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Көбөйтүү жана азайтуу" already exists as a chevron-bearing
        # SubSubtopic under Пайыздар: калькуляторсуз - it just had no
        # children yet. Reference (4 items): Increase, Decrease, Mixed,
        # Reverse - a shorter list than its Calculator-side namesake
        # (no Simple Interest/Using a Multiplier/Marginal Tax here).
        'parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Көбөйтүү жана азайтуу'),
        'target_items': [
            {'title': 'Көбөйтүү', 'url_name': 'percentages_noncalc_incdec_increase'},
            {'title': 'Азайтуу', 'url_name': 'percentages_noncalc_incdec_decrease'},
            {'title': 'Аралаш', 'url_name': 'percentages_noncalc_incdec_mixed'},
            {'title': 'Тескери', 'url_name': 'percentages_noncalc_incdec_reverse'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Туюнтуу" already exists as a chevron-bearing SubSubtopic under
        # Катыш - it just had no children yet. Reference (3 flat items):
        # Division, Simplifying, 1:n.
        'parent_path': ('Пропорция', 'Катыш', 'Туюнтуу'),
        'target_items': [
            {'title': 'Бөлүү', 'url_name': 'ratio_expressing_division'},
            {'title': 'Жөнөкөйлөтүү', 'url_name': 'ratio_expressing_simplifying'},
            {'title': '1:n', 'url_name': 'ratio_expressing_1_to_n'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Катыштар жана чоңдуктар" (Ratios & Quantities) already exists
        # as a chevron-bearing SubSubtopic under Катыш - it just had no
        # children yet. Corrected: reference actually gives it 7 FLAT
        # items (Dividing Into a Ratio, Reverse, Mixed, With Line
        # Segments, FPR: Calculator, FPR: Non-Calculator, FPR: With
        # Frequency Trees) - an earlier pass misread the grid as Dividing
        # Into a Ratio being its own chevron-bearing category with the
        # last 4 nested under it, when they're really all siblings at
        # this one level (same "column runs longer than the sibling list
        # beside it" layout as Percentage of a Quantity's 6 flat items
        # elsewhere in this file).
        'parent_path': ('Пропорция', 'Катыш', 'Катыштар жана чоңдуктар'),
        'target_items': [
            {'title': 'Катышка бөлүү', 'url_name': 'ratio_dividing_into_a_ratio'},
            {'title': 'Тескери', 'url_name': 'ratio_quantities_reverse'},
            {'title': 'Аралаш', 'url_name': 'ratio_quantities_mixed'},
            {'title': 'Сызык кесиндилери менен', 'url_name': 'ratio_dividing_with_line_segments'},
            {'title': 'Бөлчөк, пайыз жана катыш: калькулятор менен', 'url_name': 'ratio_dividing_fpr_calculator'},
            {'title': 'Бөлчөк, пайыз жана катыш: калькуляторсуз', 'url_name': 'ratio_dividing_fpr_non_calculator'},
            {'title': 'Бөлчөк, пайыз жана катыш: жыштык дарактары менен', 'url_name': 'ratio_dividing_fpr_frequency_trees'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Түрлөндүрүү" (Manipulation) already exists as a chevron-bearing
        # SubSubtopic under Катыш - it just had no children yet.
        # Reference (4 flat items): 1:n, Comparing Parts, Combining,
        # Changing.
        'parent_path': ('Пропорция', 'Катыш', 'Түрлөндүрүү'),
        'target_items': [
            {'title': '1:n', 'url_name': 'ratio_manipulation_1_to_n'},
            {'title': 'Бөлүктөрдү салыштыруу', 'url_name': 'ratio_manipulation_comparing_parts'},
            {'title': 'Бириктирүү', 'url_name': 'ratio_manipulation_combining'},
            {'title': 'Өзгөртүү', 'url_name': 'ratio_manipulation_changing'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Аралаш" (Mixed, the 5th top-level Катыш sibling) already
        # exists as a chevron-bearing SubSubtopic - it just had no
        # children yet. Reference (2 flat items): Foundation, Higher (UK
        # GCSE difficulty tiers).
        'parent_path': ('Пропорция', 'Катыш', 'Аралаш'),
        'target_items': [
            {'title': 'Негизги деңгээл', 'url_name': 'ratio_mixed_foundation'},
            {'title': 'Жогорку деңгээл', 'url_name': 'ratio_mixed_higher'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Баалар" (Prices) is a brand new chevron-bearing child of
        # Турмуштук колдонуулар, created via 'create_subsubtopics' below
        # before this entry's own target_items can find it (a cross-run
        # dependency - settles on a 2nd run of the command). Reference
        # (2 items): Calculator, Non-Calculator.
        'parent_path': ('Пропорция', 'Турмуштук колдонуулар', 'Баалар'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'real_life_prices_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'real_life_prices_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Пайдалуу сатып алуу" (Best Buys) already exists as a chevron-
        # bearing SubSubtopic under Турмуштук колдонуулар - it just had
        # no children yet. Reference (2 items): Calculator,
        # Non-Calculator.
        'parent_path': ('Пропорция', 'Турмуштук колдонуулар', 'Пайдалуу сатып алуу'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'real_life_best_buys_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'real_life_best_buys_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Валюта курстары" (Exchange Rates) already exists as a chevron-
        # bearing SubSubtopic under Турмуштук колдонуулар - it just had
        # no children yet. Reference (2 items): Calculator,
        # Non-Calculator.
        'parent_path': ('Пропорция', 'Турмуштук колдонуулар', 'Валюта курстары'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'real_life_exchange_rates_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'real_life_exchange_rates_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Рецепттер" (Recipes) already exists as a chevron-bearing
        # SubSubtopic under Турмуштук колдонуулар - it just had no
        # children yet. Reference (2 items): Calculator, Non-Calculator.
        'parent_path': ('Пропорция', 'Турмуштук колдонуулар', 'Рецепттер'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'real_life_recipes_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'real_life_recipes_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Аралаш" (Mixed, the 5th top-level Турмуштук колдонуулар
        # sibling) is a brand new chevron-bearing child, created via
        # 'create_subsubtopics' below before this entry's own
        # target_items can find it. Reference (2 items): Calculator,
        # Non-Calculator - same shape as its 4 siblings above.
        'parent_path': ('Пропорция', 'Турмуштук колдонуулар', 'Аралаш'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'real_life_mixed_calculator'},
            {'title': 'Калькуляторсуз', 'url_name': 'real_life_mixed_non_calculator'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Киришүү" (Introduction) under Алгебра was empty. Reference (4
        # items): Definitions, Notation, Forming Expressions (itself
        # chevron-bearing - created via 'create_subsubtopics' below,
        # protected from this entry's pruning via 'promoted_titles'),
        # Manipulating Formulae.
        'parent_path': ('Алгебра', 'Киришүү'),
        'target_items': [
            {'title': 'Аныктамалар', 'url_name': 'algebra_intro_definitions'},
            {'title': 'Белгилөөлөр', 'url_name': 'algebra_intro_notation'},
            {'title': 'Формулаларды түрлөндүрүү', 'url_name': 'algebra_intro_manipulating_formulae'},
        ],
        'promoted_titles': ['Туюнтмаларды түзүү'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Туюнтмаларды түзүү" (Forming Expressions) is a fresh chevron-
        # bearing child of Киришүү - created via 'create_subsubtopics'
        # below before this entry's own target_items can find it.
        # Reference (3 items): With Function Machines, Linear, Quadratic.
        'parent_path': ('Алгебра', 'Киришүү', 'Туюнтмаларды түзүү'),
        'target_items': [
            {'title': 'Функция машиналары менен', 'url_name': 'algebra_forming_expr_function_machines'},
            {'title': 'Сызыктуу', 'url_name': 'algebra_forming_expr_linear'},
            {'title': 'Квадраттык', 'url_name': 'algebra_forming_expr_quadratic'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Теңдемелер: сызыктуу" (Equations: Linear) already had 4
        # chevron-bearing children from the original taxonomy import, all
        # still empty. Corrected: further screenshots revealed "Түзүү",
        # both "Белгисиз бир жагында" variants, and "Белгисиз эки
        # жагында" all have their own chevron children too (an earlier
        # pass wrongly built them as flat leaves). Their old url_names
        # are one-time-deleted via 'displaced_url_names' below (so the
        # wrong-type flat MenuItems are gone for good, letting
        # CHILD_ORDER_FIXES's 'create_subsubtopics' recreate each as a
        # proper empty category), while their titles are ALSO in
        # 'promoted_titles' - needed permanently, not just for the
        # transition, since without it this entry's own pruning step
        # would delete the newly-recreated categories again on every
        # later run (they're not flat leaves in target_items, so nothing
        # else protects them). Only 4 of the original 8 flat items remain
        # flat here; each promoted category is filled by its own
        # dedicated GROUPS entry below.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу'),
        'target_items': [
            {'title': 'Рационалдык', 'url_name': 'algebra_linear_rational'},
            {'title': 'Аралаш', 'url_name': 'algebra_linear_mixed'},
            {'title': 'Барабарсыздыктар', 'url_name': 'algebra_linear_inequalities'},
            {'title': 'Белгисиз даражалар менен', 'url_name': 'algebra_linear_unknown_indices'},
        ],
        'promoted_titles': [
            'Кашаа менен', 'Функциялар менен', 'Түзүү',
            'Белгисиз бир жагында: калькулятор менен',
            'Белгисиз бир жагында: калькуляторсуз',
            'Белгисиз эки жагында',
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [
            'algebra_linear_forming',
            'algebra_linear_variable_one_side_calculator',
            'algebra_linear_variable_one_side_non_calculator',
            'algebra_linear_variable_both_sides',
        ],
    },
    {
        # "Кашаа менен" (With Brackets) already existed as a chevron-
        # bearing SubSubtopic under Теңдемелер: сызыктуу - it just had no
        # children yet. Reference (3 items): Without Coefficients, With
        # Coefficients, Multiple.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу', 'Кашаа менен'),
        'target_items': [
            {'title': 'Коэффициентсиз', 'url_name': 'algebra_linear_brackets_without_coefficients'},
            {'title': 'Коэффициент менен', 'url_name': 'algebra_linear_brackets_with_coefficients'},
            {'title': 'Бир нече', 'url_name': 'algebra_linear_brackets_multiple'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Түзүү" (Forming) under Теңдемелер: сызыктуу is a fresh
        # chevron-bearing category, created via 'create_subsubtopics'
        # below before this entry can find it. Reference (3 items):
        # Shapes/Angles & Real Life, With Function Machines, With
        # Functions & Sequences.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу', 'Түзүү'),
        'target_items': [
            {'title': 'Фигуралар, бурчтар жана турмуштук маселелер', 'url_name': 'algebra_linear_forming_shapes_angles_real_life'},
            {'title': 'Функция машиналары менен', 'url_name': 'algebra_linear_forming_function_machines'},
            {'title': 'Функциялар жана ырааттуулуктар менен', 'url_name': 'algebra_linear_forming_functions_sequences'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Белгисиз бир жагында: калькулятор менен" (Variable on One
        # Side: Calculator) is a fresh chevron-bearing category, created
        # via 'create_subsubtopics' below. Reference (4 items): 1-Step,
        # 2-Step, 3-Step, Mixed.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу', 'Белгисиз бир жагында: калькулятор менен'),
        'target_items': [
            {'title': '1-кадам', 'url_name': 'algebra_linear_var1side_calc_1step'},
            {'title': '2-кадам', 'url_name': 'algebra_linear_var1side_calc_2step'},
            {'title': '3-кадам', 'url_name': 'algebra_linear_var1side_calc_3step'},
            {'title': 'Аралаш', 'url_name': 'algebra_linear_var1side_calc_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Белгисиз бир жагында: калькуляторсуз" (Variable on One Side:
        # Non-Calculator) is a fresh chevron-bearing category, created
        # via 'create_subsubtopics' below. Reference (4 items): 1-Step,
        # 2-Step, 3-Step, Rational.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу', 'Белгисиз бир жагында: калькуляторсуз'),
        'target_items': [
            {'title': '1-кадам', 'url_name': 'algebra_linear_var1side_noncalc_1step'},
            {'title': '2-кадам', 'url_name': 'algebra_linear_var1side_noncalc_2step'},
            {'title': '3-кадам', 'url_name': 'algebra_linear_var1side_noncalc_3step'},
            {'title': 'Рационалдык', 'url_name': 'algebra_linear_var1side_noncalc_rational'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Белгисиз эки жагында" (Variable on Both Sides) is a fresh
        # chevron-bearing category, created via 'create_subsubtopics'
        # below. Reference (4 items): Without Brackets, With Brackets,
        # Graphical Intersections, With Parallel Lines.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу', 'Белгисиз эки жагында'),
        'target_items': [
            {'title': 'Кашаасыз', 'url_name': 'algebra_linear_var_both_sides_without_brackets'},
            {'title': 'Кашаа менен', 'url_name': 'algebra_linear_var_both_sides_with_brackets'},
            {'title': 'Графиктердин кесилиши', 'url_name': 'algebra_linear_var_both_sides_graphical_intersections'},
            {'title': 'Параллель сызыктар менен', 'url_name': 'algebra_linear_var_both_sides_parallel_lines'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Теңдемелер: квадраттык" (Equations: Quadratic) already had 2
        # chevron-bearing children (Көбөйтүүчүлөргө ажыратуу, Ыкмалар),
        # both still empty. Reference shows 13 items, none chevron-
        # bearing (all flat leaves, including a more specific
        # factorisation title) - both old categories are replaced, same
        # prune-and-rebuild-as-leaves reasoning as Equations: Linear
        # above. Screenshot's list may continue past "Barabarsyzdyktar"
        # (a partial "M" is cut off at the bottom edge) - these 13 are
        # what's clearly visible; flagged for the user to confirm this
        # is the complete list.
        'parent_path': ('Алгебра', 'Теңдемелер: квадраттык'),
        'target_items': [
            {'title': 'Түзүү', 'url_name': 'algebra_quadratic_forming'},
            {'title': 'Көбөйтүүчүлөргө ажыратуу: эки кашаа менен', 'url_name': 'algebra_quadratic_factorisation_double_brackets'},
            {'title': 'b = 0', 'url_name': 'algebra_quadratic_b_zero'},
            {'title': 'c = 0', 'url_name': 'algebra_quadratic_c_zero'},
            {'title': 'Толук квадратка келтирүү', 'url_name': 'algebra_quadratic_completing_square'},
            {'title': 'Рационалдык', 'url_name': 'algebra_quadratic_rational'},
            {'title': 'Квадраттык теңдеме формуласы', 'url_name': 'algebra_quadratic_formula'},
            {'title': 'Чечими жок теңдемелер', 'url_name': 'algebra_quadratic_no_solution'},
            {'title': 'Аралаш', 'url_name': 'algebra_quadratic_mixed'},
            {'title': 'Сыноо жана жакшыртуу', 'url_name': 'algebra_quadratic_trial_improvement'},
            {'title': 'Кайталануу', 'url_name': 'algebra_quadratic_iteration'},
            {'title': 'Кесилишүү аркылуу', 'url_name': 'algebra_quadratic_by_intersection'},
            {'title': 'Барабарсыздыктар', 'url_name': 'algebra_quadratic_inequalities'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Теңдемелер: системасы" (Equations: Simultaneous) already had
        # 2 chevron-bearing children - "Жоюу ыкмасы" (Elimination)
        # matches the reference's own chevron-bearing "Elimination" item
        # exactly, so it's kept (protected via 'promoted_titles');
        # "Ыкмалар" (the generic "Methods" placeholder) isn't in the
        # reference at all and is replaced by the 5 specific flat items
        # below.
        'parent_path': ('Алгебра', 'Теңдемелер: системасы'),
        'target_items': [
            {'title': 'Түзүү', 'url_name': 'algebra_simultaneous_forming'},
            {'title': 'Алмаштыруу', 'url_name': 'algebra_simultaneous_substitution'},
            {'title': 'Аралаш', 'url_name': 'algebra_simultaneous_mixed'},
            {'title': 'Графикалык жол менен', 'url_name': 'algebra_simultaneous_graphically'},
            {'title': 'Сызыктуу жана сызыктуу эмес', 'url_name': 'algebra_simultaneous_linear_non_linear'},
        ],
        'promoted_titles': ['Жоюу ыкмасы'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
]

# A flat GROUPS-built leaf that turns out to have its own sub-items on
# the reference site - the leaf itself becomes a category, its existing
# page survives unchanged as the new "Introduction" first child (same
# url_name, same content), and the rest are brand new pages alongside
# it. The leaf's own identity (id/title/parent/order) never changes -
# only its url_name moves onto the new "Introduction" child - so nothing
# elsewhere that already points at this title needs updating.
PROMOTE_LEAVES = [
    {
        # Reference: "Speed, Distance & Time" has 4 children (Adding
        # Introduction, Converting Speeds, 2-Stage Journeys, Relative
        # Speeds) - previously a flat leaf in the "Сандар > Өлчөмдөр >
        # Татаал өлчөмдөр" GROUPS entry above (see 'promoted_titles'
        # there, which now excludes it and protects it from that entry's
        # own pruning).
        'leaf_path': ('Сандар', 'Өлчөмдөр', 'Татаал өлчөмдөр', 'Ылдамдык, аралык жана убакыт'),
        'introduction_title': 'Киришүү',
        'new_children': [
            {'title': 'Ылдамдыкты айландыруу', 'url_name': 'speed_distance_time_converting_speeds'},
            {'title': 'Эки этаптуу саякаттар', 'url_name': 'speed_distance_time_two_stage_journeys'},
            {'title': 'Салыштырмалуу ылдамдыктар', 'url_name': 'speed_distance_time_relative_speeds'},
        ],
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
    {
        # Reference order: Prime Numbers, Multiples, Factors, Mixed, Prime
        # Factorisation, HCF & LCM: Listing, HCF & LCM: Prime
        # Factorisation - production had the 2 HCF & LCM items pulled
        # forward to positions 2-3 (sharing duplicate order values with
        # Multiples/Factors). All 7 already exist as real menu entries;
        # this only fixes their order, nothing is created or removed.
        'parent_path': ('Сандар', 'Бөлүүчүлөр, эселиктер жана жөнөкөй сандар'),
        'order': [
            'Жөнөкөй сандар',
            'Эселиктер',
            'Бөлүүчүлөр',
            'Жөнөкөй сандар, бөлүүчүлөр жана эселиктер',
            'Даража түрүндөгү жөнөкөй көбөйтүүчүлөргө ажыратуу',
            'Эң чоң орток бөлүүчү жана эң кичине орток эселик: тизмелөө менен',
            'Эң чоң орток бөлүүчү жана эң кичине орток эселик: жөнөкөй көбөйтүүчүлөргө ажыратуу менен',
        ],
    },
    {
        # Reference order: Introduction, Writing as Words, Arithmetic:
        # Unit Fractions, Arithmetic: Non-Unit Fractions, Equivalence,
        # Equivalent Fractions, Expressing, Fraction of a Quantity, Mixed
        # Numbers & Improper Fractions, Mixed, Reciprocals, With a
        # Calculator - production had positions 2/3 swapped (Arithmetic:
        # Unit Fractions ahead of Writing as Words) and Equivalence pulled
        # back to position 7 instead of 5 (all sharing duplicate order
        # values with their neighbours). All 12 already exist as real menu
        # entries with accurate translations; this only fixes their order.
        'parent_path': ('Сандар', 'Бөлчөктөр'),
        'order': [
            'Киришүү',
            'Бөлчөктөрдү сөз менен туюнтуу',
            'Эсептөөлөр: бирдик бөлчөктөр',
            'Эсептөөлөр: бирдик эмес бөлчөктөр',
            'Эквиваленттүүлүк',
            'Барабар бөлчөктөр',
            'Туюнтуу',
            'Чоңдуктун бөлчөгү',
            'Аралаш сандар жана туура эмес бөлчөктөр',
            'Аралаш бөлчөктөр боюнча суроолор',
            'Тескери сандар',
            'Калькулятордо бөлчөктөр',
        ],
    },
    {
        # Reference has a 5th sibling here, "Mixed", with no precedent in
        # the menu tree yet - same shape as its 4 siblings (a plain
        # SubSubtopic-level "Даярдалууда" placeholder, not one of the
        # rebuilt-pages GROUPS above), so it's created via
        # 'create_subsubtopics' before the order below is applied.
        'parent_path': ('Сандар', 'Даражалар жана тамырлар'),
        'create_subsubtopics': [
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Даражалар',
            'Тамырларды эсептөө',
            'Бүтүн сандар менен даражалар жана тамырлар боюнча суроолор',
            'Тамырлар менен эсептөөлөр',
            'Аралаш',
        ],
    },
    {
        # Reference order: Place Value & Ordering, Writing as Words,
        # Divisibility Rules, Arithmetic: 1 & 2 Digit, Arithmetic: 2 & 3
        # Digit, Arithmetic: With Decimals, Real-Life, Roman Numerals - all
        # 8 already exist as real menu entries; production also carries an
        # extra "Негиздери" (Introduction) not in the reference at all
        # (invisible to a fresh local dev DB), pruned by the exhaustive
        # order list below like any other leftover.
        'parent_path': ('Сандар', 'Бүтүн сандар'),
        'order': [
            'Бүтүн сандардын орун наркы жана иреттөө',
            'Бүтүн сандарды сөз менен туюнтуу',
            'Бөлүнүү белгилери',
            'Эсептөөлөр: 1 жана 2 орундук',
            'Эсептөөлөр: 2 жана 3 орундук',
            'Эсептөөлөр: ондуктар менен',
            'Турмуштук маселелер',
            'Рим сандарын окуу жана жазуу',
        ],
    },
    {
        # Reference has 8 items - production is missing "Area & Volume
        # Conversion" entirely (not invisible-to-dev-DB this time - it
        # genuinely doesn't exist anywhere yet), created the same way as
        # Даражалар жана тамырлар's missing "Аралаш" sibling above.
        'parent_path': ('Сандар', 'Өлчөмдөр'),
        'create_subsubtopics': [
            {'title': 'Аянт жана көлөм бирдиктерин алмаштыруу', 'slug': 'area-volume-conversion'},
        ],
        'order': [
            'Татаал өлчөмдөр',
            'Сызыктарды өлчөө',
            'Акча',
            'Шкаланы окуу',
            'Масштабдуу сүрөттөр',
            'Өлчөө системалары',
            'Аянт жана көлөм бирдиктерин алмаштыруу',
            'Убакыт',
        ],
    },
    {
        # Reference order: Calculations with Powers of 10, Adding &
        # Subtracting, Multiplying & Dividing, Converting, Correcting -
        # production had Multiplying & Dividing pulled forward to
        # position 2 (sharing a duplicate order value with Adding &
        # Subtracting), an over-qualified title on Adding & Subtracting
        # ("...: калькуляторсуз", not present on the reference or any
        # sibling), and an extra "Негиздери" (Introduction) not in the
        # reference at all (invisible to a fresh local dev DB), pruned by
        # the exhaustive order list below like any other leftover.
        'parent_path': ('Сандар', 'Стандарттык форма'),
        'renames': [
            {
                'from': 'Стандарттык форманы кошуу жана кемитүү: калькулятордсуз',
                'to': 'Кошуу жана кемитүү',
            },
        ],
        'order': [
            '10дун даражалары менен эсептөөлөр',
            'Кошуу жана кемитүү',
            'Көбөйтүү жана бөлүү',
            'Айландыруу',
            'Стандарттык форманы тууралоо',
        ],
    },
    {
        # Reference order (7 items): Compound Measures, Direct & Inverse,
        # Graphs, Percentages: Calculator, Percentages: Non-Calculator,
        # Ratio, Real-Life. Пропорция is itself a root Topic (1-tuple
        # parent_path, see the resolution logic above) - "Ылдамдык,
        # аралык жана убакыт" (Speed, Distance & Time - a specific
        # compound-measure example, not the general label) had 0
        # children, so it's simply renamed to the general "Татаал
        # өлчөмдөр" (Compound Measures) rather than losing any content.
        # "Percentages: Non-Calculator" was originally created via
        # 'create_subsubtopics' (now removed from this entry - it exists
        # in both dev and production now, so re-declaring it here would
        # just try to create a duplicate every run once its title no
        # longer matches). It was created with a typo'd title
        # ("калькулятордсуз") - the 'renames' entry below fixes that on
        # the existing item without touching create_subsubtopics at all,
        # same mechanism as the other 2 renames here.
        # "Айландыруу графиктери" (Conversion Graphs, over-specific) is
        # renamed to the general "Графиктер" (Graphs) for the same
        # reason as Compound Measures above - its own reference submenu
        # has a "Conversion Graphs" child of its own now.
        'parent_path': ('Пропорция',),
        'renames': [
            {'from': 'Ылдамдык, аралык жана убакыт', 'to': 'Татаал өлчөмдөр'},
            {'from': 'Айландыруу графиктери', 'to': 'Графиктер'},
            {'from': 'Пайыздар: калькулятордсуз', 'to': 'Пайыздар: калькуляторсуз'},
        ],
        'order': [
            'Татаал өлчөмдөр',
            'Түз жана тескери пропорция',
            'Графиктер',
            'Пайыздар: калькулятор менен',
            'Пайыздар: калькуляторсуз',
            'Катыш',
            'Турмуштук колдонуулар',
        ],
    },
    {
        # Reference order for Татаал өлчөмдөр's OWN children (8 items):
        # Area & Volume Conversion, Density/Mass/Volume, Work-Hours,
        # Population Density, Pressure/Force/Area, Rates of Pay, Time,
        # Speed/Distance/Time. "Убакыт" (Time) is mirrored in as an 8th
        # item by MIRROR_NODES below, which runs after this loop - so on
        # a from-scratch run this entry's reorder skips it the first
        # time (not created yet) and only fully settles on a second run,
        # same as any other cross-run dependency in this command.
        'parent_path': ('Пропорция', 'Татаал өлчөмдөр'),
        'order': [
            'Аянт жана көлөм бирдиктерин алмаштыруу',
            'Тыгыздык, масса жана көлөм',
            'Жумуш-сааттар',
            'Калктын калыңдыгы',
            'Басым, күч жана аянт',
            'Эмгек акы ставкалары',
            'Убакыт',
            'Ылдамдык, аралык жана убакыт',
        ],
    },
    {
        # Reference has a 5th sibling here, "Mixed", with no precedent in
        # the menu tree yet - same shape as the other "Аралаш" leaf
        # placeholders elsewhere in this file (a plain SubSubtopic-level
        # placeholder, not one of the rebuilt-pages GROUPS above), so it's
        # created via 'create_subsubtopics' before the order below is
        # applied.
        'parent_path': ('Пропорция', 'Пайыздар: калькулятор менен'),
        'create_subsubtopics': [
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Туюнтуу',
            'Чоңдуктун пайызы',
            'Көбөйтүү жана азайтуу',
            'Кайталанма пайыздык өзгөрүү',
            'Аралаш',
        ],
    },
    {
        # "Пайыздар: калькуляторсуз" was created empty (see its own
        # 'create_subsubtopics' entry above, under Пропорция) - reference
        # gives it 5 children (Equivalence, Expressing, Percentage of a
        # Quantity, Increase & Decrease, Mixed), 4 of them chevron-bearing
        # SubSubtopics of their own (reusing the same slugs as their
        # namesake siblings under Пайыздар: калькулятор менен - no global
        # slug uniqueness constraint, same as "Туюнтуу"/expressing already
        # being reused 3x elsewhere) and "Аралаш" a plain leaf placeholder
        # like its Calculator counterpart.
        'parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз'),
        'create_subsubtopics': [
            {'title': 'Барабардык', 'slug': 'equivalence'},
            {'title': 'Туюнтуу', 'slug': 'expressing'},
            {'title': 'Чоңдуктун пайызы', 'slug': 'percentage-of-a-quantity'},
            {'title': 'Көбөйтүү жана азайтуу', 'slug': 'increase-decrease'},
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Барабардык',
            'Туюнтуу',
            'Чоңдуктун пайызы',
            'Көбөйтүү жана азайтуу',
            'Аралаш',
        ],
    },
    {
        # "Катыш" (Ratio) already has its own 4 chevron-bearing children
        # from import_reference_taxonomy.py (Эквиваленттүүлүк, Туюнтуу,
        # Катыштар жана чоңдуктар, Түрлөндүрүү) - reference adds a 5th,
        # "Аралаш" (Mixed), same shape as its Percentages counterparts.
        # Unlike those, this reference "Mixed" itself shows a chevron
        # (its own further children) rather than being a flat leaf - left
        # as an empty placeholder for now, pending a screenshot of its
        # contents.
        'parent_path': ('Пропорция', 'Катыш'),
        'create_subsubtopics': [
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Эквиваленттүүлүк',
            'Туюнтуу',
            'Катыштар жана чоңдуктар',
            'Түрлөндүрүү',
            'Аралаш',
        ],
    },
    {
        # "Турмуштук колдонуулар" (Real-Life) already has 3 chevron-
        # bearing children from import_reference_taxonomy.py (Пайдалуу
        # сатып алуу, Валюта курстары, Рецепттер) - reference adds 2 more:
        # "Баалар" (Prices, 1st) and "Аралаш" (Mixed, 5th), both getting
        # the same Calculator/Non-Calculator shape as their siblings.
        'parent_path': ('Пропорция', 'Турмуштук колдонуулар'),
        'create_subsubtopics': [
            {'title': 'Баалар', 'slug': 'prices'},
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Баалар',
            'Пайдалуу сатып алуу',
            'Валюта курстары',
            'Рецепттер',
            'Аралаш',
        ],
    },
    {
        # Алгебра (root Topic) already had 6 children from the original
        # taxonomy import - reference adds 6 more chevron-bearing
        # siblings: Графиктер: абстракттуу, Графиктер: турмуштук,
        # Барабарсыздыктар, Түрлөндүрүү, Ырааттуулуктар, Коюу.
        # "Туюнтмаларды түзүү" (Forming Expressions) isn't in the
        # reference at all - confirmed with the user to drop it, so it's
        # left out of 'order' below and pruned by this entry's own
        # cleanup step (only the nav entry is removed; its underlying
        # page, if any, is untouched).
        'parent_path': ('Алгебра',),
        'create_subsubtopics': [
            {'title': 'Графиктер: абстракттуу', 'slug': 'graphs-abstract'},
            {'title': 'Графиктер: турмуштук', 'slug': 'graphs-real-life'},
            {'title': 'Барабарсыздыктар', 'slug': 'inequalities'},
            {'title': 'Түрлөндүрүү', 'slug': 'manipulation'},
            {'title': 'Ырааттуулуктар', 'slug': 'sequences'},
            {'title': 'Коюу', 'slug': 'substitution'},
        ],
        'order': [
            'Киришүү',
            'Теңдемелер: сызыктуу',
            'Теңдемелер: квадраттык',
            'Теңдемелер: системасы',
            'Функциялар',
            'Графиктер: абстракттуу',
            'Графиктер: турмуштук',
            'Барабарсыздыктар',
            'Түрлөндүрүү',
            'Ырааттуулуктар',
            'Коюу',
        ],
    },
    {
        # "Туюнтмаларды түзүү" is created here (a fresh chevron-bearing
        # child of Киришүү) before its own GROUPS entry (target_items)
        # can find it - settles on a 2nd run, same cross-run dependency
        # as any other freshly-'create_subsubtopics'-d parent.
        'parent_path': ('Алгебра', 'Киришүү'),
        'create_subsubtopics': [
            {'title': 'Туюнтмаларды түзүү', 'slug': 'forming-expressions'},
        ],
        'order': [
            'Аныктамалар',
            'Белгилөөлөр',
            'Туюнтмаларды түзүү',
            'Формулаларды түрлөндүрүү',
        ],
    },
    {
        # "Функциялар менен" plus 4 more (Түзүү, both Белгисиз бир
        # жагында variants, Белгисиз эки жагында - each pruned as the
        # wrong node type by the GROUPS entry above, then recreated here
        # as proper empty categories) are created before their own
        # GROUPS entries can find them (2-run cross-run dependency). The
        # final order below interleaves these 5 categories and the kept
        # "Кашаа менен" among the 4 flat leaves GROUPS' target_items
        # builds (its own sequential numbering doesn't leave room for
        # 6 categories, so this explicit order fixes the final positions
        # to match the reference exactly). Note: since GROUPS' own
        # target_items always resets those 4 leaves back to its own
        # numbering on every run, this entry's reordering re-fires every
        # run too - cosmetic log noise only, the end state each run is
        # identical and correct, same as Теңдемелер: системасы below.
        'parent_path': ('Алгебра', 'Теңдемелер: сызыктуу'),
        'create_subsubtopics': [
            {'title': 'Функциялар менен', 'slug': 'with-functions'},
            {'title': 'Түзүү', 'slug': 'forming'},
            {'title': 'Белгисиз бир жагында: калькулятор менен', 'slug': 'variable-on-one-side-calculator'},
            {'title': 'Белгисиз бир жагында: калькуляторсуз', 'slug': 'variable-on-one-side-non-calculator'},
            {'title': 'Белгисиз эки жагында', 'slug': 'variable-on-both-sides'},
        ],
        'order': [
            'Түзүү',
            'Белгисиз бир жагында: калькулятор менен',
            'Белгисиз бир жагында: калькуляторсуз',
            'Кашаа менен',
            'Белгисиз эки жагында',
            'Рационалдык',
            'Аралаш',
            'Барабарсыздыктар',
            'Функциялар менен',
            'Белгисиз даражалар менен',
        ],
    },
    {
        # Final order for Теңдемелер: системасы (6 items) - "Жоюу
        # ыкмасы" (kept, chevron-bearing) interleaved among the 5 flat
        # leaves GROUPS' target_items builds.
        'parent_path': ('Алгебра', 'Теңдемелер: системасы'),
        'order': [
            'Түзүү',
            'Жоюу ыкмасы',
            'Алмаштыруу',
            'Аралаш',
            'Графикалык жол менен',
            'Сызыктуу жана сызыктуу эмес',
        ],
    },
]

# The reference site cross-links some groups from two different places
# in the menu tree rather than duplicating their content - e.g. Compound
# Measures is filed under both Сандар > Өлчөмдөр (as a Measures topic)
# and Пропорция (since compound measures are a proportion concept too).
# Each entry here copies an existing GROUPS-built parent's children
# (same title, same url_name - so both locations link to the exact same
# page) into a second parent that has none of its own yet. Matched by
# (parent, title), not url_name, since the point here is to deliberately
# reuse a url_name across two menu locations - the opposite of GROUPS'
# own rule against that.
MIRROR_GROUPS = [
    {
        'parent_path': ('Пропорция', 'Татаал өлчөмдөр'),
        'source_parent_path': ('Сандар', 'Өлчөмдөр', 'Татаал өлчөмдөр'),
    },
    {
        # "Барабардык" (Equivalence) under Пайыздар: калькуляторсуз is
        # the same percentage-equivalence exercise set as Сандар's own
        # top-level Эквиваленттүүлүк > Пайыздарды айландыруу - reuses
        # those same 8 real pages rather than building duplicates.
        # (Reference shows 7 of these 8 plus the 4 FDP-family items
        # mirrored in via MIRROR_NODES below, 11 total - this mirrors the
        # whole existing 8-item set since mirror_children copies a parent
        # wholesale, not a hand-picked subset; the one extra item, "Баары
        # менен"/With All, is harmless bonus practice, not a wrong page.)
        'parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Барабардык'),
        'source_parent_path': ('Сандар', 'Эквиваленттүүлүк', 'Пайыздарды айландыруу'),
    },
    {
        # "Эквиваленттүүлүк" (Equivalence) under Катыш (Ratio) is the same
        # ratio-equivalence exercise set as Сандар's own top-level
        # Эквиваленттүүлүк > Катыштарды айландыруу - reuses those same 6
        # real pages. (Reference shows 5 of these 6 plus FPR/FDPR mirrored
        # in via MIRROR_NODES below, 7 total - same "mirrors the whole
        # existing set, one harmless extra item" reasoning as Барабардык
        # above; the extra item here is "Экөө менен тең"/With Both.)
        'parent_path': ('Пропорция', 'Катыш', 'Эквиваленттүүлүк'),
        'source_parent_path': ('Сандар', 'Эквиваленттүүлүк', 'Катыштарды айландыруу'),
    },
]

# Like MIRROR_GROUPS above, but the mirrored thing is itself a whole
# node with its own children (e.g. "Убакыт"/Time, a Measures topic with
# 5 sub-items), not a flat leaf page - so it needs a new MenuItem of its
# own under the target parent, which then gets its own mirrored children
# one level deeper.
MIRROR_NODES = [
    {
        'target_parent_path': ('Пропорция', 'Татаал өлчөмдөр'),
        'source_path': ('Сандар', 'Өлчөмдөр', 'Убакыт'),
    },
    {
        # The 4 FDP-family items ("FDP", "FDP Ordering", "FPR", "FDPR")
        # already exist as empty placeholder SubSubtopics under Сандар >
        # Эквиваленттүүлүк (siblings of Пайыздарды айландыруу, mirrored
        # above) - mirrored in as their own (still-empty) nodes so both
        # locations share the same underlying SubSubtopic and stay in
        # sync once either one gets real content.
        'target_parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Барабардык'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөк, ондук жана пайыз эквиваленттүүлүгү'),
    },
    {
        'target_parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Барабардык'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөктөрдү, ондуктарды жана пайыздарды иреттөө'),
    },
    {
        'target_parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Барабардык'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөк, пайыз жана катыш эквиваленттүүлүгү'),
    },
    {
        'target_parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Барабардык'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөк, ондук, пайыз жана катыш эквиваленттүүлүгү'),
    },
    {
        # "Converting Fractions" under Пайыздар: калькуляторсуз >
        # Туюнтуу shows a chevron on the reference site (unlike its flat-
        # leaf Calculator-side namesake), matching Сандар >
        # Эквиваленттүүлүк > Бөлчөктөрдү айландыруу's own 10-item
        # structure closely enough to be the same shared content, same
        # reasoning as Барабардык's mirror above.
        'target_parent_path': ('Пропорция', 'Пайыздар: калькуляторсуз', 'Туюнтуу'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөктөрдү айландыруу'),
    },
    {
        # FPR and FDPR (2 of the same 4 FDP-family nodes already mirrored
        # into Барабардык above) also appear under Катыш > Эквиваленттүүлүк
        # - mirrored into this third location too, same underlying
        # SubSubtopics.
        'target_parent_path': ('Пропорция', 'Катыш', 'Эквиваленттүүлүк'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөк, пайыз жана катыш эквиваленттүүлүгү'),
    },
    {
        'target_parent_path': ('Пропорция', 'Катыш', 'Эквиваленттүүлүк'),
        'source_path': ('Сандар', 'Эквиваленттүүлүк', 'Бөлчөк, ондук, пайыз жана катыш эквиваленттүүлүгү'),
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

    def resolve_path(self, path):
        """Looks up a MenuItem by its chain of ancestor titles (any
        length - e.g. a 2-tuple Topic>Subtopic or a 3-tuple Topic>
        Subtopic>SubSubtopic), same ancestor-walk technique as the GROUPS
        loop below. Used by MIRROR_GROUPS/MIRROR_NODES so a mirror target
        or source isn't limited to exactly 2 levels deep."""
        *ancestor_titles, leaf_title = path
        lookup = {'title': leaf_title}
        field = 'parent'
        for ancestor_title in reversed(ancestor_titles):
            lookup[f'{field}__title'] = ancestor_title
            field += '__parent'
        return MenuItem.objects.get(**lookup)

    def mirror_children(self, target_parent, source_parent, extra_protected_titles=(), indent='  '):
        """Recursively mirrors source_parent's children (title + url_name,
        matched by title) into target_parent, descending into any child
        that itself has children (e.g. a GROUPS leaf later promoted to
        its own category via PROMOTE_LEAVES) so the whole subtree stays
        in sync, not just the first level."""
        source_children = list(source_parent.children.all().order_by('order'))
        for child in source_children:
            mirrored, created = MenuItem.objects.get_or_create(
                parent=target_parent, title=child.title,
                defaults={'url_name': child.url_name, 'order': child.order},
            )
            if created:
                self.stdout.write(f'{indent}Mirrored: {child.title} ({child.url_name})')
            elif mirrored.url_name != child.url_name:
                # order is deliberately left alone once created - the
                # target parent can have its own extra siblings (see
                # MIRROR_NODES) needing a different position than the
                # source uses, and CHILD_ORDER_FIXES already owns
                # ordering for this parent.
                mirrored.url_name = child.url_name
                mirrored.save(update_fields=['url_name'])
                self.stdout.write(f'{indent}Updated mirror: {child.title}')
            if child.children.exists():
                self.mirror_children(mirrored, child, indent=indent + '  ')

        source_titles = {child.title for child in source_children}
        protected_titles = source_titles | set(extra_protected_titles)
        for extra in MenuItem.objects.filter(parent=target_parent):
            if extra.title not in protected_titles:
                self.stdout.write(f'{indent}Removed stale mirror "{extra.title}"')
                extra.delete()

    def handle(self, *args, **options):
        for group in GROUPS:
            # Usually a 3-tuple (Topic, Subtopic, Sub-subtopic), but a
            # root Topic's own direct child (e.g. "Түз жана тескери
            # пропорция" straight under Пропорция, no Subtopic level in
            # between) needs a shorter chain - so this walks 'parent__'
            # back however many ancestors are given, same technique as
            # CHILD_ORDER_FIXES's 1-or-2-tuple resolution and
            # PROMOTE_LEAVES's 4-tuple one.
            *ancestor_titles, parent_ss_title = group['parent_path']
            lookup = {'title': parent_ss_title}
            field = 'parent'
            for ancestor_title in reversed(ancestor_titles):
                lookup[f'{field}__title'] = ancestor_title
                field += '__parent'
            self.stdout.write(f'=== {" > ".join(group["parent_path"])} ===')
            try:
                parent_menu = MenuItem.objects.get(**lookup)
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
                # Usually exactly one MenuItem per url_name, but
                # MIRROR_GROUPS below deliberately gives a second row the
                # same url_name under a different parent (two nav
                # locations linking to the one page) - prefer the row
                # already under this parent over crashing on
                # MultipleObjectsReturned, and leave the other parent's
                # copy alone rather than repositioning it here.
                matches = list(MenuItem.objects.filter(url_name=item['url_name']))
                leaf = next((m for m in matches if m.parent_id == parent_menu.id), None) or (
                    matches[0] if matches else None
                )
                if leaf is None:
                    leaf = MenuItem.objects.create(
                        url_name=item['url_name'], title=item['title'], parent=parent_menu, order=order,
                    )
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
            promoted_titles = set(group.get('promoted_titles', []))
            for extra in MenuItem.objects.filter(parent=parent_menu):
                if extra.url_name not in target_url_names and extra.title not in promoted_titles:
                    self.stdout.write(
                        f'  Removed extra menu item "{extra.title}" under this parent '
                        f'(any underlying page/content is untouched).'
                    )
                    extra.delete()

        for promo in PROMOTE_LEAVES:
            *ancestors, leaf_title = promo['leaf_path']
            lookup = {'title': leaf_title}
            field = 'parent'
            for ancestor_title in reversed(ancestors):
                lookup[f'{field}__title'] = ancestor_title
                field += '__parent'
            self.stdout.write(f'=== Promote: {" > ".join(promo["leaf_path"])} ===')
            node = MenuItem.objects.filter(**lookup).first()
            if node is None:
                self.stderr.write(f'  Not found.')
                continue

            if not node.children.exists():
                MenuItem.objects.create(
                    parent=node, title=promo['introduction_title'], url_name=node.url_name, order=1,
                )
                node.url_name = None
                node.save(update_fields=['url_name'])
                self.stdout.write(
                    f'  Promoted to a category; its old page is now "{promo["introduction_title"]}"'
                )

            for order, item in enumerate(promo['new_children'], start=2):
                child, created = MenuItem.objects.get_or_create(
                    parent=node, title=item['title'], defaults={'url_name': item['url_name'], 'order': order},
                )
                if created:
                    self.stdout.write(f'  Created: {item["title"]} ({item["url_name"]})')

        for fix in CHILD_ORDER_FIXES:
            # Usually a 2-tuple (Topic, Subtopic) - the Subtopic sits
            # under a root Topic (e.g. Ондуктар under Сандар), or deeper
            # (e.g. a 3-tuple for a SubSubtopic's own children, resolved
            # via the same title-chain walk as resolve_path). Пропорция
            # is itself a root Topic (no parent), so a 1-tuple means
            # "this title, with no parent at all".
            label = ' > '.join(fix['parent_path'])
            self.stdout.write(f'=== {label} (direct children order) ===')
            try:
                if len(fix['parent_path']) == 1:
                    (subtopic_title,) = fix['parent_path']
                    parent = MenuItem.objects.get(title=subtopic_title, parent__isnull=True)
                else:
                    parent = self.resolve_path(fix['parent_path'])
            except MenuItem.DoesNotExist:
                self.stderr.write(
                    f'  "{label}" not found - '
                    f'run import_reference_taxonomy / fix_number_menu first.'
                )
                continue

            for item in fix.get('create_subsubtopics', []):
                if MenuItem.objects.filter(parent=parent, title=item['title']).exists():
                    continue
                if parent.subtopic_id:
                    # Parent's own children share its one subtopic, each
                    # getting its own SubSubtopic (e.g. Даражалар жана
                    # тамырлар, Өлчөмдөр).
                    new_ss = SubSubtopic.objects.create(
                        subtopic_id=parent.subtopic_id, title=item['title'], slug=item['slug'],
                    )
                    MenuItem.objects.create(
                        parent=parent, title=item['title'], topic=parent.topic,
                        subtopic_id=parent.subtopic_id, subsubtopic=new_ss,
                    )
                else:
                    # Parent is itself a root Topic (e.g. Пропорция) -
                    # each direct child is its own Subtopic, not a
                    # SubSubtopic sharing one.
                    new_subtopic = Subtopic.objects.create(
                        topic=parent.topic, title=item['title'], slug=item['slug'],
                    )
                    MenuItem.objects.create(
                        parent=parent, title=item['title'], topic=parent.topic,
                        subtopic=new_subtopic,
                    )
                self.stdout.write(f'  Created sibling "{item["title"]}" (new Subtopic/SubSubtopic + MenuItem)')

            for rename in fix.get('renames', []):
                child = MenuItem.objects.filter(parent=parent, title__in=[rename['from'], rename['to']]).first()
                if not child:
                    continue
                if child.title != rename['to']:
                    child.title = rename['to']
                    child.save(update_fields=['title'])
                    self.stdout.write(f'  Renamed: "{rename["from"]}" -> "{rename["to"]}"')
                # The MenuItem title is what the nav shows, but the
                # generic topic/subsubtopic page headings read straight
                # from the underlying Subtopic/SubSubtopic - rename
                # whichever one this item actually represents too, so a
                # rename doesn't leave the page itself showing the old
                # title. Checked independently of the block above so a
                # rename applied in an earlier run still gets its
                # underlying title fixed on a later one.
                if child.subsubtopic_id and child.subsubtopic.title != rename['to']:
                    child.subsubtopic.title = rename['to']
                    child.subsubtopic.save(update_fields=['title'])
                    self.stdout.write(f'  Renamed underlying SubSubtopic to "{rename["to"]}"')
                elif child.subtopic_id and not child.subsubtopic_id and child.subtopic.title != rename['to']:
                    child.subtopic.title = rename['to']
                    child.subtopic.save(update_fields=['title'])
                    self.stdout.write(f'  Renamed underlying Subtopic to "{rename["to"]}"')

            for order, title in enumerate(fix['order'], start=1):
                child = MenuItem.objects.filter(parent=parent, title=title).first()
                if not child:
                    continue
                if child.order != order:
                    child.order = order
                    child.save(update_fields=['order'])
                    self.stdout.write(f'  Reordered: {title} -> {order}')

            # A canonical order list is meant to be the exhaustive set of
            # this parent's children, so - same as GROUPS' target_items
            # pruning above - anything else under this parent is a
            # leftover/duplicate (e.g. an old menu entry never seeded by
            # any command in this repo, invisible to a fresh local dev DB,
            # only surfaced by running against production's real, longer-
            # lived menu state). Only the navigation entry is deleted; any
            # underlying page/content is untouched.
            fixed_titles = set(fix['order'])
            for extra in MenuItem.objects.filter(parent=parent):
                if extra.title not in fixed_titles:
                    self.stdout.write(
                        f'  Removed extra menu item "{extra.title}" under this parent '
                        f'(any underlying page/content is untouched).'
                    )
                    extra.delete()

        for mirror in MIRROR_GROUPS:
            label = ' > '.join(mirror['parent_path'])
            self.stdout.write(f'=== Mirror: {label} ===')
            try:
                target_parent = self.resolve_path(mirror['parent_path'])
            except MenuItem.DoesNotExist:
                self.stderr.write(f'  "{label}" not found.')
                continue

            src_label = ' > '.join(mirror['source_parent_path'])
            try:
                source_parent = self.resolve_path(mirror['source_parent_path'])
            except MenuItem.DoesNotExist:
                self.stderr.write(f'  Source "{src_label}" not found.')
                continue

            # Recurses into any child that itself has children (e.g. a
            # GROUPS leaf later promoted to its own category via
            # PROMOTE_LEAVES), so the whole subtree stays mirrored, not
            # just the flat top level. A title also managed by a
            # MIRROR_NODES entry on this same parent (a whole separate
            # mirrored subtree) is protected from this mirror's own
            # pruning.
            node_mirror_titles = {
                node_mirror['source_path'][-1]
                for node_mirror in MIRROR_NODES
                if node_mirror['target_parent_path'] == mirror['parent_path']
            }
            self.mirror_children(target_parent, source_parent, extra_protected_titles=node_mirror_titles)

        for mirror in MIRROR_NODES:
            label = ' > '.join(mirror['target_parent_path'])
            self.stdout.write(f'=== Mirror node: {label} ===')
            try:
                target_parent = self.resolve_path(mirror['target_parent_path'])
            except MenuItem.DoesNotExist:
                self.stderr.write(f'  "{label}" not found.')
                continue

            src_label = ' > '.join(mirror['source_path'])
            try:
                source_node = self.resolve_path(mirror['source_path'])
            except MenuItem.DoesNotExist:
                self.stderr.write(f'  Source "{src_label}" not found.')
                continue

            mirrored_node, created = MenuItem.objects.get_or_create(
                parent=target_parent, title=source_node.title,
                defaults={'order': target_parent.children.count() + 1},
            )
            if created:
                self.stdout.write(f'  Mirrored node: {source_node.title}')

            self.mirror_children(mirrored_node, source_node, indent='    ')

        self.stdout.write(self.style.SUCCESS('Done.'))
