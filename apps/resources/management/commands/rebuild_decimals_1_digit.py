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
        # "Өзгөртүп түзүү" (Manipulation) already exists as a chevron-bearing
        # SubSubtopic under Катыш - it just had no children yet.
        # Reference (4 flat items): 1:n, Comparing Parts, Combining,
        # Changing.
        'parent_path': ('Пропорция', 'Катыш', 'Өзгөртүп түзүү'),
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
        # both still empty. Corrected: further screenshots confirmed
        # "Көбөйтүүчүлөргө ажыратуу: эки кашаа менен" and "b = 0" both
        # have their own chevron children (same misread as Equations:
        # Linear) - removed from target_items, one-time-cleaned via
        # 'displaced_url_names', recreated as categories via
        # CHILD_ORDER_FIXES, protected via 'promoted_titles', each filled
        # by its own dedicated GROUPS entry below. A later screenshot
        # confirmed "c = 0", "Completing the Square", "Quadratic
        # Formula", "Equations with No Solution", "Mixed", "Trial &
        # Improvement", "Iteration", "By Intersection" and
        # "Inequalities" are all flat (no chevron) and this is the
        # complete list. A further screenshot then showed "Рационалдык"
        # (Rational) ALSO has its own chevron children (Without
        # Coefficients, With Coefficients) - same misread again, fixed
        # the same way below.
        'parent_path': ('Алгебра', 'Теңдемелер: квадраттык'),
        'target_items': [
            {'title': 'Түзүү', 'url_name': 'algebra_quadratic_forming'},
            {'title': 'c = 0', 'url_name': 'algebra_quadratic_c_zero'},
            {'title': 'Толук квадратка келтирүү', 'url_name': 'algebra_quadratic_completing_square'},
            {'title': 'Квадраттык теңдеме формуласы', 'url_name': 'algebra_quadratic_formula'},
            {'title': 'Чечими жок теңдемелер', 'url_name': 'algebra_quadratic_no_solution'},
            {'title': 'Аралаш', 'url_name': 'algebra_quadratic_mixed'},
            {'title': 'Сыноо жана жакшыртуу', 'url_name': 'algebra_quadratic_trial_improvement'},
            {'title': 'Кайталануу', 'url_name': 'algebra_quadratic_iteration'},
            {'title': 'Кесилишүү аркылуу', 'url_name': 'algebra_quadratic_by_intersection'},
            {'title': 'Барабарсыздыктар', 'url_name': 'algebra_quadratic_inequalities'},
        ],
        'promoted_titles': [
            'Көбөйтүүчүлөргө ажыратуу: эки кашаа менен', 'b = 0', 'Рационалдык',
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [
            'algebra_quadratic_factorisation_double_brackets',
            'algebra_quadratic_b_zero',
            'algebra_quadratic_rational',
        ],
    },
    {
        # "Көбөйтүүчүлөргө ажыратуу: эки кашаа менен" (Factorisation:
        # Double Brackets) is a fresh chevron-bearing category, created
        # via 'create_subsubtopics' below. Reference (2 items): Without
        # Coefficients, With Coefficients.
        'parent_path': ('Алгебра', 'Теңдемелер: квадраттык', 'Көбөйтүүчүлөргө ажыратуу: эки кашаа менен'),
        'target_items': [
            {'title': 'Коэффициентсиз', 'url_name': 'algebra_quadratic_factorisation_without_coefficients'},
            {'title': 'Коэффициент менен', 'url_name': 'algebra_quadratic_factorisation_with_coefficients'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "b = 0" is a fresh chevron-bearing category, created via
        # 'create_subsubtopics' below. Reference (3 items): Rearranging,
        # Difference of Two Squares, Mixed.
        'parent_path': ('Алгебра', 'Теңдемелер: квадраттык', 'b = 0'),
        'target_items': [
            {'title': 'Кайра жайгаштыруу', 'url_name': 'algebra_quadratic_b_zero_rearranging'},
            {'title': 'Эки квадраттын айырмасы', 'url_name': 'algebra_quadratic_b_zero_difference_of_squares'},
            {'title': 'Аралаш', 'url_name': 'algebra_quadratic_b_zero_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Рационалдык" (Rational) is a fresh chevron-bearing category,
        # created via 'create_subsubtopics' below. Reference (2 items):
        # Without Coefficients, With Coefficients - same pair of titles
        # as Factorisation: Double Brackets above, distinct url_names.
        'parent_path': ('Алгебра', 'Теңдемелер: квадраттык', 'Рационалдык'),
        'target_items': [
            {'title': 'Коэффициентсиз', 'url_name': 'algebra_quadratic_rational_without_coefficients'},
            {'title': 'Коэффициент менен', 'url_name': 'algebra_quadratic_rational_with_coefficients'},
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
        # below. A further screenshot then showed "Сызыктуу жана
        # сызыктуу эмес" (Linear & Non-Linear) ALSO has its own chevron
        # children (Algebraically, Graphically) - same misread as the
        # Quadratic items - removed from target_items, one-time-cleaned
        # via 'displaced_url_names', recreated as a category via
        # CHILD_ORDER_FIXES, protected via 'promoted_titles', filled by
        # its own dedicated GROUPS entry below. The same screenshot
        # finally revealed "Жоюу ыкмасы" (Elimination)'s own children:
        # Without Balancing Coefficients, With Balancing Coefficients,
        # Only Negative Coefficients - filled in by another dedicated
        # GROUPS entry below (no displaced_url_names/promoted_titles
        # needed there since Elimination was already a category).
        'parent_path': ('Алгебра', 'Теңдемелер: системасы'),
        'target_items': [
            {'title': 'Түзүү', 'url_name': 'algebra_simultaneous_forming'},
            {'title': 'Алмаштыруу', 'url_name': 'algebra_simultaneous_substitution'},
            {'title': 'Аралаш', 'url_name': 'algebra_simultaneous_mixed'},
            {'title': 'Графикалык жол менен', 'url_name': 'algebra_simultaneous_graphically'},
        ],
        'promoted_titles': ['Жоюу ыкмасы', 'Сызыктуу жана сызыктуу эмес'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': ['algebra_simultaneous_linear_non_linear'],
    },
    {
        # "Жоюу ыкмасы" (Elimination) is an already-existing category -
        # reference (3 items): Without Balancing Coefficients, With
        # Balancing Coefficients, Only Negative Coefficients.
        'parent_path': ('Алгебра', 'Теңдемелер: системасы', 'Жоюу ыкмасы'),
        'target_items': [
            {'title': 'Коэффициенттерди теңдөөсүз', 'url_name': 'algebra_simultaneous_elimination_without_balancing'},
            {'title': 'Коэффициенттерди теңдөө менен', 'url_name': 'algebra_simultaneous_elimination_with_balancing'},
            {'title': 'Терс коэффициенттер гана', 'url_name': 'algebra_simultaneous_elimination_negative_only'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Сызыктуу жана сызыктуу эмес" (Linear & Non-Linear) is a fresh
        # chevron-bearing category, created via 'create_subsubtopics'
        # below. Reference (2 items): Algebraically, Graphically.
        'parent_path': ('Алгебра', 'Теңдемелер: системасы', 'Сызыктуу жана сызыктуу эмес'),
        'target_items': [
            {'title': 'Алгебралык жол менен', 'url_name': 'algebra_simultaneous_linear_non_linear_algebraically'},
            {'title': 'Графикалык жол менен', 'url_name': 'algebra_simultaneous_linear_non_linear_graphically'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Функциялар" (Functions) was an empty top-level category.
        # Already had 2 chevron-bearing children - "Түзүү" (Forming)
        # and "Маанисин эсептөө" (Evaluating) - both empty, both kept
        # (protected via 'promoted_titles', same as "Жоюу ыкмасы"
        # above). Reference's 3rd item, "IGCSE" (a UK exam board), is
        # flat - localized as "ЖРТ" (the Kyrgyz national exam) since the
        # user asked for it by that name; url_name stays as-is.
        'parent_path': ('Алгебра', 'Функциялар'),
        'target_items': [
            {'title': 'ЖРТ', 'url_name': 'algebra_functions_igcse'},
        ],
        'promoted_titles': ['Түзүү', 'Маанисин эсептөө'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Түзүү" (Forming) under Функциялар is an already-existing
        # category - reference (7 items): Expressions, Simple
        # Functions, Changing the Subject of a Formula, Composite:
        # Linear, Inverse, Composite & Inverse, Composite: With
        # Quadratics.
        'parent_path': ('Алгебра', 'Функциялар', 'Түзүү'),
        'target_items': [
            {'title': 'Туюнтмалар', 'url_name': 'algebra_functions_forming_expressions'},
            {'title': 'Жөнөкөй функциялар', 'url_name': 'algebra_functions_forming_simple_functions'},
            {'title': 'Формуланын өзгөрмөсүн алмаштыруу', 'url_name': 'algebra_functions_forming_changing_subject'},
            {'title': 'Татаал функция: сызыктуу', 'url_name': 'algebra_functions_forming_composite_linear'},
            {'title': 'Тескери функция', 'url_name': 'algebra_functions_forming_inverse'},
            {'title': 'Татаал жана тескери функциялар', 'url_name': 'algebra_functions_forming_composite_inverse'},
            {'title': 'Татаал функция: квадраттык менен', 'url_name': 'algebra_functions_forming_composite_quadratics'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Маанисин эсептөө" (Evaluating) under Функциялар is an
        # already-existing category - reference (10 items): Simple
        # Function Machines, Graphing, With Equations & Sequences,
        # Linear, With Indices, Composite, Inverse, Composite &
        # Inverse, Solving Equations, Iteration.
        'parent_path': ('Алгебра', 'Функциялар', 'Маанисин эсептөө'),
        'target_items': [
            {'title': 'Жөнөкөй функция машиналары', 'url_name': 'algebra_functions_evaluating_simple_machines'},
            {'title': 'Графигин түзүү', 'url_name': 'algebra_functions_evaluating_graphing'},
            {'title': 'Теңдемелер жана ырааттуулуктар менен', 'url_name': 'algebra_functions_evaluating_equations_sequences'},
            {'title': 'Сызыктуу', 'url_name': 'algebra_functions_evaluating_linear'},
            {'title': 'Даражалар менен', 'url_name': 'algebra_functions_evaluating_indices'},
            {'title': 'Татаал функция', 'url_name': 'algebra_functions_evaluating_composite'},
            {'title': 'Тескери функция', 'url_name': 'algebra_functions_evaluating_inverse'},
            {'title': 'Татаал жана тескери функциялар', 'url_name': 'algebra_functions_evaluating_composite_inverse'},
            {'title': 'Теңдемелерди чечүү', 'url_name': 'algebra_functions_evaluating_solving_equations'},
            {'title': 'Кайталануу', 'url_name': 'algebra_functions_evaluating_iteration'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Графиктер: абстракттуу" (Graphs: Abstract) was an empty
        # top-level category. Reference (10 items): Coordinates,
        # Linear: Calculating, Linear: Plotting, Linear: Reading,
        # Linear: Mixed are flat; Quadratic, Circles, Other Non-Linear,
        # Transformations, Differentiation are chevron-bearing
        # categories (created via 'create_subsubtopics' below, left
        # empty pending screenshots of their own contents). Further
        # screenshots then showed "Координаттар" (Coordinates),
        # "Сызыктуу: эсептөө" (Linear: Calculating), "Сызыктуу:
        # чиймелөө" (Linear: Plotting) and "Сызыктуу: окуу" (Linear:
        # Reading) ALL have their own chevron children too - the same
        # misread pattern already fixed for the Equations topics -
        # removed from target_items, one-time-cleaned via
        # 'displaced_url_names', recreated as categories via
        # CHILD_ORDER_FIXES, protected via 'promoted_titles', each
        # filled by its own dedicated GROUPS entry below. "Сызыктуу:
        # окуу"'s reference screenshot was cut off after 4 items
        # (5th row read "Identifying..." with nothing after) - only
        # those 4 are built for now, flagged to the user to confirm the
        # rest.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу'),
        'target_items': [
            {'title': 'Сызыктуу: аралаш', 'url_name': 'algebra_graphs_abstract_linear_mixed'},
        ],
        'promoted_titles': [
            'Квадраттык', 'Тегеректер', 'Башка сызыктуу эмес',
            'Түрлөндүрүүлөр', 'Дифференциалдоо',
            'Координаттар', 'Сызыктуу: эсептөө', 'Сызыктуу: чиймелөө',
            'Сызыктуу: окуу',
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [
            'algebra_graphs_abstract_coordinates',
            'algebra_graphs_abstract_linear_calculating',
            'algebra_graphs_abstract_linear_plotting',
            'algebra_graphs_abstract_linear_reading',
        ],
    },
    {
        # "Координаттар" (Coordinates) is a fresh chevron-bearing
        # category, created via 'create_subsubtopics' below. Reference
        # (6 items, all flat): Reading, Reading & Plotting, Midpoint &
        # Endpoint of a Line, Line Segments & Ratio, Geometric
        # Problems, With Pythagoras.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Координаттар'),
        'target_items': [
            {'title': 'Окуу', 'url_name': 'algebra_graphs_abstract_coordinates_reading'},
            {'title': 'Окуу жана чиймелөө', 'url_name': 'algebra_graphs_abstract_coordinates_reading_plotting'},
            {'title': 'Кесиндинин орто жана учтук чекиттери', 'url_name': 'algebra_graphs_abstract_coordinates_midpoint_endpoint'},
            {'title': 'Кесиндилер жана катыш', 'url_name': 'algebra_graphs_abstract_coordinates_segments_ratio'},
            {'title': 'Геометриялык маселелер', 'url_name': 'algebra_graphs_abstract_coordinates_geometric_problems'},
            {'title': 'Пифагор менен', 'url_name': 'algebra_graphs_abstract_coordinates_with_pythagoras'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Сызыктуу: эсептөө" (Linear: Calculating) is a fresh
        # chevron-bearing category, created via 'create_subsubtopics'
        # below. Reference (10 items): Functions & Graphs, Identifying
        # Gradient & Intercept, Evaluating Coordinates, Evaluating
        # Intersections, Parallel, Perpendicular, Parallel &
        # Perpendicular, Mixed, Identifying Graphs are flat; From
        # Coordinates is a chevron-bearing category left empty pending
        # a screenshot of its own contents.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: эсептөө'),
        'target_items': [
            {'title': 'Функциялар жана графиктер', 'url_name': 'algebra_graphs_abstract_linear_calc_functions_graphs'},
            {'title': 'Кыйшаюусун жана кесилиш чекитин аныктоо', 'url_name': 'algebra_graphs_abstract_linear_calc_gradient_intercept'},
            {'title': 'Координаттарды эсептөө', 'url_name': 'algebra_graphs_abstract_linear_calc_evaluating_coordinates'},
            {'title': 'Кесилишүүлөрдү эсептөө', 'url_name': 'algebra_graphs_abstract_linear_calc_evaluating_intersections'},
            {'title': 'Параллель', 'url_name': 'algebra_graphs_abstract_linear_calc_parallel'},
            {'title': 'Перпендикуляр', 'url_name': 'algebra_graphs_abstract_linear_calc_perpendicular'},
            {'title': 'Параллель жана перпендикуляр', 'url_name': 'algebra_graphs_abstract_linear_calc_parallel_perpendicular'},
            {'title': 'Аралаш', 'url_name': 'algebra_graphs_abstract_linear_calc_mixed'},
            {'title': 'Графиктерди аныктоо', 'url_name': 'algebra_graphs_abstract_linear_calc_identifying_graphs'},
        ],
        'promoted_titles': ['Координаттардан'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Координаттардан" (From Coordinates) under Сызыктуу: эсептөө
        # is a fresh chevron-bearing category, created via
        # 'create_subsubtopics' below. Left empty pending a screenshot
        # of its own contents.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: эсептөө', 'Координаттардан'),
        'target_items': [],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Сызыктуу: чиймелөө" (Linear: Plotting) is a fresh
        # chevron-bearing category, created via 'create_subsubtopics'
        # below. Reference (8 items, all flat): With Functions, With
        # Sequences, Cover-Up Method, Gradient of a Line,
        # Gradient-Intercept Method, Table of Values Method,
        # Inequalities, Simultaneous Equations.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: чиймелөө'),
        'target_items': [
            {'title': 'Функциялар менен', 'url_name': 'algebra_graphs_abstract_linear_plot_with_functions'},
            {'title': 'Ырааттуулуктар менен', 'url_name': 'algebra_graphs_abstract_linear_plot_with_sequences'},
            {'title': 'Жабуу ыкмасы', 'url_name': 'algebra_graphs_abstract_linear_plot_cover_up'},
            {'title': 'Сызыктын кыйшаюусу', 'url_name': 'algebra_graphs_abstract_linear_plot_gradient'},
            {'title': 'Кыйшаюу-кесилиш ыкмасы', 'url_name': 'algebra_graphs_abstract_linear_plot_gradient_intercept_method'},
            {'title': 'Маанилер таблицасы ыкмасы', 'url_name': 'algebra_graphs_abstract_linear_plot_table_of_values'},
            {'title': 'Барабарсыздыктар', 'url_name': 'algebra_graphs_abstract_linear_plot_inequalities'},
            {'title': 'Теңдемелер системасы', 'url_name': 'algebra_graphs_abstract_linear_plot_simultaneous'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Сызыктуу: окуу" (Linear: Reading) is a fresh chevron-bearing
        # category, created via 'create_subsubtopics' below. Reference
        # screenshot was cut off after 4 items (Horizontal & Vertical,
        # Gradient of a Line, Equation of a Line, Evaluating
        # Intersections) - a 5th row read "Identifying..." with nothing
        # after, so only these 4 are built for now. Flagged to the user
        # to confirm the rest.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: окуу'),
        'target_items': [
            {'title': 'Горизонталдык жана вертикалдык', 'url_name': 'algebra_graphs_abstract_linear_read_horizontal_vertical'},
            {'title': 'Сызыктын кыйшаюусу', 'url_name': 'algebra_graphs_abstract_linear_read_gradient'},
            {'title': 'Сызыктын теңдемеси', 'url_name': 'algebra_graphs_abstract_linear_read_equation'},
            {'title': 'Кесилишүүлөрдү эсептөө', 'url_name': 'algebra_graphs_abstract_linear_read_evaluating_intersections'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Квадраттык" (Quadratic) under Графиктер: абстракттуу was
        # already an empty chevron-bearing category (created earlier,
        # see the Algebra-level CHILD_ORDER_FIXES entry above) -
        # reference (5 items, all flat): Plotting, Significant Points,
        # Turning Points by Completing the Square, Solving by
        # Intersection, Simultaneous Equations.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Квадраттык'),
        'target_items': [
            {'title': 'Чиймелөө', 'url_name': 'algebra_graphs_abstract_quadratic_plotting'},
            {'title': 'Маанилүү чекиттер', 'url_name': 'algebra_graphs_abstract_quadratic_significant_points'},
            {'title': 'Толук квадратка келтирүү менен бурулуш чекиттери', 'url_name': 'algebra_graphs_abstract_quadratic_turning_points'},
            {'title': 'Кесилишүү аркылуу чечүү', 'url_name': 'algebra_graphs_abstract_quadratic_solving_by_intersection'},
            {'title': 'Теңдемелер системасы', 'url_name': 'algebra_graphs_abstract_quadratic_simultaneous'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Тегеректер" (Circles) under Графиктер: абстракттуу was
        # already an empty chevron-bearing category - reference (2
        # items, both flat): Equation, Tangent.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Тегеректер'),
        'target_items': [
            {'title': 'Теңдеме', 'url_name': 'algebra_graphs_abstract_circles_equation'},
            {'title': 'Жанама', 'url_name': 'algebra_graphs_abstract_circles_tangent'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Башка сызыктуу эмес" (Other Non-Linear) under Графиктер:
        # абстракттуу was already an empty chevron-bearing category -
        # reference (6 items, all flat): Plotting, Identifying:
        # Non-Linear, Identifying: Proportional, Estimating Gradient,
        # Exponential Functions, Trigonometric Functions.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Башка сызыктуу эмес'),
        'target_items': [
            {'title': 'Чиймелөө', 'url_name': 'algebra_graphs_abstract_other_nonlinear_plotting'},
            {'title': 'Аныктоо: сызыктуу эмес', 'url_name': 'algebra_graphs_abstract_other_nonlinear_identifying_nonlinear'},
            {'title': 'Аныктоо: пропорционалдык', 'url_name': 'algebra_graphs_abstract_other_nonlinear_identifying_proportional'},
            {'title': 'Кыйшаюуну болжолдоо', 'url_name': 'algebra_graphs_abstract_other_nonlinear_estimating_gradient'},
            {'title': 'Көрсөткүчтүү функциялар', 'url_name': 'algebra_graphs_abstract_other_nonlinear_exponential_functions'},
            {'title': 'Тригонометриялык функциялар', 'url_name': 'algebra_graphs_abstract_other_nonlinear_trig_functions'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Түрлөндүрүүлөр" (Transformations) under Графиктер:
        # абстракттуу was already an empty chevron-bearing category -
        # reference (2 items, both flat): GCSE, IGCSE. "IGCSE" was
        # initially kept as a literal exam-board name pending the
        # user's call on whether to localize it like Functions' IGCSE ->
        # ЖРТ - user confirmed the same treatment here, so "IGCSE" ->
        # "ЖРТ" (self-correcting via url_name match); "GCSE" has no
        # Kyrgyz equivalent requested and stays as-is, kept distinct
        # from "ЖРТ" as its own sibling item.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Түрлөндүрүүлөр'),
        'target_items': [
            {'title': 'GCSE', 'url_name': 'algebra_graphs_abstract_transformations_gcse'},
            {'title': 'ЖРТ', 'url_name': 'algebra_graphs_abstract_transformations_igcse'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Графиктер: турмуштук" (Graphs: Real-Life) was an empty
        # top-level category. Reference (9 items): Depth-Time,
        # Volume-Time, Mixed, Mixed: Distance & Velocity are flat;
        # Conversion Graphs, Cost Relationships, Distance-Time:
        # Constant Speeds, Distance-Time: Variable Speeds, Velocity-Time
        # are chevron-bearing categories (created via
        # 'create_subsubtopics' below, left empty pending screenshots of
        # their own contents).
        'parent_path': ('Алгебра', 'Графиктер: турмуштук'),
        'target_items': [
            {'title': 'Тереңдик-Убакыт', 'url_name': 'algebra_graphs_real_life_depth_time'},
            {'title': 'Көлөм-Убакыт', 'url_name': 'algebra_graphs_real_life_volume_time'},
            {'title': 'Аралаш', 'url_name': 'algebra_graphs_real_life_mixed'},
            {'title': 'Аралаш: аралык жана ылдамдык', 'url_name': 'algebra_graphs_real_life_mixed_distance_velocity'},
        ],
        'promoted_titles': [
            'Айландыруу графиктери', 'Баа катыштары',
            'Аралык-Убакыт: турактуу ылдамдык',
            'Аралык-Убакыт: өзгөрмө ылдамдык', 'Ылдамдык-Убакыт',
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Айландыруу графиктери" (Conversion Graphs) under Графиктер:
        # турмуштук was already an empty chevron-bearing category -
        # reference screenshot was cut off after 2 items (Reading,
        # Plotting & Reading) - only these are built for now, flagged
        # to the user to confirm the rest.
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Айландыруу графиктери'),
        'target_items': [
            {'title': 'Окуу', 'url_name': 'algebra_graphs_real_life_conversion_reading'},
            {'title': 'Чиймелөө жана окуу', 'url_name': 'algebra_graphs_real_life_conversion_plotting_reading'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Баа катыштары" (Cost Relationships) under Графиктер:
        # турмуштук was already an empty chevron-bearing category -
        # reference screenshot was cut off after 2 items (Introduction,
        # With Equations) - only these are built for now, flagged to
        # the user to confirm the rest.
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Баа катыштары'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'algebra_graphs_real_life_cost_introduction'},
            {'title': 'Теңдемелер менен', 'url_name': 'algebra_graphs_real_life_cost_with_equations'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Аралык-Убакыт: турактуу ылдамдык" (Distance-Time: Constant
        # Speeds) under Графиктер: турмуштук was already an empty
        # chevron-bearing category - reference screenshot was cut off
        # after 2 items (Reading, Plotting & Reading) - only these are
        # built for now, flagged to the user to confirm the rest.
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Аралык-Убакыт: турактуу ылдамдык'),
        'target_items': [
            {'title': 'Окуу', 'url_name': 'algebra_graphs_real_life_distance_time_constant_reading'},
            {'title': 'Чиймелөө жана окуу', 'url_name': 'algebra_graphs_real_life_distance_time_constant_plotting_reading'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Ылдамдык-Убакыт" (Velocity-Time) under Графиктер: турмуштук
        # was already an empty chevron-bearing category - reference (3
        # items, all flat): Distance, Acceleration, Mixed.
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Ылдамдык-Убакыт'),
        'target_items': [
            {'title': 'Аралык', 'url_name': 'algebra_graphs_real_life_velocity_time_distance'},
            {'title': 'Ылдамдануу', 'url_name': 'algebra_graphs_real_life_velocity_time_acceleration'},
            {'title': 'Аралаш', 'url_name': 'algebra_graphs_real_life_velocity_time_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Барабарсыздыктар" (Inequalities) top-level was an empty
        # category. Reference (4 items): Quadratic, Trial &
        # Improvement are flat; Linear, Graphical are chevron-bearing
        # categories (created via 'create_subsubtopics' below, left
        # empty pending screenshots of their own contents).
        'parent_path': ('Алгебра', 'Барабарсыздыктар'),
        'target_items': [
            {'title': 'Квадраттык', 'url_name': 'algebra_inequalities_quadratic'},
            {'title': 'Сыноо жана жакшыртуу', 'url_name': 'algebra_inequalities_trial_improvement'},
        ],
        'promoted_titles': ['Сызыктуу', 'Графикалык'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Өзгөртүп түзүү" (Manipulation) was an empty top-level category.
        # Reference (11 items): Notation, Changing the Subject of a
        # Formula are flat; Forming Expressions, Algebraic Fractions,
        # Expanding Single Brackets, Expanding Double & Triple
        # Brackets, Factorising into Single Brackets, Factorising into
        # Double Brackets, Proofs, Simplifying Expressions, Mixed are
        # chevron-bearing categories (created via 'create_subsubtopics'
        # below, left empty pending screenshots of their own contents).
        # A further screenshot then showed "Формуланын өзгөрмөсүн
        # алмаштыруу" (Changing the Subject of a Formula) ALSO has its
        # own chevron children - same misread pattern already hit
        # repeatedly - removed from target_items, one-time-cleaned via
        # 'displaced_url_names', recreated as a category via
        # CHILD_ORDER_FIXES, protected via 'promoted_titles', filled by
        # its own dedicated GROUPS entry below. A further screenshot
        # then showed "Белгилөө" (Notation) ALSO has its own chevron
        # children (14 of them) - same misread pattern yet again - same
        # treatment.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү'),
        'target_items': [],
        'promoted_titles': [
            'Туюнтма түзүү', 'Алгебралык бөлчөктөр',
            'Бир кашааны ачуу', 'Эки жана үч кашааны ачуу',
            'Бир кашаага ажыратуу', 'Эки кашаага ажыратуу',
            'Далилдөөлөр', 'Туюнтмаларды жөнөкөйлөтүү', 'Аралаш',
            'Формуланын өзгөрмөсүн алмаштыруу', 'Белгилөө',
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [
            'algebra_manipulation_changing_subject',
            'algebra_manipulation_notation',
        ],
    },
    {
        # "Бир кашаага ажыратуу" (Factorising into Single Brackets)
        # under Өзгөртүп түзүү was already an empty chevron-bearing
        # category - a first screenshot showed only 2 items (Without
        # Indices, With Indices); a fuller screenshot then revealed 2
        # more (With Expanding: Without/With Indices) that had been
        # missed - reference (4 items, all flat): Without Indices, With
        # Indices, With Expanding: Without Indices, With Expanding:
        # With Indices.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Бир кашаага ажыратуу'),
        'target_items': [
            {'title': 'Даражасыз', 'url_name': 'algebra_manipulation_factorise_single_without_indices'},
            {'title': 'Даража менен', 'url_name': 'algebra_manipulation_factorise_single_with_indices'},
            {'title': 'Ачуу менен: даражасыз', 'url_name': 'algebra_manipulation_factorise_single_expanding_without_indices'},
            {'title': 'Ачуу менен: даража менен', 'url_name': 'algebra_manipulation_factorise_single_expanding_with_indices'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Эки кашаага ажыратуу" (Factorising into Double Brackets)
        # under Өзгөртүп түзүү was already an empty chevron-bearing
        # category - reference (7 items, all flat): Quadratic Without
        # Coefficients, Quadratic: With Coefficients, With Expanding,
        # Completing the Square, Difference of Two Squares, Mixed
        # Factorising, Grouping.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Эки кашаага ажыратуу'),
        'target_items': [
            {'title': 'Квадраттык: коэффициентсиз', 'url_name': 'algebra_manipulation_factorise_double_quadratic_without_coefficients'},
            {'title': 'Квадраттык: коэффициент менен', 'url_name': 'algebra_manipulation_factorise_double_quadratic_with_coefficients'},
            {'title': 'Ачуу менен', 'url_name': 'algebra_manipulation_factorise_double_with_expanding'},
            {'title': 'Толук квадратка келтирүү', 'url_name': 'algebra_manipulation_factorise_double_completing_square'},
            {'title': 'Эки квадраттын айырмасы', 'url_name': 'algebra_manipulation_factorise_double_difference_squares'},
            {'title': 'Аралаш ажыратуу', 'url_name': 'algebra_manipulation_factorise_double_mixed'},
            {'title': 'Топтоштуруу', 'url_name': 'algebra_manipulation_factorise_double_grouping'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Аралаш" (Mixed) under Өзгөртүп түзүү was already an empty
        # chevron-bearing category - reference (2 items, both flat):
        # Foundation, Higher (exam-tier labels).
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Аралаш'),
        'target_items': [
            {'title': 'Негизги деңгээл', 'url_name': 'algebra_manipulation_mixed_foundation'},
            {'title': 'Жогорку деңгээл', 'url_name': 'algebra_manipulation_mixed_higher'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Белгилөө" (Notation) is a fresh chevron-bearing category,
        # created via 'create_subsubtopics' below. Reference (14 items,
        # all flat): Adding, Adding: With Brackets, Adding: With
        # Indices, Multiplying, Multiplying & Adding, Dividing,
        # Multiplying & Dividing, Squared & Cubed, Mixed Arithmetic,
        # With Negative & Fractional Indices, Rational: With
        # Factorisation, Rational: Difference of Two Squares, Mixed,
        # Mixed: All.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Белгилөө'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'algebra_manipulation_notation_adding'},
            {'title': 'Кошуу: кашаа менен', 'url_name': 'algebra_manipulation_notation_adding_brackets'},
            {'title': 'Кошуу: даража менен', 'url_name': 'algebra_manipulation_notation_adding_indices'},
            {'title': 'Көбөйтүү', 'url_name': 'algebra_manipulation_notation_multiplying'},
            {'title': 'Көбөйтүү жана кошуу', 'url_name': 'algebra_manipulation_notation_multiplying_adding'},
            {'title': 'Бөлүү', 'url_name': 'algebra_manipulation_notation_dividing'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'algebra_manipulation_notation_multiplying_dividing'},
            {'title': 'Квадрат жана куб', 'url_name': 'algebra_manipulation_notation_squared_cubed'},
            {'title': 'Аралаш арифметика', 'url_name': 'algebra_manipulation_notation_mixed_arithmetic'},
            {'title': 'Терс жана бөлчөк даражалар менен', 'url_name': 'algebra_manipulation_notation_negative_fractional_indices'},
            {'title': 'Рационалдык: көбөйтүүчүлөргө ажыратуу менен', 'url_name': 'algebra_manipulation_notation_rational_with_factorisation'},
            {'title': 'Рационалдык: эки квадраттын айырмасы', 'url_name': 'algebra_manipulation_notation_rational_difference_squares'},
            {'title': 'Аралаш', 'url_name': 'algebra_manipulation_notation_mixed'},
            {'title': 'Аралаш: баары', 'url_name': 'algebra_manipulation_notation_mixed_all'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Сызыктуу" (Linear) under Барабарсыздыктар was already an
        # empty chevron-bearing category - reference (6 items, all
        # flat): Forming, Evaluating, Representing, Solving: Single,
        # Solving: Single & Double, Mixed.
        'parent_path': ('Алгебра', 'Барабарсыздыктар', 'Сызыктуу'),
        'target_items': [
            {'title': 'Түзүү', 'url_name': 'algebra_inequalities_linear_forming'},
            {'title': 'Эсептөө', 'url_name': 'algebra_inequalities_linear_evaluating'},
            {'title': 'Чагылдыруу', 'url_name': 'algebra_inequalities_linear_representing'},
            {'title': 'Чечүү: жалгыз', 'url_name': 'algebra_inequalities_linear_solving_single'},
            {'title': 'Чечүү: жалгыз жана кош', 'url_name': 'algebra_inequalities_linear_solving_single_double'},
            {'title': 'Аралаш', 'url_name': 'algebra_inequalities_linear_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Графикалык" (Graphical) under Барабарсыздыктар was already
        # an empty chevron-bearing category - reference screenshot was
        # cut off after 2 items (Shade Wanted, Shade Unwanted) - only
        # these are built for now, flagged to the user to confirm the
        # rest.
        'parent_path': ('Алгебра', 'Барабарсыздыктар', 'Графикалык'),
        'target_items': [
            {'title': 'Керектүү аймакты боёо', 'url_name': 'algebra_inequalities_graphical_shade_wanted'},
            {'title': 'Керексиз аймакты боёо', 'url_name': 'algebra_inequalities_graphical_shade_unwanted'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Туюнтма түзүү" (Forming Expressions) under Өзгөртүп түзүү was
        # already an empty chevron-bearing category - reference (3
        # items, all flat): With Function Machines, Linear, Quadratic.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Туюнтма түзүү'),
        'target_items': [
            {'title': 'Функция машиналары менен', 'url_name': 'algebra_manipulation_forming_function_machines'},
            {'title': 'Сызыктуу', 'url_name': 'algebra_manipulation_forming_linear'},
            {'title': 'Квадраттык', 'url_name': 'algebra_manipulation_forming_quadratic'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Алгебралык бөлчөктөр" (Algebraic Fractions) under
        # Өзгөртүп түзүү was already an empty chevron-bearing category -
        # reference (6 items, all flat): Adding & Subtracting,
        # Multiplying & Dividing, Mixed, Simplifying, Simplifying: With
        # Factorisation, Simplifying: Difference of Two Squares.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Алгебралык бөлчөктөр'),
        'target_items': [
            {'title': 'Кошуу жана кемитүү', 'url_name': 'algebra_manipulation_fractions_adding_subtracting'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'algebra_manipulation_fractions_multiplying_dividing'},
            {'title': 'Аралаш', 'url_name': 'algebra_manipulation_fractions_mixed'},
            {'title': 'Жөнөкөйлөтүү', 'url_name': 'algebra_manipulation_fractions_simplifying'},
            {'title': 'Жөнөкөйлөтүү: көбөйтүүчүлөргө ажыратуу менен', 'url_name': 'algebra_manipulation_fractions_simplifying_with_factorisation'},
            {'title': 'Жөнөкөйлөтүү: эки квадраттын айырмасы', 'url_name': 'algebra_manipulation_fractions_simplifying_difference_squares'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Формуланын өзгөрмөсүн алмаштыруу" (Changing the Subject of a
        # Formula) is a fresh chevron-bearing category, created via
        # 'create_subsubtopics' below. Reference (4 items, all flat):
        # Manipulating Formulae, Using a Function Machine, Without
        # Factorisation, With Factorisation.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Формуланын өзгөрмөсүн алмаштыруу'),
        'target_items': [
            {'title': 'Формулаларды түрлөндүрүү', 'url_name': 'algebra_manipulation_changing_subject_manipulating_formulae'},
            {'title': 'Функция машинасын колдонуу', 'url_name': 'algebra_manipulation_changing_subject_function_machine'},
            {'title': 'Көбөйтүүчүлөргө ажыратуусуз', 'url_name': 'algebra_manipulation_changing_subject_without_factorisation'},
            {'title': 'Көбөйтүүчүлөргө ажыратуу менен', 'url_name': 'algebra_manipulation_changing_subject_with_factorisation'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Бир кашааны ачуу" (Expanding Single Brackets) under
        # Өзгөртүп түзүү was already an empty chevron-bearing category -
        # reference (7 items, all flat): Without Coefficients, With
        # Coefficients, With Indices, Multiple, Mixed, With
        # Factorisation: Without Indices, With Factorisation: With
        # Indices.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Бир кашааны ачуу'),
        'target_items': [
            {'title': 'Коэффициентсиз', 'url_name': 'algebra_manipulation_expand_single_without_coefficients'},
            {'title': 'Коэффициент менен', 'url_name': 'algebra_manipulation_expand_single_with_coefficients'},
            {'title': 'Даражалар менен', 'url_name': 'algebra_manipulation_expand_single_with_indices'},
            {'title': 'Көп кашаалар', 'url_name': 'algebra_manipulation_expand_single_multiple'},
            {'title': 'Аралаш', 'url_name': 'algebra_manipulation_expand_single_mixed'},
            {'title': 'Көбөйтүүчүлөргө ажыратуу менен: даражасыз', 'url_name': 'algebra_manipulation_expand_single_factorisation_without_indices'},
            {'title': 'Көбөйтүүчүлөргө ажыратуу менен: даража менен', 'url_name': 'algebra_manipulation_expand_single_factorisation_with_indices'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Эки жана үч кашааны ачуу" (Expanding Double & Triple
        # Brackets) under Өзгөртүп түзүү was already an empty
        # chevron-bearing category - reference (7 items, all flat):
        # Double: Without Coefficients, Double: With Coefficients, With
        # Factorisation, Squares, Triple, Mixed Expanding, With Surds.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Эки жана үч кашааны ачуу'),
        'target_items': [
            {'title': 'Эки кашаа: коэффициентсиз', 'url_name': 'algebra_manipulation_expand_double_triple_double_without_coefficients'},
            {'title': 'Эки кашаа: коэффициент менен', 'url_name': 'algebra_manipulation_expand_double_triple_double_with_coefficients'},
            {'title': 'Көбөйтүүчүлөргө ажыратуу менен', 'url_name': 'algebra_manipulation_expand_double_triple_with_factorisation'},
            {'title': 'Квадраттар', 'url_name': 'algebra_manipulation_expand_double_triple_squares'},
            {'title': 'Үч кашаа', 'url_name': 'algebra_manipulation_expand_double_triple_triple'},
            {'title': 'Аралаш ачуу', 'url_name': 'algebra_manipulation_expand_double_triple_mixed'},
            {'title': 'Тамырлар менен', 'url_name': 'algebra_manipulation_expand_double_triple_with_surds'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Ырааттуулуктар" (Sequences) was an empty top-level category.
        # Reference (10 items): Introduction, With Graphs, With
        # Equations & Functions, Quadratic, Linear & Quadratic,
        # Geometric, Fibonacci, Special, Mixed are flat; Linear is a
        # chevron-bearing category (created via 'create_subsubtopics'
        # below, left empty pending a screenshot of its own contents).
        'parent_path': ('Алгебра', 'Ырааттуулуктар'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'algebra_sequences_introduction'},
            {'title': 'Графиктер менен', 'url_name': 'algebra_sequences_with_graphs'},
            {'title': 'Теңдемелер жана функциялар менен', 'url_name': 'algebra_sequences_equations_functions'},
            {'title': 'Квадраттык', 'url_name': 'algebra_sequences_quadratic'},
            {'title': 'Сызыктуу жана квадраттык', 'url_name': 'algebra_sequences_linear_quadratic'},
            {'title': 'Геометриялык', 'url_name': 'algebra_sequences_geometric'},
            {'title': 'Фибоначчи', 'url_name': 'algebra_sequences_fibonacci'},
            {'title': 'Атайын', 'url_name': 'algebra_sequences_special'},
            {'title': 'Аралаш', 'url_name': 'algebra_sequences_mixed'},
        ],
        'promoted_titles': ['Сызыктуу'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Сызыктуу" (Linear) under Ырааттуулуктар was already an empty
        # chevron-bearing category - reference (4 items, all flat):
        # Introduction, Evaluating Terms, From 2 Terms, Summing
        # (IGCSE) - "IGCSE" localized to "ЖРТ" per the user's standing
        # request.
        'parent_path': ('Алгебра', 'Ырааттуулуктар', 'Сызыктуу'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'algebra_sequences_linear_introduction'},
            {'title': 'Мүчөлөрдү эсептөө', 'url_name': 'algebra_sequences_linear_evaluating_terms'},
            {'title': '2 мүчөдөн', 'url_name': 'algebra_sequences_linear_from_2_terms'},
            {'title': 'Суммалоо (ЖРТ)', 'url_name': 'algebra_sequences_linear_summing'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Туюнтмаларды жөнөкөйлөтүү" (Simplifying Expressions) under
        # Өзгөртүп түзүү was an empty flat leaf - reference (13 items,
        # all flat): Adding, Adding: With Brackets, Adding: With
        # Indices, Multiplying, Multiplying & Adding, Dividing,
        # Multiplying & Dividing, Squared & Cubed, Mixed Arithmetic,
        # With Negative & Fractional Indices, Rational: With
        # Factorisation, Rational: Difference of Two Squares, Mixed:
        # All. Near-identical item set to Белгилөө (Notation, see
        # above) minus its extra plain "Mixed" item - distinct
        # url_names since these are separate pages, not a mirror.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Туюнтмаларды жөнөкөйлөтүү'),
        'target_items': [
            {'title': 'Кошуу', 'url_name': 'algebra_manipulation_expressions_adding'},
            {'title': 'Кошуу: кашаа менен', 'url_name': 'algebra_manipulation_expressions_adding_brackets'},
            {'title': 'Кошуу: даража менен', 'url_name': 'algebra_manipulation_expressions_adding_indices'},
            {'title': 'Көбөйтүү', 'url_name': 'algebra_manipulation_expressions_multiplying'},
            {'title': 'Көбөйтүү жана кошуу', 'url_name': 'algebra_manipulation_expressions_multiplying_adding'},
            {'title': 'Бөлүү', 'url_name': 'algebra_manipulation_expressions_dividing'},
            {'title': 'Көбөйтүү жана бөлүү', 'url_name': 'algebra_manipulation_expressions_multiplying_dividing'},
            {'title': 'Квадрат жана куб', 'url_name': 'algebra_manipulation_expressions_squared_cubed'},
            {'title': 'Аралаш арифметика', 'url_name': 'algebra_manipulation_expressions_mixed_arithmetic'},
            {'title': 'Терс жана бөлчөк даражалар менен', 'url_name': 'algebra_manipulation_expressions_negative_fractional_indices'},
            {'title': 'Рационалдык: көбөйтүүчүлөргө ажыратуу менен', 'url_name': 'algebra_manipulation_expressions_rational_with_factorisation'},
            {'title': 'Рационалдык: эки квадраттын айырмасы', 'url_name': 'algebra_manipulation_expressions_rational_difference_squares'},
            {'title': 'Аралаш: баары', 'url_name': 'algebra_manipulation_expressions_mixed_all'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Ордуна коюу" (Substitution, renamed from "Коюу" per the
        # user's request - see the Algebra-root CHILD_ORDER_FIXES entry
        # below) was an empty top-level category. Reference (5 items):
        # With a Calculator, Vectors are flat; Using Symbols, Without
        # Indices, With Indices are chevron-bearing categories (created
        # via 'create_subsubtopics' below, left empty pending
        # screenshots of their own contents).
        'parent_path': ('Алгебра', 'Ордуна коюу'),
        'target_items': [
            {'title': 'Калькулятор менен', 'url_name': 'algebra_substitution_with_calculator'},
            {'title': 'Векторлор', 'url_name': 'algebra_substitution_vectors'},
        ],
        'promoted_titles': ['Белгилерди колдонуу', 'Даражасыз', 'Даража менен'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Белгилерди колдонуу" (Using Symbols) under Ордуна коюу was an
        # empty chevron-bearing category - reference (3 items, all
        # flat): Positive, Negative, Mixed. Same shape repeats for its 2
        # siblings below (Даражасыз/Without Indices, Даража менен/With
        # Indices) - "Mixed" carries the reference site's own mirror
        # icon there, since all 3 categories reuse the exact same Mixed
        # page. This entry builds the canonical copy; the other 2 pick
        # it up via MIRROR_LEAVES below instead of repeating it here -
        # GROUPS' target_items can't safely share one url_name across
        # sibling entries in the same run (whichever entry runs last
        # would "steal" the single row via the url_name-reuse fallback
        # a few lines above, since there's no existing row under the
        # earlier entries' parents yet to prefer).
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Белгилерди колдонуу'),
        'target_items': [
            {'title': 'Оң', 'url_name': 'algebra_substitution_symbols_positive'},
            {'title': 'Терс', 'url_name': 'algebra_substitution_symbols_negative'},
            {'title': 'Аралаш', 'url_name': 'algebra_substitution_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Даражасыз" (Without Indices) under Ордуна коюу - same shape
        # as Белгилерди колдонуу above, own distinct Positive/Negative;
        # "Аралаш" is protected from this entry's own pruning via
        # 'promoted_titles' and supplied by MIRROR_LEAVES below instead.
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Даражасыз'),
        'target_items': [
            {'title': 'Оң', 'url_name': 'algebra_substitution_without_indices_positive'},
            {'title': 'Терс', 'url_name': 'algebra_substitution_without_indices_negative'},
        ],
        'promoted_titles': ['Аралаш'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Даража менен" (With Indices) under Ордуна коюу - same shape
        # as its 2 siblings above; "Аралаш" handled the same way.
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Даража менен'),
        'target_items': [
            {'title': 'Оң', 'url_name': 'algebra_substitution_with_indices_positive'},
            {'title': 'Терс', 'url_name': 'algebra_substitution_with_indices_negative'},
        ],
        'promoted_titles': ['Аралаш'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Бурч фактылары" (Angle Facts) under Геометрия > Бурчтар is a
        # fresh chevron-bearing category, created via
        # 'create_subsubtopics' in CHILD_ORDER_FIXES below (first run
        # reports "not found" here, second run succeeds - the usual
        # cross-run dependency for a parent created in the same
        # command execution). Reference (6 items, all flat): Vocabulary,
        # Around a Point, On Straight Lines, Vertically Opposite,
        # Triangles, Mixed.
        'parent_path': ('Геометрия', 'Бурчтар', 'Бурч фактылары'),
        'target_items': [
            {'title': 'Терминология', 'url_name': 'geometry_angles_angle_facts_vocabulary'},
            {'title': 'Чекиттин тегерегинде', 'url_name': 'geometry_angles_angle_facts_around_a_point'},
            {'title': 'Түз сызыктарда', 'url_name': 'geometry_angles_angle_facts_on_straight_lines'},
            {'title': 'Вертикаль бурчтар', 'url_name': 'geometry_angles_angle_facts_vertically_opposite'},
            {'title': 'Үч бурчтуктар', 'url_name': 'geometry_angles_angle_facts_triangles'},
            {'title': 'Аралаш', 'url_name': 'geometry_angles_angle_facts_mixed'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Чийүү жана өлчөө" (Drawing & Measuring) under Геометрия >
        # Бурчтар - same cross-run dependency as Бурч фактылары above.
        # Reference (4 items, all flat): Drawing, Measuring, Drawing &
        # Measuring, Estimating - the 3rd item repeats the parent's own
        # name verbatim on the reference site (a combined-skill drill
        # alongside the 2 standalone ones), kept faithfully as shown.
        'parent_path': ('Геометрия', 'Бурчтар', 'Чийүү жана өлчөө'),
        'target_items': [
            {'title': 'Чийүү', 'url_name': 'geometry_angles_drawing_measuring_drawing'},
            {'title': 'Өлчөө', 'url_name': 'geometry_angles_drawing_measuring_measuring'},
            {'title': 'Чийүү жана өлчөө', 'url_name': 'geometry_angles_drawing_measuring_both'},
            {'title': 'Болжолдоо', 'url_name': 'geometry_angles_drawing_measuring_estimating'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Тегерек теоремалары" (Circle Theorems) under Геометрия >
        # Бурчтар - same cross-run dependency as its 2 siblings above.
        # Reference (10 items, all flat): Vocabulary, Alternate Segment,
        # At the Circumference, Cyclic Quadrilaterals, Tangents &
        # Chords, Combined, Mixed, With Pythagoras, With Trigonometry,
        # Intersecting Chords (IGCSE) - "IGCSE" localized to "ЖРТ" per
        # the user's standing request.
        'parent_path': ('Геометрия', 'Бурчтар', 'Тегерек теоремалары'),
        'target_items': [
            {'title': 'Терминология', 'url_name': 'geometry_angles_circle_theorems_vocabulary'},
            {'title': 'Алмашма сегмент', 'url_name': 'geometry_angles_circle_theorems_alternate_segment'},
            {'title': 'Тегеректин четинде', 'url_name': 'geometry_angles_circle_theorems_at_circumference'},
            {'title': 'Циклдик төрт бурчтуктар', 'url_name': 'geometry_angles_circle_theorems_cyclic_quadrilaterals'},
            {'title': 'Жанамалар жана хордалар', 'url_name': 'geometry_angles_circle_theorems_tangents_chords'},
            {'title': 'Айкалышкан', 'url_name': 'geometry_angles_circle_theorems_combined'},
            {'title': 'Аралаш', 'url_name': 'geometry_angles_circle_theorems_mixed'},
            {'title': 'Пифагор менен', 'url_name': 'geometry_angles_circle_theorems_with_pythagoras'},
            {'title': 'Тригонометрия менен', 'url_name': 'geometry_angles_circle_theorems_with_trigonometry'},
            {'title': 'Кесилишкен хордалар (ЖРТ)', 'url_name': 'geometry_angles_circle_theorems_intersecting_chords'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Параллель сызыктар" (Parallel Lines) under Геометрия >
        # Бурчтар was already an empty chevron-bearing category (kept
        # from the old import - see the Бурчтар entry above). Reference
        # screenshot was cut off after 2 items (Introduction, Solving
        # Equations) - only these are built for now, flagged to the
        # user to confirm the rest.
        'parent_path': ('Геометрия', 'Бурчтар', 'Параллель сызыктар'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'geometry_angles_parallel_lines_introduction'},
            {'title': 'Теңдемелерди чечүү', 'url_name': 'geometry_angles_parallel_lines_solving_equations'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Көп бурчтуктар" (Polygons) under Геометрия > Бурчтар was
        # already an empty chevron-bearing category. Reference (6
        # items): Triangles, Quadrilaterals, Special Quadrilaterals,
        # Regular, Irregular are flat; "Mixed" is itself a
        # chevron-bearing category (2 children of its own, shown on the
        # reference with the same mirror-arrow icon used elsewhere in
        # this file - but unlike those cases this one isn't shared with
        # any sibling, it's just this Polygons-specific Mixed page) -
        # created via 'create_subsubtopics' below, filled in by the
        # next GROUPS entry.
        'parent_path': ('Геометрия', 'Бурчтар', 'Көп бурчтуктар'),
        'target_items': [
            {'title': 'Үч бурчтуктар', 'url_name': 'geometry_angles_polygons_triangles'},
            {'title': 'Төрт бурчтуктар', 'url_name': 'geometry_angles_polygons_quadrilaterals'},
            {'title': 'Атайын төрт бурчтуктар', 'url_name': 'geometry_angles_polygons_special_quadrilaterals'},
            {'title': 'Туура', 'url_name': 'geometry_angles_polygons_regular'},
            {'title': 'Туура эмес', 'url_name': 'geometry_angles_polygons_irregular'},
        ],
        'promoted_titles': ['Аралаш'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Аралаш" (Mixed) under Көп бурчтуктар - created via
        # 'create_subsubtopics' in CHILD_ORDER_FIXES below (first run
        # reports "not found" here, second run succeeds). Reference (2
        # items, both flat): Without Circle Theorems, With Circle
        # Theorems.
        'parent_path': ('Геометрия', 'Бурчтар', 'Көп бурчтуктар', 'Аралаш'),
        'target_items': [
            {'title': 'Тегерек теоремаларысыз', 'url_name': 'geometry_angles_polygons_mixed_without_circle_theorems'},
            {'title': 'Тегерек теоремалары менен', 'url_name': 'geometry_angles_polygons_mixed_with_circle_theorems'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Азимут" (Bearings) under Геометрия was an empty top-level
        # category. Reference (5 items, all flat): Cardinal Points,
        # Measuring, With Scale Drawings, Calculating, With
        # Trigonometry.
        'parent_path': ('Геометрия', 'Азимут'),
        'target_items': [
            {'title': 'Негизги багыттар', 'url_name': 'geometry_bearings_cardinal_points'},
            {'title': 'Өлчөө', 'url_name': 'geometry_bearings_measuring'},
            {'title': 'Масштабдуу сүрөт менен', 'url_name': 'geometry_bearings_with_scale_drawings'},
            {'title': 'Эсептөө', 'url_name': 'geometry_bearings_calculating'},
            {'title': 'Тригонометрия менен', 'url_name': 'geometry_bearings_with_trigonometry'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Координаттар" (Coordinates) under Геометрия was an empty
        # top-level category. Reference (6 items, all flat): Reading,
        # Reading & Plotting, Midpoint & Endpoint of a Line, Line
        # Segments & Ratio, Geometric Problems, With Pythagoras.
        'parent_path': ('Геометрия', 'Координаттар'),
        'target_items': [
            {'title': 'Окуу', 'url_name': 'geometry_coordinates_reading'},
            {'title': 'Окуу жана белгилөө', 'url_name': 'geometry_coordinates_reading_plotting'},
            {'title': 'Кесиндинин орто жана чеки чекиттери', 'url_name': 'geometry_coordinates_midpoint_endpoint'},
            {'title': 'Кесиндилер жана катыш', 'url_name': 'geometry_coordinates_line_segments_ratio'},
            {'title': 'Геометриялык маселелер', 'url_name': 'geometry_coordinates_geometric_problems'},
            {'title': 'Пифагор менен', 'url_name': 'geometry_coordinates_with_pythagoras'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Пифагор" (Pythagoras) under Геометрия was an empty top-level
        # category. Reference (12 items): Introduction, Finding A or B,
        # Finding A/B/C, Isosceles Triangles, Real-Life, 3D,
        # Coordinates, Mixed, Shape Perimeters, With Surds, With Circle
        # Theorems are flat; "With Trigonometry" is itself a
        # chevron-bearing category (created via 'create_subsubtopics'
        # below, left empty pending its own screenshot).
        'parent_path': ('Геометрия', 'Пифагор'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'geometry_pythagoras_introduction'},
            {'title': 'A же B табуу', 'url_name': 'geometry_pythagoras_finding_a_or_b'},
            {'title': 'A, B же C табуу', 'url_name': 'geometry_pythagoras_finding_a_b_or_c'},
            {'title': 'Тең бүйрүүчү үч бурчтуктар', 'url_name': 'geometry_pythagoras_isosceles_triangles'},
            {'title': 'Турмуштук маселелер', 'url_name': 'geometry_pythagoras_real_life'},
            {'title': '3D', 'url_name': 'geometry_pythagoras_3d'},
            {'title': 'Координаттар', 'url_name': 'geometry_pythagoras_coordinates'},
            {'title': 'Аралаш', 'url_name': 'geometry_pythagoras_mixed'},
            {'title': 'Фигуралардын периметрлери', 'url_name': 'geometry_pythagoras_shape_perimeters'},
            {'title': 'Тамырлар менен', 'url_name': 'geometry_pythagoras_with_surds'},
            {'title': 'Тегерек теоремалары менен', 'url_name': 'geometry_pythagoras_with_circle_theorems'},
        ],
        'promoted_titles': ['Тригонометрия менен'],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Окшоштук" (Similarity) under Геометрия was an empty
        # top-level category. Reference screenshot clearly showed 4
        # items (all flat): Similar 2D Shapes, Similar Triangles,
        # Congruent Triangles, Length/Area/Volume Scale Factors - a 5th
        # row ("Area & Volume Conversion") appeared above these at the
        # same row position as Measures' own matching item one
        # screenshot earlier, which doesn't fit this topic at all and
        # is very likely a stale render artifact from the previous
        # hover rather than a genuine child - left out, flagged to the
        # user to confirm.
        'parent_path': ('Геометрия', 'Окшоштук'),
        'target_items': [
            {'title': 'Окшош 2D фигуралар', 'url_name': 'geometry_similarity_similar_2d_shapes'},
            {'title': 'Окшош үч бурчтуктар', 'url_name': 'geometry_similarity_similar_triangles'},
            {'title': 'Тең үч бурчтуктар', 'url_name': 'geometry_similarity_congruent_triangles'},
            {'title': 'Узундук, аянт жана көлөм масштаб көбөйткүчтөрү', 'url_name': 'geometry_similarity_length_area_volume_scale_factors'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Тригонометрия" (Trigonometry) under Геометрия was an empty
        # top-level category. Reference (13 items): Introduction,
        # Graphs, Choosing a Ratio, Isosceles Triangles, Without a
        # Calculator, With Circle Theorems, Area Rule are flat; Sine &
        # Cosine Ratios, Tangent Ratio, All Ratios, Real-Life, With
        # Pythagoras, Sine & Cosine Rules are chevron-bearing categories
        # (created via 'create_subsubtopics' below, left empty pending
        # their own screenshots).
        'parent_path': ('Геометрия', 'Тригонометрия'),
        'target_items': [
            {'title': 'Киришүү', 'url_name': 'geometry_trigonometry_introduction'},
            {'title': 'Графиктер', 'url_name': 'geometry_trigonometry_graphs'},
            {'title': 'Катышты тандоо', 'url_name': 'geometry_trigonometry_choosing_a_ratio'},
            {'title': 'Тең бүйрүүчү үч бурчтуктар', 'url_name': 'geometry_trigonometry_isosceles_triangles'},
            {'title': 'Калькуляторсуз', 'url_name': 'geometry_trigonometry_without_calculator'},
            {'title': 'Тегерек теоремалары менен', 'url_name': 'geometry_trigonometry_with_circle_theorems'},
            {'title': 'Аянт эрежеси', 'url_name': 'geometry_trigonometry_area_rule'},
        ],
        'promoted_titles': [
            'Синус жана косинус катыштары',
            'Тангенс катышы',
            'Бардык катыштар',
            'Турмуштук маселелер',
            'Пифагор менен',
            'Синус жана косинус эрежелери',
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Векторлор" (Vectors) under Геометрия carried 2 children
        # ("Векторлор менен эсептөөлөр", "Векторлук геометрия") from the
        # old coarser import (see the Геометрия root entry far above) -
        # neither matches the new reference's 5-item flat list at all
        # (0 resources attached to either), pruned by GROUPS' own
        # exhaustive target_items set below like any other leftover.
        # Reference (5 items, all flat): Translation, Expressing,
        # Substitution, Around Shapes, Proofs.
        'parent_path': ('Геометрия', 'Векторлор'),
        'target_items': [
            {'title': 'Жылдыруу', 'url_name': 'geometry_vectors_translation'},
            {'title': 'Туюнтуу', 'url_name': 'geometry_vectors_expressing'},
            {'title': 'Коюу', 'url_name': 'geometry_vectors_substitution'},
            {'title': 'Фигуралардын тегерегинде', 'url_name': 'geometry_vectors_around_shapes'},
            {'title': 'Далилдөөлөр', 'url_name': 'geometry_vectors_proofs'},
        ],
        'stale_subsubtopic_titles': [],
        'displaced_url_names': [],
    },
    {
        # "Көлөм жана бет аянты" (Volume & Surface Area) under Геометрия
        # was an empty top-level category. Reference (12 items):
        # Vocabulary, Introduction to Volume, Nets are flat; Cone,
        # Cuboid, Cylinder, Prism, Cylinder & Prism, Frustum, Pyramid,
        # Sphere, Mixed are chevron-bearing categories (created via
        # 'create_subsubtopics' below, left empty pending their own
        # screenshots).
        'parent_path': ('Геометрия', 'Көлөм жана бет аянты'),
        'target_items': [
            {'title': 'Терминология', 'url_name': 'geometry_volume_surface_area_vocabulary'},
            {'title': 'Көлөмгө киришүү', 'url_name': 'geometry_volume_surface_area_introduction_to_volume'},
            {'title': 'Жайылмалар', 'url_name': 'geometry_volume_surface_area_nets'},
        ],
        'promoted_titles': [
            'Конус',
            'Параллелепипед',
            'Цилиндр',
            'Призма',
            'Цилиндр жана призма',
            'Кесилген конус',
            'Пирамида',
            'Сфера',
            'Аралаш',
        ],
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
        # Катыштар жана чоңдуктар, Өзгөртүп түзүү) - reference adds a 5th,
        # "Аралаш" (Mixed), same shape as its Percentages counterparts.
        # Unlike those, this reference "Mixed" itself shows a chevron
        # (its own further children) rather than being a flat leaf - left
        # as an empty placeholder for now, pending a screenshot of its
        # contents. "Түрлөндүрүү" (created by import_reference_taxonomy.py
        # under its old name) has been renamed to "Өзгөртүп түзүү" per the
        # user's request - Kazakh terminology that gets confused with
        # Kyrgyz in this context.
        'parent_path': ('Пропорция', 'Катыш'),
        'create_subsubtopics': [
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'renames': [
            {'from': 'Түрлөндүрүү', 'to': 'Өзгөртүп түзүү'},
        ],
        'order': [
            'Эквиваленттүүлүк',
            'Туюнтуу',
            'Катыштар жана чоңдуктар',
            'Өзгөртүп түзүү',
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
        # Барабарсыздыктар, Өзгөртүп түзүү, Ырааттуулуктар, Коюу.
        # "Туюнтмаларды түзүү" (Forming Expressions) isn't in the
        # reference at all - confirmed with the user to drop it, so it's
        # left out of 'order' below and pruned by this entry's own
        # cleanup step (only the nav entry is removed; its underlying
        # page, if any, is untouched). "Коюу" (Substitution) has since
        # been renamed to "Ордуна коюу" per the user's request - removed
        # from 'create_subsubtopics' now that it exists in both dev and
        # production (re-declaring it here would just create a
        # duplicate every run once its title no longer matches, same
        # reasoning as "Percentages: Non-Calculator" below), fixed via
        # the 'renames' entry instead. "Түрлөндүрүү" (Manipulation) has
        # likewise been renamed to "Өзгөртүп түзүү" per the user's
        # request - "Түрлөндүрүү" is Kazakh terminology that gets
        # confused with Kyrgyz in this context - same
        # removed-from-create_subsubtopics + renames-entry treatment.
        'parent_path': ('Алгебра',),
        'create_subsubtopics': [
            {'title': 'Графиктер: абстракттуу', 'slug': 'graphs-abstract'},
            {'title': 'Графиктер: турмуштук', 'slug': 'graphs-real-life'},
            {'title': 'Барабарсыздыктар', 'slug': 'inequalities'},
            {'title': 'Ырааттуулуктар', 'slug': 'sequences'},
        ],
        'renames': [
            {'from': 'Коюу', 'to': 'Ордуна коюу'},
            {'from': 'Түрлөндүрүү', 'to': 'Өзгөртүп түзүү'},
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
            'Өзгөртүп түзүү',
            'Ырааттуулуктар',
            'Ордуна коюу',
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
        # "Көбөйтүүчүлөргө ажыратуу: эки кашаа менен", "b = 0" and
        # "Рационалдык" are created here (fresh chevron-bearing
        # categories) before their own GROUPS entries can find them -
        # 2-run cross-run dependency, same as Теңдемелер: сызыктуу
        # above. The final order below interleaves them among the 10
        # flat leaves GROUPS' target_items builds (same cosmetic
        # every-run reorder noise as Теңдемелер: сызыктуу - the end
        # state each run is identical and correct).
        'parent_path': ('Алгебра', 'Теңдемелер: квадраттык'),
        'create_subsubtopics': [
            {'title': 'Көбөйтүүчүлөргө ажыратуу: эки кашаа менен', 'slug': 'factorisation-double-brackets'},
            {'title': 'b = 0', 'slug': 'b-equals-0'},
            {'title': 'Рационалдык', 'slug': 'rational'},
        ],
        'order': [
            'Түзүү',
            'Көбөйтүүчүлөргө ажыратуу: эки кашаа менен',
            'b = 0',
            'c = 0',
            'Толук квадратка келтирүү',
            'Рационалдык',
            'Квадраттык теңдеме формуласы',
            'Чечими жок теңдемелер',
            'Аралаш',
            'Сыноо жана жакшыртуу',
            'Кайталануу',
            'Кесилишүү аркылуу',
            'Барабарсыздыктар',
        ],
    },
    {
        # Final order for Теңдемелер: системасы (6 items) - "Жоюу
        # ыкмасы" (kept, chevron-bearing) and "Сызыктуу жана сызыктуу
        # эмес" (fresh chevron-bearing category, created here before its
        # own GROUPS entry can find it - 2-run cross-run dependency,
        # same pattern as the Quadratic fixes above) interleaved among
        # the 4 flat leaves GROUPS' target_items builds.
        'parent_path': ('Алгебра', 'Теңдемелер: системасы'),
        'create_subsubtopics': [
            {'title': 'Сызыктуу жана сызыктуу эмес', 'slug': 'linear-non-linear'},
        ],
        'order': [
            'Түзүү',
            'Жоюу ыкмасы',
            'Алмаштыруу',
            'Аралаш',
            'Графикалык жол менен',
            'Сызыктуу жана сызыктуу эмес',
        ],
    },
    {
        # Final order for Функциялар (3 items) - "Түзүү" and "Маанисин
        # эсептөө" already existed as chevron-bearing categories, no
        # 'create_subsubtopics' needed here; "ЖРТ" is the one flat leaf
        # GROUPS' target_items builds.
        'parent_path': ('Алгебра', 'Функциялар'),
        'order': [
            'Түзүү',
            'Маанисин эсептөө',
            'ЖРТ',
        ],
    },
    {
        # "Квадраттык", "Тегеректер", "Башка сызыктуу эмес",
        # "Түрлөндүрүүлөр", "Дифференциалдоо" are created here (fresh
        # chevron-bearing categories, left empty pending screenshots of
        # their own contents) before their own GROUPS entry can find
        # them - 2-run cross-run dependency, same pattern as the
        # Quadratic/Simultaneous fixes above. "Координаттар", "Сызыктуу:
        # эсептөө", "Сызыктуу: чиймелөө" and "Сызыктуу: окуу" are
        # re-created here too, now as categories, after the GROUPS
        # entry above one-time-deletes each one's old flat MenuItem via
        # 'displaced_url_names' - both steps run in the same execution
        # (GROUPS phase runs entirely before CHILD_ORDER_FIXES), so the
        # delete-then-recreate completes in a single run; their own
        # children still need a 2nd run, same as the brand-new
        # categories above.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу'),
        'create_subsubtopics': [
            {'title': 'Квадраттык', 'slug': 'graphs-abstract-quadratic'},
            {'title': 'Тегеректер', 'slug': 'graphs-abstract-circles'},
            {'title': 'Башка сызыктуу эмес', 'slug': 'graphs-abstract-other-non-linear'},
            {'title': 'Түрлөндүрүүлөр', 'slug': 'graphs-abstract-transformations'},
            {'title': 'Дифференциалдоо', 'slug': 'graphs-abstract-differentiation'},
            {'title': 'Координаттар', 'slug': 'graphs-abstract-coordinates'},
            {'title': 'Сызыктуу: эсептөө', 'slug': 'graphs-abstract-linear-calculating'},
            {'title': 'Сызыктуу: чиймелөө', 'slug': 'graphs-abstract-linear-plotting'},
            {'title': 'Сызыктуу: окуу', 'slug': 'graphs-abstract-linear-reading'},
        ],
        'order': [
            'Координаттар',
            'Сызыктуу: эсептөө',
            'Сызыктуу: чиймелөө',
            'Сызыктуу: окуу',
            'Сызыктуу: аралаш',
            'Квадраттык',
            'Тегеректер',
            'Башка сызыктуу эмес',
            'Түрлөндүрүүлөр',
            'Дифференциалдоо',
        ],
    },
    {
        # "Айландыруу графиктери", "Баа катыштары", "Аралык-Убакыт:
        # турактуу ылдамдык", "Аралык-Убакыт: өзгөрмө ылдамдык",
        # "Ылдамдык-Убакыт" are created here (fresh chevron-bearing
        # categories, left empty pending screenshots of their own
        # contents) - 2-run cross-run dependency.
        'parent_path': ('Алгебра', 'Графиктер: турмуштук'),
        'create_subsubtopics': [
            {'title': 'Айландыруу графиктери', 'slug': 'graphs-real-life-conversion'},
            {'title': 'Баа катыштары', 'slug': 'graphs-real-life-cost-relationships'},
            {'title': 'Аралык-Убакыт: турактуу ылдамдык', 'slug': 'graphs-real-life-distance-time-constant'},
            {'title': 'Аралык-Убакыт: өзгөрмө ылдамдык', 'slug': 'graphs-real-life-distance-time-variable'},
            {'title': 'Ылдамдык-Убакыт', 'slug': 'graphs-real-life-velocity-time'},
        ],
        'order': [
            'Айландыруу графиктери',
            'Баа катыштары',
            'Тереңдик-Убакыт',
            'Көлөм-Убакыт',
            'Аралаш',
            'Аралык-Убакыт: турактуу ылдамдык',
            'Аралык-Убакыт: өзгөрмө ылдамдык',
            'Ылдамдык-Убакыт',
            'Аралаш: аралык жана ылдамдык',
        ],
    },
    {
        # "Сызыктуу" and "Графикалык" are created here (fresh
        # chevron-bearing categories, left empty pending screenshots of
        # their own contents) - 2-run cross-run dependency.
        'parent_path': ('Алгебра', 'Барабарсыздыктар'),
        'create_subsubtopics': [
            {'title': 'Сызыктуу', 'slug': 'inequalities-linear'},
            {'title': 'Графикалык', 'slug': 'inequalities-graphical'},
        ],
        'order': [
            'Сызыктуу',
            'Графикалык',
            'Квадраттык',
            'Сыноо жана жакшыртуу',
        ],
    },
    {
        # "Туюнтма түзүү", "Алгебралык бөлчөктөр", "Бир кашааны ачуу",
        # "Эки жана үч кашааны ачуу", "Бир кашаага ажыратуу", "Эки
        # кашаага ажыратуу", "Далилдөөлөр", "Туюнтмаларды жөнөкөйлөтүү",
        # "Аралаш" are created here (fresh chevron-bearing categories,
        # left empty pending screenshots of their own contents) - 2-run
        # cross-run dependency. "Формуланын өзгөрмөсүн алмаштыруу" and
        # "Белгилөө" are re-created here too, now as categories, after
        # the GROUPS entry above one-time-deletes their old flat
        # MenuItems via 'displaced_url_names' (same pattern as the
        # Equations/Graphs: Abstract fixes - both steps run in the same
        # execution, so the delete-then-recreate completes in a single
        # run; their own children still need a 2nd run).
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү'),
        'create_subsubtopics': [
            {'title': 'Туюнтма түзүү', 'slug': 'manipulation-forming-expressions'},
            {'title': 'Алгебралык бөлчөктөр', 'slug': 'manipulation-algebraic-fractions'},
            {'title': 'Бир кашааны ачуу', 'slug': 'manipulation-expanding-single-brackets'},
            {'title': 'Эки жана үч кашааны ачуу', 'slug': 'manipulation-expanding-double-triple-brackets'},
            {'title': 'Бир кашаага ажыратуу', 'slug': 'manipulation-factorising-single-brackets'},
            {'title': 'Эки кашаага ажыратуу', 'slug': 'manipulation-factorising-double-brackets'},
            {'title': 'Далилдөөлөр', 'slug': 'manipulation-proofs'},
            {'title': 'Туюнтмаларды жөнөкөйлөтүү', 'slug': 'manipulation-simplifying-expressions'},
            {'title': 'Аралаш', 'slug': 'manipulation-mixed'},
            {'title': 'Формуланын өзгөрмөсүн алмаштыруу', 'slug': 'manipulation-changing-subject'},
            {'title': 'Белгилөө', 'slug': 'manipulation-notation'},
        ],
        'order': [
            'Белгилөө',
            'Туюнтма түзүү',
            'Алгебралык бөлчөктөр',
            'Формуланын өзгөрмөсүн алмаштыруу',
            'Бир кашааны ачуу',
            'Эки жана үч кашааны ачуу',
            'Бир кашаага ажыратуу',
            'Эки кашаага ажыратуу',
            'Далилдөөлөр',
            'Туюнтмаларды жөнөкөйлөтүү',
            'Аралаш',
        ],
    },
    {
        # "Сызыктуу" is created here (fresh chevron-bearing category,
        # left empty pending a screenshot of its own contents) - 2-run
        # cross-run dependency.
        'parent_path': ('Алгебра', 'Ырааттуулуктар'),
        'create_subsubtopics': [
            {'title': 'Сызыктуу', 'slug': 'sequences-linear'},
        ],
        'order': [
            'Киришүү',
            'Графиктер менен',
            'Теңдемелер жана функциялар менен',
            'Сызыктуу',
            'Квадраттык',
            'Сызыктуу жана квадраттык',
            'Геометриялык',
            'Фибоначчи',
            'Атайын',
            'Аралаш',
        ],
    },
    {
        # "Белгилерди колдонуу", "Даражасыз", "Даража менен" are created
        # here (fresh chevron-bearing categories, left empty pending
        # screenshots of their own contents) - depends on the
        # Algebra-root entry above having already renamed "Коюу" to
        # "Ордуна коюу" this same run (it appears earlier in this list),
        # then a further cross-run dependency for its own GROUPS entry
        # to find this parent, same pattern as the other fixes above.
        'parent_path': ('Алгебра', 'Ордуна коюу'),
        'create_subsubtopics': [
            {'title': 'Белгилерди колдонуу', 'slug': 'substitution-using-symbols'},
            {'title': 'Даражасыз', 'slug': 'substitution-without-indices'},
            {'title': 'Даража менен', 'slug': 'substitution-with-indices'},
        ],
        'order': [
            'Белгилерди колдонуу',
            'Даражасыз',
            'Даража менен',
            'Калькулятор менен',
            'Векторлор',
        ],
    },
    {
        # Final order for Координаттар's own 6 children - all flat,
        # GROUPS' target_items builds them directly, no
        # 'create_subsubtopics' needed here.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Координаттар'),
        'order': [
            'Окуу',
            'Окуу жана чиймелөө',
            'Кесиндинин орто жана учтук чекиттери',
            'Кесиндилер жана катыш',
            'Геометриялык маселелер',
            'Пифагор менен',
        ],
    },
    {
        # "Координаттардан" (From Coordinates) is a fresh
        # chevron-bearing category, created here, left empty pending a
        # screenshot of its own contents - 2-run cross-run dependency
        # for the 9 flat leaves GROUPS' target_items builds.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: эсептөө'),
        'create_subsubtopics': [
            {'title': 'Координаттардан', 'slug': 'graphs-abstract-linear-calc-from-coordinates'},
        ],
        'order': [
            'Функциялар жана графиктер',
            'Кыйшаюусун жана кесилиш чекитин аныктоо',
            'Координаттарды эсептөө',
            'Кесилишүүлөрдү эсептөө',
            'Координаттардан',
            'Параллель',
            'Перпендикуляр',
            'Параллель жана перпендикуляр',
            'Аралаш',
            'Графиктерди аныктоо',
        ],
    },
    {
        # Final order for Сызыктуу: чиймелөө's own 8 children - all
        # flat, GROUPS' target_items builds them directly.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: чиймелөө'),
        'order': [
            'Функциялар менен',
            'Ырааттуулуктар менен',
            'Жабуу ыкмасы',
            'Сызыктын кыйшаюусу',
            'Кыйшаюу-кесилиш ыкмасы',
            'Маанилер таблицасы ыкмасы',
            'Барабарсыздыктар',
            'Теңдемелер системасы',
        ],
    },
    {
        # Partial order for Сызыктуу: окуу's 4 confirmed children (a 5th
        # row, "Identifying...", was cut off in the reference screenshot
        # - not built yet, flagged to the user).
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Сызыктуу: окуу'),
        'order': [
            'Горизонталдык жана вертикалдык',
            'Сызыктын кыйшаюусу',
            'Сызыктын теңдемеси',
            'Кесилишүүлөрдү эсептөө',
        ],
    },
    {
        # Final order for Квадраттык's own 5 children (under Графиктер:
        # абстракттуу) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Квадраттык'),
        'order': [
            'Чиймелөө',
            'Маанилүү чекиттер',
            'Толук квадратка келтирүү менен бурулуш чекиттери',
            'Кесилишүү аркылуу чечүү',
            'Теңдемелер системасы',
        ],
    },
    {
        # Final order for Тегеректер's own 2 children - both flat,
        # GROUPS' target_items builds them directly.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Тегеректер'),
        'order': [
            'Теңдеме',
            'Жанама',
        ],
    },
    {
        # Final order for Башка сызыктуу эмес's own 6 children - all
        # flat, GROUPS' target_items builds them directly.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Башка сызыктуу эмес'),
        'order': [
            'Чиймелөө',
            'Аныктоо: сызыктуу эмес',
            'Аныктоо: пропорционалдык',
            'Кыйшаюуну болжолдоо',
            'Көрсөткүчтүү функциялар',
            'Тригонометриялык функциялар',
        ],
    },
    {
        # Final order for Түрлөндүрүүлөр's own 2 children - both flat,
        # GROUPS' target_items builds them directly.
        'parent_path': ('Алгебра', 'Графиктер: абстракттуу', 'Түрлөндүрүүлөр'),
        'order': [
            'GCSE',
            'ЖРТ',
        ],
    },
    {
        # Partial order for Айландыруу графиктери's 2 confirmed children
        # (reference screenshot was cut off after these, flagged to the
        # user).
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Айландыруу графиктери'),
        'order': [
            'Окуу',
            'Чиймелөө жана окуу',
        ],
    },
    {
        # Partial order for Баа катыштары's 2 confirmed children
        # (reference screenshot was cut off after these, flagged to the
        # user).
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Баа катыштары'),
        'order': [
            'Киришүү',
            'Теңдемелер менен',
        ],
    },
    {
        # Partial order for Аралык-Убакыт: турактуу ылдамдык's 2
        # confirmed children (reference screenshot was cut off after
        # these, flagged to the user).
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Аралык-Убакыт: турактуу ылдамдык'),
        'order': [
            'Окуу',
            'Чиймелөө жана окуу',
        ],
    },
    {
        # Final order for Ылдамдык-Убакыт's own 3 children - all flat,
        # GROUPS' target_items builds them directly.
        'parent_path': ('Алгебра', 'Графиктер: турмуштук', 'Ылдамдык-Убакыт'),
        'order': [
            'Аралык',
            'Ылдамдануу',
            'Аралаш',
        ],
    },
    {
        # Final order for Сызыктуу's own 6 children (under
        # Барабарсыздыктар) - all flat, GROUPS' target_items builds
        # them directly.
        'parent_path': ('Алгебра', 'Барабарсыздыктар', 'Сызыктуу'),
        'order': [
            'Түзүү',
            'Эсептөө',
            'Чагылдыруу',
            'Чечүү: жалгыз',
            'Чечүү: жалгыз жана кош',
            'Аралаш',
        ],
    },
    {
        # Partial order for Графикалык's 2 confirmed children (under
        # Барабарсыздыктар) - reference screenshot was cut off after
        # these, flagged to the user.
        'parent_path': ('Алгебра', 'Барабарсыздыктар', 'Графикалык'),
        'order': [
            'Керектүү аймакты боёо',
            'Керексиз аймакты боёо',
        ],
    },
    {
        # Final order for Туюнтма түзүү's own 3 children (under
        # Өзгөртүп түзүү) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Туюнтма түзүү'),
        'order': [
            'Функция машиналары менен',
            'Сызыктуу',
            'Квадраттык',
        ],
    },
    {
        # Final order for Алгебралык бөлчөктөр's own 6 children (under
        # Өзгөртүп түзүү) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Алгебралык бөлчөктөр'),
        'order': [
            'Кошуу жана кемитүү',
            'Көбөйтүү жана бөлүү',
            'Аралаш',
            'Жөнөкөйлөтүү',
            'Жөнөкөйлөтүү: көбөйтүүчүлөргө ажыратуу менен',
            'Жөнөкөйлөтүү: эки квадраттын айырмасы',
        ],
    },
    {
        # Final order for Формуланын өзгөрмөсүн алмаштыруу's own 4
        # children (under Өзгөртүп түзүү) - all flat, GROUPS' target_items
        # builds them directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Формуланын өзгөрмөсүн алмаштыруу'),
        'order': [
            'Формулаларды түрлөндүрүү',
            'Функция машинасын колдонуу',
            'Көбөйтүүчүлөргө ажыратуусуз',
            'Көбөйтүүчүлөргө ажыратуу менен',
        ],
    },
    {
        # Final order for Бир кашааны ачуу's own 7 children (under
        # Өзгөртүп түзүү) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Бир кашааны ачуу'),
        'order': [
            'Коэффициентсиз',
            'Коэффициент менен',
            'Даражалар менен',
            'Көп кашаалар',
            'Аралаш',
            'Көбөйтүүчүлөргө ажыратуу менен: даражасыз',
            'Көбөйтүүчүлөргө ажыратуу менен: даража менен',
        ],
    },
    {
        # Final order for Эки жана үч кашааны ачуу's own 7 children
        # (under Өзгөртүп түзүү) - all flat, GROUPS' target_items builds
        # them directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Эки жана үч кашааны ачуу'),
        'order': [
            'Эки кашаа: коэффициентсиз',
            'Эки кашаа: коэффициент менен',
            'Көбөйтүүчүлөргө ажыратуу менен',
            'Квадраттар',
            'Үч кашаа',
            'Аралаш ачуу',
            'Тамырлар менен',
        ],
    },
    {
        # Final order for Бир кашаага ажыратуу's own 4 children (under
        # Өзгөртүп түзүү) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Бир кашаага ажыратуу'),
        'order': [
            'Даражасыз',
            'Даража менен',
            'Ачуу менен: даражасыз',
            'Ачуу менен: даража менен',
        ],
    },
    {
        # Final order for Эки кашаага ажыратуу's own 7 children (under
        # Өзгөртүп түзүү) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Эки кашаага ажыратуу'),
        'order': [
            'Квадраттык: коэффициентсиз',
            'Квадраттык: коэффициент менен',
            'Ачуу менен',
            'Толук квадратка келтирүү',
            'Эки квадраттын айырмасы',
            'Аралаш ажыратуу',
            'Топтоштуруу',
        ],
    },
    {
        # Final order for Белгилөө's own 14 children (under Өзгөртүп
        # түзүү) - all flat, GROUPS' target_items builds them directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Белгилөө'),
        'order': [
            'Кошуу',
            'Кошуу: кашаа менен',
            'Кошуу: даража менен',
            'Көбөйтүү',
            'Көбөйтүү жана кошуу',
            'Бөлүү',
            'Көбөйтүү жана бөлүү',
            'Квадрат жана куб',
            'Аралаш арифметика',
            'Терс жана бөлчөк даражалар менен',
            'Рационалдык: көбөйтүүчүлөргө ажыратуу менен',
            'Рационалдык: эки квадраттын айырмасы',
            'Аралаш',
            'Аралаш: баары',
        ],
    },
    {
        # Final order for Аралаш's own 2 children (under Өзгөртүп
        # түзүү) - both flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Аралаш'),
        'order': [
            'Негизги деңгээл',
            'Жогорку деңгээл',
        ],
    },
    {
        # Final order for Сызыктуу's own 4 children (under
        # Ырааттуулуктар) - all flat, GROUPS' target_items builds them
        # directly.
        'parent_path': ('Алгебра', 'Ырааттуулуктар', 'Сызыктуу'),
        'order': [
            'Киришүү',
            'Мүчөлөрдү эсептөө',
            '2 мүчөдөн',
            'Суммалоо (ЖРТ)',
        ],
    },
    {
        # Final order for Туюнтмаларды жөнөкөйлөтүү's own 13 children
        # (under Өзгөртүп түзүү) - all flat, GROUPS' target_items builds
        # them directly.
        'parent_path': ('Алгебра', 'Өзгөртүп түзүү', 'Туюнтмаларды жөнөкөйлөтүү'),
        'order': [
            'Кошуу',
            'Кошуу: кашаа менен',
            'Кошуу: даража менен',
            'Көбөйтүү',
            'Көбөйтүү жана кошуу',
            'Бөлүү',
            'Көбөйтүү жана бөлүү',
            'Квадрат жана куб',
            'Аралаш арифметика',
            'Терс жана бөлчөк даражалар менен',
            'Рационалдык: көбөйтүүчүлөргө ажыратуу менен',
            'Рационалдык: эки квадраттын айырмасы',
            'Аралаш: баары',
        ],
    },
    {
        # Final order for Белгилерди колдонуу's own 3 children (under
        # Ордуна коюу) - GROUPS' target_items builds Оң/Терс directly;
        # Аралаш is the canonical copy MIRROR_LEAVES mirrors elsewhere.
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Белгилерди колдонуу'),
        'order': ['Оң', 'Терс', 'Аралаш'],
    },
    {
        # Final order for Даражасыз's own 3 children (under Ордуна
        # коюу) - Аралаш is supplied by MIRROR_LEAVES, which runs before
        # this fix.
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Даражасыз'),
        'order': ['Оң', 'Терс', 'Аралаш'],
    },
    {
        # Final order for Даража менен's own 3 children (under Ордуна
        # коюу) - same as its 2 siblings above.
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Даража менен'),
        'order': ['Оң', 'Терс', 'Аралаш'],
    },
    {
        # Геометрия (a root Topic, like Пропорция) started out with 6
        # merged Subtopics from an earlier, coarser import
        # (import_reference_taxonomy.py) - e.g. "Аянт, периметр жана
        # көлөм" bundled Area & Perimeter, Circles and Volume & Surface
        # Area into one. The new reference site's own top-level menu
        # instead shows 13 separate categories, so this entry rebuilds
        # Геометрия's direct children to match it exactly: Бурчтар
        # (Angles), Түрлөндүрүүлөр (Transformations) and Векторлор
        # (Vectors) already matched 1:1 and are left untouched; the
        # other 10 are created fresh as empty Subtopic-level categories
        # via 'create_subsubtopics' (which, same as for a root-Topic
        # parent elsewhere in this file, creates a new Subtopic + its
        # MenuItem rather than a SubSubtopic when the parent itself has
        # no subtopic_id). The 3 old merged Subtopics (and their now-
        # orphaned SubSubtopic children, all with 0 resources attached)
        # are then pruned by the exhaustive 'order' list below like any
        # other leftover - only the navigation entries go; the
        # underlying Subtopic/SubSubtopic rows are left in place,
        # unreferenced, same as every other prune in this file.
        'parent_path': ('Геометрия',),
        'create_subsubtopics': [
            {'title': 'Аянт жана периметр', 'slug': 'area-perimeter'},
            {'title': 'Азимут', 'slug': 'bearings'},
            {'title': 'Классификациялоо жана терминология', 'slug': 'classifying-vocabulary'},
            {'title': 'Курулуштар', 'slug': 'construction'},
            {'title': 'Координаттар', 'slug': 'coordinates'},
            {'title': 'Өлчөмдөр', 'slug': 'measures'},
            {'title': 'Пифагор', 'slug': 'pythagoras'},
            {'title': 'Окшоштук', 'slug': 'similarity'},
            {'title': 'Тригонометрия', 'slug': 'trigonometry'},
            {'title': 'Көлөм жана бет аянты', 'slug': 'volume-surface-area'},
        ],
        'order': [
            'Бурчтар',
            'Аянт жана периметр',
            'Азимут',
            'Классификациялоо жана терминология',
            'Курулуштар',
            'Координаттар',
            'Өлчөмдөр',
            'Пифагор',
            'Окшоштук',
            'Түрлөндүрүүлөр',
            'Тригонометрия',
            'Векторлор',
            'Көлөм жана бет аянты',
        ],
    },
    {
        # "Бурчтар" (Angles) carried 3 children from the old coarser
        # import (see the Геометрия entry above) - "Негизги бурчтар"
        # (Basic Angles) isn't in the new reference's 6-item list at
        # all, while "Параллель сызыктар" (Parallel Lines) and "Көп
        # бурчтуктар" (Polygons) match 1:1 and are kept, reused as-is.
        # Reference (6 items): Angle Facts, Drawing & Measuring, Circle
        # Theorems, Parallel Lines, Polygons, Mixed are all
        # chevron-bearing categories - the 4 new ones are created here
        # via 'create_subsubtopics', left empty pending their own
        # screenshots (which the next 3 entries below already fill in
        # for Angle Facts, Drawing & Measuring, Circle Theorems).
        'parent_path': ('Геометрия', 'Бурчтар'),
        'create_subsubtopics': [
            {'title': 'Бурч фактылары', 'slug': 'angle-facts'},
            {'title': 'Чийүү жана өлчөө', 'slug': 'drawing-measuring'},
            {'title': 'Тегерек теоремалары', 'slug': 'circle-theorems'},
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Бурч фактылары',
            'Чийүү жана өлчөө',
            'Тегерек теоремалары',
            'Параллель сызыктар',
            'Көп бурчтуктар',
            'Аралаш',
        ],
    },
    {
        # Final order for Бурч фактылары's own 6 children (under
        # Геометрия > Бурчтар) - all flat, GROUPS' target_items builds
        # them directly.
        'parent_path': ('Геометрия', 'Бурчтар', 'Бурч фактылары'),
        'order': [
            'Терминология',
            'Чекиттин тегерегинде',
            'Түз сызыктарда',
            'Вертикаль бурчтар',
            'Үч бурчтуктар',
            'Аралаш',
        ],
    },
    {
        # Final order for Чийүү жана өлчөө's own 4 children (under
        # Геометрия > Бурчтар) - all flat, GROUPS' target_items builds
        # them directly.
        'parent_path': ('Геометрия', 'Бурчтар', 'Чийүү жана өлчөө'),
        'order': [
            'Чийүү',
            'Өлчөө',
            'Чийүү жана өлчөө',
            'Болжолдоо',
        ],
    },
    {
        # Final order for Тегерек теоремалары's own 10 children (under
        # Геометрия > Бурчтар) - all flat, GROUPS' target_items builds
        # them directly.
        'parent_path': ('Геометрия', 'Бурчтар', 'Тегерек теоремалары'),
        'order': [
            'Терминология',
            'Алмашма сегмент',
            'Тегеректин четинде',
            'Циклдик төрт бурчтуктар',
            'Жанамалар жана хордалар',
            'Айкалышкан',
            'Аралаш',
            'Пифагор менен',
            'Тригонометрия менен',
            'Кесилишкен хордалар (ЖРТ)',
        ],
    },
    {
        # Final order for Параллель сызыктар's own 2 known children
        # (under Геометрия > Бурчтар) - partial, screenshot was cut off.
        'parent_path': ('Геометрия', 'Бурчтар', 'Параллель сызыктар'),
        'order': [
            'Киришүү',
            'Теңдемелерди чечүү',
        ],
    },
    {
        # "Аралаш" under Көп бурчтуктар doesn't exist yet - created here
        # via 'create_subsubtopics' (GROUPS' own target_items can only
        # create flat url_name leaves, not a chevron-bearing category).
        # An 'order' entry is needed too, unlike a purely-GROUPS-built
        # parent: 'create_subsubtopics' doesn't know about the 5
        # existing GROUPS-built siblings' order values, so without this
        # it would default to the back of the queue by coincidence
        # rather than by design - this pins it to its reference
        # position (last).
        'parent_path': ('Геометрия', 'Бурчтар', 'Көп бурчтуктар'),
        'create_subsubtopics': [
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Үч бурчтуктар',
            'Төрт бурчтуктар',
            'Атайын төрт бурчтуктар',
            'Туура',
            'Туура эмес',
            'Аралаш',
        ],
    },
    {
        # "Аянт жана периметр" (Area & Perimeter) under Геометрия was
        # an empty top-level category. Reference (7 items), all
        # chevron-bearing categories - created here via
        # 'create_subsubtopics', left empty pending their own
        # screenshots.
        'parent_path': ('Геометрия', 'Аянт жана периметр'),
        'create_subsubtopics': [
            {'title': 'Тегеректер', 'slug': 'circles'},
            {'title': 'Татаал: түз сызыктуу', 'slug': 'compound-rectilinear'},
            {'title': 'Татаал: көп бурчтуктуу', 'slug': 'compound-polygonal'},
            {'title': 'Татаал: тегеректер менен', 'slug': 'compound-with-circles'},
            {'title': 'Төрт бурчтуктар', 'slug': 'quadrilaterals'},
            {'title': 'Үч бурчтуктар', 'slug': 'triangles'},
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Тегеректер',
            'Татаал: түз сызыктуу',
            'Татаал: көп бурчтуктуу',
            'Татаал: тегеректер менен',
            'Төрт бурчтуктар',
            'Үч бурчтуктар',
            'Аралаш',
        ],
    },
    {
        # "Классификациялоо жана терминология" (Classifying &
        # Vocabulary) under Геометрия was an empty top-level category.
        # Reference (2 items), both chevron-bearing categories -
        # created here via 'create_subsubtopics', left empty pending
        # their own screenshots.
        'parent_path': ('Геометрия', 'Классификациялоо жана терминология'),
        'create_subsubtopics': [
            {'title': 'Фигураларды классификациялоо', 'slug': 'classifying-shapes'},
            {'title': 'Терминология', 'slug': 'vocabulary'},
        ],
        'order': [
            'Фигураларды классификациялоо',
            'Терминология',
        ],
    },
    {
        # "Курулуштар" (Construction) under Геометрия was an empty
        # top-level category. Reference screenshot showed 12 items
        # (Angles, Compass Skills, Polygons, Bisectors, Loci, Bisectors
        # & Loci, Nets, Plans & Elevations, Isometric Grids, Measuring
        # Lines, Scale Drawings, Sketching Diagrams) all chevron-bearing
        # - the last one ("Sketching Diagrams") was only partially
        # visible at the very bottom edge of the screenshot, so there
        # may be more below it; only these 12 are built for now,
        # flagged to the user to confirm the rest. Created here via
        # 'create_subsubtopics', left empty pending their own
        # screenshots.
        'parent_path': ('Геометрия', 'Курулуштар'),
        'create_subsubtopics': [
            {'title': 'Бурчтар', 'slug': 'angles'},
            {'title': 'Циркуль көндүмдөрү', 'slug': 'compass-skills'},
            {'title': 'Көп бурчтуктар', 'slug': 'polygons'},
            {'title': 'Бисектрисалар', 'slug': 'bisectors'},
            {'title': 'Геометриялык орундар', 'slug': 'loci'},
            {'title': 'Бисектрисалар жана геометриялык орундар', 'slug': 'bisectors-loci'},
            {'title': 'Жайылмалар', 'slug': 'nets'},
            {'title': 'Пландар жана көрүнүштөр', 'slug': 'plans-elevations'},
            {'title': 'Изометрикалык тор', 'slug': 'isometric-grids'},
            {'title': 'Сызыктарды өлчөө', 'slug': 'measuring-lines'},
            {'title': 'Масштабдуу сүрөттөр', 'slug': 'scale-drawings'},
            {'title': 'Диаграммаларды чийүү', 'slug': 'sketching-diagrams'},
        ],
        'order': [
            'Бурчтар',
            'Циркуль көндүмдөрү',
            'Көп бурчтуктар',
            'Бисектрисалар',
            'Геометриялык орундар',
            'Бисектрисалар жана геометриялык орундар',
            'Жайылмалар',
            'Пландар жана көрүнүштөр',
            'Изометрикалык тор',
            'Сызыктарды өлчөө',
            'Масштабдуу сүрөттөр',
            'Диаграммаларды чийүү',
        ],
    },
    {
        # "Тригонометрия менен" under Пифагор doesn't exist yet -
        # created here via 'create_subsubtopics' (GROUPS' own
        # target_items can only create flat url_name leaves). An
        # 'order' entry is needed since 'create_subsubtopics' doesn't
        # know where the 11 GROUPS-built siblings already sit.
        'parent_path': ('Геометрия', 'Пифагор'),
        'create_subsubtopics': [
            {'title': 'Тригонометрия менен', 'slug': 'with-trigonometry'},
        ],
        'order': [
            'Киришүү',
            'A же B табуу',
            'A, B же C табуу',
            'Тең бүйрүүчү үч бурчтуктар',
            'Турмуштук маселелер',
            '3D',
            'Координаттар',
            'Аралаш',
            'Фигуралардын периметрлери',
            'Тамырлар менен',
            'Тригонометрия менен',
            'Тегерек теоремалары менен',
        ],
    },
    {
        # "Түрлөндүрүүлөр" (Transformations) under Геометрия carried 1
        # child ("2D түрлөндүрүүлөр") from the old coarser import - not
        # in the new reference's 10-item list at all (0 resources
        # attached), pruned by the exhaustive order list below. All 10
        # reference items are chevron-bearing categories, created here
        # via 'create_subsubtopics', left empty pending their own
        # screenshots.
        'parent_path': ('Геометрия', 'Түрлөндүрүүлөр'),
        'create_subsubtopics': [
            {'title': 'Чоңойтуу', 'slug': 'enlargement'},
            {'title': 'Чагылдыруу', 'slug': 'reflection'},
            {'title': 'Буруу', 'slug': 'rotation'},
            {'title': 'Жылдыруу', 'slug': 'translation'},
            {'title': 'Өзгөрбөгөн чекиттер', 'slug': 'invariant-points'},
            {'title': 'Айкалышкан', 'slug': 'combined'},
            {'title': 'Аралаш', 'slug': 'mixed'},
            {'title': 'Сызыктуу симметрия', 'slug': 'line-symmetry'},
            {'title': 'Айлануу симметриясы', 'slug': 'rotational-symmetry'},
            {'title': 'Тесселляция', 'slug': 'tessellation'},
        ],
        'order': [
            'Чоңойтуу',
            'Чагылдыруу',
            'Буруу',
            'Жылдыруу',
            'Өзгөрбөгөн чекиттер',
            'Айкалышкан',
            'Аралаш',
            'Сызыктуу симметрия',
            'Айлануу симметриясы',
            'Тесселляция',
        ],
    },
    {
        # The 6 chevron-bearing categories under Тригонометрия don't
        # exist yet - created here via 'create_subsubtopics'. An
        # 'order' entry is needed since 'create_subsubtopics' doesn't
        # know where the 7 GROUPS-built flat siblings already sit.
        'parent_path': ('Геометрия', 'Тригонометрия'),
        'create_subsubtopics': [
            {'title': 'Синус жана косинус катыштары', 'slug': 'sine-cosine-ratios'},
            {'title': 'Тангенс катышы', 'slug': 'tangent-ratio'},
            {'title': 'Бардык катыштар', 'slug': 'all-ratios'},
            {'title': 'Турмуштук маселелер', 'slug': 'real-life'},
            {'title': 'Пифагор менен', 'slug': 'with-pythagoras'},
            {'title': 'Синус жана косинус эрежелери', 'slug': 'sine-cosine-rules'},
        ],
        'order': [
            'Киришүү',
            'Графиктер',
            'Катышты тандоо',
            'Синус жана косинус катыштары',
            'Тангенс катышы',
            'Бардык катыштар',
            'Тең бүйрүүчү үч бурчтуктар',
            'Турмуштук маселелер',
            'Калькуляторсуз',
            'Пифагор менен',
            'Тегерек теоремалары менен',
            'Аянт эрежеси',
            'Синус жана косинус эрежелери',
        ],
    },
    {
        # The 9 chevron-bearing categories under Көлөм жана бет аянты
        # don't exist yet - created here via 'create_subsubtopics'. An
        # 'order' entry is needed since 'create_subsubtopics' doesn't
        # know where the 3 GROUPS-built flat siblings already sit.
        'parent_path': ('Геометрия', 'Көлөм жана бет аянты'),
        'create_subsubtopics': [
            {'title': 'Конус', 'slug': 'cone'},
            {'title': 'Параллелепипед', 'slug': 'cuboid'},
            {'title': 'Цилиндр', 'slug': 'cylinder'},
            {'title': 'Призма', 'slug': 'prism'},
            {'title': 'Цилиндр жана призма', 'slug': 'cylinder-prism'},
            {'title': 'Кесилген конус', 'slug': 'frustum'},
            {'title': 'Пирамида', 'slug': 'pyramid'},
            {'title': 'Сфера', 'slug': 'sphere'},
            {'title': 'Аралаш', 'slug': 'mixed'},
        ],
        'order': [
            'Терминология',
            'Көлөмгө киришүү',
            'Жайылмалар',
            'Конус',
            'Параллелепипед',
            'Цилиндр',
            'Призма',
            'Цилиндр жана призма',
            'Кесилген конус',
            'Пирамида',
            'Сфера',
            'Аралаш',
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
        # "Өлчөмдөр" (Measures) under Геометрия is the exact same
        # 8-item set as Сандар's own top-level Өлчөмдөр (Compound,
        # Measuring Lines, Money, Reading Scales, Scale Drawings,
        # Systems of Measurement, Area & Volume Conversion, Time) - the
        # user spotted this duplication directly from the reference
        # site's own menu. mirror_children recurses into every child
        # that itself has further children (Татаал өлчөмдөр,
        # Акча, Масштабдуу сүрөттөр, Өлчөө системалары, Аянт жана
        # көлөм бирдиктерин алмаштыруу, Убакыт all do), so this one
        # entry brings the whole already-built subtree across - no new
        # pages needed.
        'parent_path': ('Геометрия', 'Өлчөмдөр'),
        'source_parent_path': ('Сандар', 'Өлчөмдөр'),
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

# A single flat leaf item (not a whole node, not a whole children list)
# that the reference site reuses verbatim across more than one parent -
# e.g. Ордуна коюу's "Белгилерди колдонуу"/"Даражасыз"/"Даража менен"
# siblings each keep their own distinct Positive/Negative pages but all
# 3 share one "Аралаш" (Mixed) page, shown with the reference's own
# mirror-arrow icon. Neither GROUPS (can't safely share a url_name
# across sibling entries within one run - see that entry's own comment)
# nor MIRROR_GROUPS/MIRROR_NODES (built for copying a whole children
# list or a whole node, which would also drag along - and overwrite -
# each target's own distinct siblings) fits this one-leaf-only case, so
# it gets its own small, direct (parent, title) match instead.
MIRROR_LEAVES = [
    {
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Даражасыз'),
        'title': 'Аралаш',
        'url_name': 'algebra_substitution_mixed',
        'order': 3,
    },
    {
        'parent_path': ('Алгебра', 'Ордуна коюу', 'Даража менен'),
        'title': 'Аралаш',
        'url_name': 'algebra_substitution_mixed',
        'order': 3,
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

        for leaf in MIRROR_LEAVES:
            label = ' > '.join(leaf['parent_path'])
            self.stdout.write(f'=== Mirror leaf: {label} ===')
            try:
                parent = self.resolve_path(leaf['parent_path'])
            except MenuItem.DoesNotExist:
                self.stderr.write(f'  "{label}" not found.')
                continue
            mirrored, created = MenuItem.objects.get_or_create(
                parent=parent, title=leaf['title'],
                defaults={'url_name': leaf['url_name'], 'order': leaf['order']},
            )
            if created:
                self.stdout.write(f'  Mirrored leaf: {leaf["title"]} ({leaf["url_name"]})')
            elif mirrored.url_name != leaf['url_name']:
                mirrored.url_name = leaf['url_name']
                mirrored.save(update_fields=['url_name'])
                self.stdout.write(f'  Updated mirrored leaf: {leaf["title"]} ({leaf["url_name"]})')

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
