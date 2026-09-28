from django.http import Http404
from django.shortcuts import render

# The other 7 slots of Decimals > Arithmetic: 1 Digit (Кошуу/Adding is the
# one real hand-built page - see koshuu_1_digit_view - the rest have no
# material yet). Shares that page's exact visual chrome (see
# templates/resources/onduktar/operation_placeholder.html) so navigating
# between a real operation and a "coming soon" one feels like the same
# page family, not two different systems. Each gets its own short URL
# (config/urls.py), matching koshuu-1-digit/'s own convention, instead of
# the long generic /resources/topic/number/... path.
OPERATION_PLACEHOLDER_TITLES = {
    'subtracting-1-digit': 'Кемитүү — 1 орундуу сандар',
    'adding-subtracting-1-digit': 'Кошуу жана кемитүү — 1 орундуу сандар',
    'multiplying-1-digit': 'Көбөйтүү — 1 орундуу сандар',
    'dividing-1-digit': 'Бөлүү — 1 орундуу сандар',
    'multiplying-dividing-1-digit': 'Көбөйтүү жана бөлүү — 1 орундуу сандар',
    'mixed-1-digit': 'Аралаш эсептөөлөр — 1 орундуу сандар',
    'dividing-by-less-than-1': '1ден кичине ондукка бөлүү',

    # Ондуктар > Эсептөөлөр: 1 жана 2 орундук сандар - none of these 8
    # have a real hand-built page yet, unlike the 1-digit group above.
    'adding-1-2-digit': 'Кошуу — 1 жана 2 орундук сандар',
    'subtracting-1-2-digit': 'Кемитүү — 1 жана 2 орундук сандар',
    'adding-subtracting-1-2-digit': 'Кошуу жана кемитүү — 1 жана 2 орундук сандар',
    'multiplying-1-2-digit': 'Көбөйтүү — 1 жана 2 орундук сандар',
    'dividing-1-2-digit': 'Бөлүү — 1 жана 2 орундук сандар',
    'multiplying-dividing-1-2-digit': 'Көбөйтүү жана бөлүү — 1 жана 2 орундук сандар',
    'multiplying-dividing-10-100-1000': '10, 100, 1000гө көбөйтүү жана бөлүү',
    'mixed-1-2-digit': 'Аралаш эсептөөлөр — 1 жана 2 орундук сандар',

    # Ондуктар > Эсептөөлөр: бүтүн сандар менен - none of these 8 have a
    # real hand-built page yet either.
    'adding-with-integers': 'Кошуу — бүтүн сандар менен',
    'subtracting-with-integers': 'Кемитүү — бүтүн сандар менен',
    'adding-subtracting-with-integers': 'Кошуу жана кемитүү — бүтүн сандар менен',
    'multiplying-with-integers': 'Көбөйтүү — бүтүн сандар менен',
    'dividing-with-integers': 'Бөлүү — бүтүн сандар менен',
    'multiplying-dividing-with-integers': 'Көбөйтүү жана бөлүү — бүтүн сандар менен',
    'mixed-with-integers': 'Аралаш эсептөөлөр — бүтүн сандар менен',
    'dividing-divisor-less-than-1-with-integers': 'Бөлүүчүсү 1ден кичине бөлүү — бүтүн сандар менен',

    # Ондуктар > Акча - none of these 5 have a real hand-built page yet.
    'purchasing-calculator': 'Сатып алуу: калькулятор менен',
    'purchasing-non-calculator': 'Сатып алуу: калькуляторсуз',
    'hire-purchase': 'Насыяга сатып алуу',
    'bills-and-statements': 'Эсептер жана көчүрмөлөр',
    'rates-of-pay': 'Эмгек акы ставкалары',

    # Ондуктар > Мезгилдүү ондуктар - neither of these 2 have a real
    # hand-built page yet.
    'recurring-decimals-ordering': 'Мезгилдүү ондуктарды иреттөө',
    'recurring-converting-to-fractions': 'Мезгилдүү ондуктарды бөлчөккө айландыруу',

    # Багытталган сандар > Эсептөөлөр - none of these 7 have a real
    # hand-built page yet (the one real page for Directed Numbers,
    # directed_numbers_view, is a general combined page that doesn't map
    # onto any single one of these 7 slots).
    'adding-directed': 'Кошуу',
    'subtracting-directed': 'Кемитүү',
    'adding-subtracting-directed': 'Кошуу жана кемитүү',
    'multiplying-dividing-directed': 'Көбөйтүү жана бөлүү',
    'mixed-directed': 'Аралаш эсептөөлөр',
    'with-bidmas-directed': 'BIDMAS менен',
    'complex-directed': 'Татаал эсептөөлөр',

    # Сандар > Эквиваленттүүлүк (top-level topic) > Бөлчөктөрдү айландыруу
    # (Converting Fractions) - none of these 10 have a real hand-built
    # page yet.
    'fractions-to-decimals': 'Ондукка айландыруу',
    'fractions-to-decimals-calculator': 'Ондукка айландыруу: калькулятор менен',
    'fractions-to-percentages': 'Пайызга айландыруу',
    'fractions-to-percentages-calculator': 'Пайызга айландыруу: калькулятор менен',
    'fractions-to-ratios': 'Катышка айландыруу',
    'fractions-to-all': 'Баарына айландыруу',
    'fractions-with-decimals': 'Ондуктар менен',
    'fractions-with-percentages': 'Пайыздар менен',
    'fractions-with-ratios': 'Катыштар менен',
    'fractions-with-all': 'Баары менен',

    # Сандар > Эквиваленттүүлүк (top-level topic) > Ондуктарды айландыруу
    # (Converting Decimals) - none of these 7 have a real hand-built page
    # yet.
    'decimals-to-fractions': 'Бөлчөккө айландыруу',
    'decimals-to-percentages': 'Пайызга айландыруу',
    'decimals-to-both': 'Бөлчөккө жана пайызга айландыруу',
    'decimals-recurring-to-fractions': 'Кайталануучу ондуктарды бөлчөккө айландыруу',
    'decimals-with-fractions': 'Бөлчөктөр менен',
    'decimals-with-percentages': 'Пайыздар менен',
    'decimals-with-both': 'Экөө менен тең',

    # Сандар > Эквиваленттүүлүк (top-level topic) > Пайыздарды айландыруу
    # (Converting Percentages) - none of these 8 have a real hand-built
    # page yet.
    'percentages-to-fractions': 'Бөлчөккө айландыруу',
    'percentages-to-decimals': 'Ондукка айландыруу',
    'percentages-to-ratios': 'Катышка айландыруу',
    'percentages-to-all': 'Баарына айландыруу',
    'percentages-with-fractions': 'Бөлчөктөр менен',
    'percentages-with-decimals': 'Ондуктар менен',
    'percentages-with-ratios': 'Катыштар менен',
    'percentages-with-all': 'Баары менен',

    # Сандар > Эквиваленттүүлүк (top-level topic) > Катыштарды айландыруу
    # (Converting Ratios) - none of these 6 have a real hand-built page
    # yet.
    'ratios-to-fractions': 'Бөлчөккө айландыруу',
    'ratios-to-percentages': 'Пайызга айландыруу',
    'ratios-to-both': 'Бөлчөккө жана пайызга айландыруу',
    'ratios-with-fractions': 'Бөлчөктөр менен',
    'ratios-with-percentages': 'Пайыздар менен',
    'ratios-with-both': 'Экөө менен тең',

    # Болжолдоо жана тегеректөө (Estimating & Rounding) > Тегеректөө
    # (Rounding) - none of these 4 have a real hand-built page yet.
    'rounding-decimal-places': 'Ондук орундар',
    'rounding-significant-figures': 'Маанилүү сандар',
    'rounding-mixed': 'Аралаш',
    'rounding-whole-numbers': 'Бүтүн сандар',

    # Болжолдоо жана тегеректөө > Ката аралыктары (Error Intervals) -
    # none of these 3 have a real hand-built page yet.
    'error-intervals-decimal-significant': 'Ондук орундар жана маанилүү сандар',
    'error-intervals-calculations': 'Эсептөөлөр',
    'error-intervals-truncation': 'Кесүү',

    # Бөлүүчүлөр, эселиктер жана жөнөкөй сандар > ЭЧОБ & ЭКОЭ: тизмелөө
    # менен (HCF & LCM: Listing) - none of these 3 have a real hand-built
    # page yet.
    'hcf-listing': 'Эң чоң орток бөлүүчү',
    'lcm-listing': 'Эң кичине орток эселик',
    'hcf-lcm-listing-mixed': 'Аралаш',

    # Бөлүүчүлөр, эселиктер жана жөнөкөй сандар > ЭЧОБ & ЭКОЭ: жөнөкөй
    # көбөйтүүчүлөргө ажыратуу менен (HCF & LCM: Prime Factorisation) -
    # none of these 3 have a real hand-built page yet.
    'hcf-prime-factorisation': 'Эң чоң орток бөлүүчү',
    'lcm-prime-factorisation': 'Эң кичине орток эселик',
    'hcf-lcm-prime-factorisation-mixed': 'Аралаш',

    # Бөлчөктөр > Эсептөөлөр: бирдик бөлчөктөр (Arithmetic: Unit
    # Fractions) - none of these 8 have a real hand-built page yet.
    'unit-fractions-adding': 'Кошуу',
    'unit-fractions-subtracting': 'Кемитүү',
    'unit-fractions-adding-subtracting': 'Кошуу жана кемитүү',
    'unit-fractions-multiplying': 'Көбөйтүү',
    'unit-fractions-dividing': 'Бөлүү',
    'unit-fractions-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'unit-fractions-with-integers': 'Бүтүн сандар менен',
    'unit-fractions-mixed': 'Аралаш',

    # Бөлчөктөр > Эсептөөлөр: бирдик эмес бөлчөктөр (Arithmetic: Non-Unit
    # Fractions) - none of these 9 have a real hand-built page yet.
    'non-unit-fractions-adding': 'Кошуу',
    'non-unit-fractions-subtracting': 'Кемитүү',
    'non-unit-fractions-adding-subtracting': 'Кошуу жана кемитүү',
    'non-unit-fractions-multiplying': 'Көбөйтүү',
    'non-unit-fractions-dividing': 'Бөлүү',
    'non-unit-fractions-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'non-unit-fractions-with-cancelling': 'Кыскартуу менен',
    'non-unit-fractions-with-integers': 'Бүтүн сандар менен',
    'non-unit-fractions-mixed': 'Аралаш',

    # Бөлчөктөр > Эквиваленттүүлүк - none of these 13 have a real
    # hand-built page yet.
    'fractions-equiv-to-decimals': 'Ондукка айландыруу',
    'fractions-equiv-to-decimals-calculator': 'Ондукка айландыруу: калькулятор менен',
    'fractions-equiv-to-percentages': 'Пайызга айландыруу',
    'fractions-equiv-to-percentages-calculator': 'Пайызга айландыруу: калькулятор менен',
    'fractions-equiv-to-ratios': 'Катышка айландыруу',
    'fractions-equiv-to-all': 'Баарына айландыруу',
    'fractions-equiv-with-decimals': 'Ондуктар менен',
    'fractions-equiv-with-percentages': 'Пайыздар менен',
    'fractions-equiv-with-ratios': 'Катыштар менен',
    'fractions-equiv-fdp': 'Бөлчөк, ондук жана пайыздык эквиваленттүүлүк',
    'fractions-equiv-fdp-ordering': 'Бөлчөктөрдү, ондуктарды жана пайыздарды иреттөө',
    'fractions-equiv-fpr': 'Бөлчөк, пайыз жана катыш эквиваленттүүлүгү',
    'fractions-equiv-fdpr': 'Бөлчөк, ондук, пайыз жана катыш эквиваленттүүлүгү',

    # Бөлчөктөр > Барабар бөлчөктөр (Equivalent Fractions) - none of these
    # 4 have a real hand-built page yet.
    'equivalent-fractions-simplifying': 'Жөнөкөйлөтүү',
    'equivalent-fractions-comparing-ordering': 'Салыштыруу жана иреттөө',
    'equivalent-fractions-comparing-inequality': 'Барабарсыздык белгилери менен салыштыруу',
    'equivalent-fractions-with-calculations': 'Эсептөөлөр менен',

    # Бөлчөктөр > Туюнтуу (Expressing) - none of these 2 have a real
    # hand-built page yet.
    'expressing-quantity': 'Чоңдук',
    'expressing-change': 'Өзгөрүү',

    # Даражалар жана тамырлар > Тамырлар менен эсептөөлөр (Surds) - none
    # of these 8 have a real hand-built page yet.
    'surds-simplifying': 'Жөнөкөйлөтүү',
    'surds-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'surds-adding-subtracting': 'Кошуу жана кемитүү',
    'surds-expanding-brackets': 'Кашаны ачуу',
    'surds-rationalising-without-conjugates': 'Рационалдаштыруу: коньюгатасыз',
    'surds-rationalising-denominators': 'Бөлүүчүнү рационалдаштыруу',
    'surds-mixed': 'Аралаш',
    'surds-with-pythagoras': 'Пифагор менен',
}


def operation_placeholder_view(request, operation_slug):
    try:
        page_title = OPERATION_PLACEHOLDER_TITLES[operation_slug]
    except KeyError:
        raise Http404('Unknown operation')
    return render(
        request,
        'resources/onduktar/operation_placeholder.html',
        {'page_title': page_title},
    )
