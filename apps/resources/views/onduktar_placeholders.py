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

    # Даражалар жана тамырлар > Даражалар (Indices) - none of these 11
    # have a real hand-built page yet.
    'indices-introduction': 'Киришүү',
    'indices-square-numbers': 'Квадрат сандар',
    'indices-cube-numbers': 'Куб сандар',
    'indices-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'indices-negative': 'Терс даража',
    'indices-fractional': 'Бөлчөк даража',
    'indices-negative-fractional': 'Терс бөлчөк даража',
    'indices-with-brackets': 'Кашалар менен',
    'indices-mixed': 'Аралаш',
    'indices-equations': 'Даражалар менен теңдемелер',
    'indices-reciprocals': 'Тескери сандар',

    # Даражалар жана тамырлар > Тамырларды эсептөө (Evaluating Roots) -
    # none of these 3 have a real hand-built page yet.
    'evaluating-roots-estimating': 'Тамырларды болжолдоо',
    'evaluating-roots-square': 'Квадрат',
    'evaluating-roots-square-cube': 'Квадрат жана куб',

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

    # Бүтүн сандар > Эсептөөлөр: 1 жана 2 орундук - none of these 8 have
    # a real hand-built page yet.
    'integers-adding-1-2-digit': 'Кошуу',
    'integers-subtracting-1-2-digit': 'Кемитүү',
    'integers-adding-subtracting-1-2-digit': 'Кошуу жана кемитүү',
    'integers-multiplying-1-2-digit': 'Көбөйтүү',
    'integers-dividing-1-2-digit': 'Бөлүү',
    'integers-multiplying-dividing-1-2-digit': 'Көбөйтүү жана бөлүү',
    'integers-multiplying-dividing-10-100-1000': '10, 100, 1000гө көбөйтүү жана бөлүү',
    'integers-mixed-1-2-digit': 'Аралаш',

    # Бүтүн сандар > Эсептөөлөр: 2 жана 3 орундук - none of these 7 have
    # a real hand-built page yet.
    'integers-adding-2-3-digit': 'Кошуу',
    'integers-subtracting-2-3-digit': 'Кемитүү',
    'integers-adding-subtracting-2-3-digit': 'Кошуу жана кемитүү',
    'integers-multiplying-2-3-digit': 'Көбөйтүү',
    'integers-dividing-2-3-digit': 'Бөлүү',
    'integers-multiplying-dividing-2-3-digit': 'Көбөйтүү жана бөлүү',
    'integers-mixed-2-3-digit': 'Аралаш',

    # Бүтүн сандар > Эсептөөлөр: ондуктар менен - none of these 8 have a
    # real hand-built page yet.
    'integers-adding-with-decimals': 'Кошуу',
    'integers-subtracting-with-decimals': 'Кемитүү',
    'integers-adding-subtracting-with-decimals': 'Кошуу жана кемитүү',
    'integers-multiplying-with-decimals': 'Көбөйтүү',
    'integers-dividing-with-decimals': 'Бөлүү',
    'integers-multiplying-dividing-with-decimals': 'Көбөйтүү жана бөлүү',
    'integers-mixed-with-decimals': 'Аралаш',
    'integers-dividing-divisor-less-than-1-with-decimals': 'Бөлүүчүсү 1ден кичине бөлүү',

    # Бүтүн сандар > Турмуштук маселелер - neither of these 2 have a real
    # hand-built page yet.
    'integers-real-life-calculator': 'Калькулятор менен',
    'integers-real-life-non-calculator': 'Калькуляторсуз',

    # Өлчөмдөр > Татаал өлчөмдөр (Compound) - none of these 7 have a real
    # hand-built page yet.
    'compound-area-volume-conversion': 'Аянт жана көлөм бирдиктерин алмаштыруу',
    'compound-density-mass-volume': 'Тыгыздык, масса жана көлөм',
    'compound-work-hours': 'Жумуш-сааттар',
    'compound-population-density': 'Калктын калыңдыгы',
    'compound-pressure-force-area': 'Басым, күч жана аянт',
    'compound-rates-of-pay': 'Эмгек акы ставкалары',
    # Renamed from "Ылдамдык, аралык жана убакыт" - this url_name now
    # belongs to the "Introduction" child of the Speed, Distance & Time
    # category (see PROMOTE_LEAVES in rebuild_decimals_1_digit.py),
    # which took over the category's old title as its own nav label.
    'compound-speed-distance-time': 'Киришүү',

    # Өлчөмдөр > Акча - none of these 5 have a real hand-built page yet.
    'measures-money-purchasing-calculator': 'Сатып алуу: калькулятор менен',
    'measures-money-purchasing-non-calculator': 'Сатып алуу: калькуляторсуз',
    'measures-money-hire-purchase': 'Насыяга сатып алуу',
    'measures-money-bills-statements': 'Эсептер жана көчүрмөлөр',
    'measures-money-rates-of-pay': 'Эмгек акы ставкалары',

    # Өлчөмдөр > Масштабдуу сүрөттөр - none of these 4 have a real
    # hand-built page yet.
    'scale-drawings-lengths': 'Узундуктар',
    'scale-drawings-estimation': 'Болжолдоо',
    'scale-drawings-with-bearings': 'Багыттар менен',
    'scale-drawings-areas': 'Аянттар',

    # Өлчөмдөр > Өлчөө системалары - none of these 4 have a real
    # hand-built page yet.
    'systems-of-measurement-imperial': 'Империялык система',
    'systems-of-measurement-metric': 'Метрикалык система',
    'systems-of-measurement-mixed': 'Аралаш',
    'systems-of-measurement-conversion-factors': 'Айландыруу коэффициенттери',

    # Өлчөмдөр > Аянт жана көлөм бирдиктерин алмаштыруу (the top-level
    # sibling, distinct from Compound's own child of the same name) -
    # none of these 3 have a real hand-built page yet.
    'area-volume-conversion-area': 'Аянт',
    'area-volume-conversion-volume': 'Көлөм',
    'area-volume-conversion-mixed': 'Аралаш',

    # Өлчөмдөр > Убакыт (Time) - none of these 5 have a real hand-built
    # page yet.
    'time-reading-clocks': 'Саатты окуу',
    'time-days-months-years': 'Күндөр, айлар жана жылдар',
    'time-timetables': 'Жүрүш тартиби',
    'time-calculations': 'Эсептөөлөр',
    'time-converting': 'Айландыруу',

    # Татаал өлчөмдөр > Ылдамдык, аралык жана убакыт (Speed, Distance &
    # Time, promoted to a category) - none of these 3 new children have
    # a real hand-built page yet.
    'speed-distance-time-converting-speeds': 'Ылдамдыкты айландыруу',
    'speed-distance-time-two-stage-journeys': 'Эки этаптуу саякаттар',
    'speed-distance-time-relative-speeds': 'Салыштырмалуу ылдамдыктар',

    # Стандарттык форма > Көбөйтүү жана бөлүү - neither of these 2 have a
    # real hand-built page yet.
    'standard-form-multiplying-dividing-calculator': 'Калькулятор менен',
    'standard-form-multiplying-dividing-non-calculator': 'Калькуляторсуз',

    # Стандарттык форма > Айландыруу - none of these 3 have a real
    # hand-built page yet.
    'standard-form-converting-ordinary-to-standard': 'Жөнөкөйдөн стандарттык формага',
    'standard-form-converting-standard-to-ordinary': 'Стандарттык формадан жөнөкөйгө',
    'standard-form-converting-mixed': 'Аралаш',

    # Пропорция > Түз жана тескери пропорция - none of these 5 have a
    # real hand-built page yet.
    'direct-inverse-introduction': 'Киришүү',
    'direct-inverse-direct': 'Түз пропорция',
    'direct-inverse-inverse': 'Тескери пропорция',
    'direct-inverse-mixed': 'Аралаш',
    'direct-inverse-identifying-graphs': 'Графиктерди аныктоо',

    # Пропорция > Графиктер (Graphs) - none of these 10 have a real
    # hand-built page yet.
    'graphs-identifying-proportional': 'Пропорционалдуу графиктерди аныктоо',
    'graphs-conversion-graphs': 'Айландыруу графиктери',
    'graphs-cost-relationships': 'Баа мамилелери',
    'graphs-depth-time': 'Тереңдик-убакыт',
    'graphs-volume-time': 'Көлөм-убакыт',
    'graphs-mixed': 'Аралаш',
    'graphs-distance-time-constant-speeds': 'Аралык-убакыт: туруктуу ылдамдыктар',
    'graphs-distance-time-variable-speeds': 'Аралык-убакыт: өзгөрмө ылдамдыктар',
    'graphs-velocity-time': 'Ылдамдык-убакыт',
    'graphs-mixed-distance-velocity': 'Аралаш: аралык жана ылдамдык',

    # Графиктер > Айландыруу графиктери - neither of these 2 have a real
    # hand-built page yet.
    'graphs-conversion-reading': 'Окуу',
    'graphs-conversion-plotting-reading': 'Тургузуу жана окуу',

    # Графиктер > Баа мамилелери - neither of these 2 have a real
    # hand-built page yet.
    'graphs-cost-introduction': 'Киришүү',
    'graphs-cost-with-equations': 'Теңдемелер менен',

    # Графиктер > Аралык-убакыт: туруктуу ылдамдыктар - neither of these
    # 2 have a real hand-built page yet.
    'graphs-distance-time-reading': 'Окуу',
    'graphs-distance-time-plotting-reading': 'Тургузуу жана окуу',

    # Графиктер > Ылдамдык-убакыт - none of these 3 have a real
    # hand-built page yet.
    'graphs-velocity-time-distance': 'Аралык',
    'graphs-velocity-time-acceleration': 'Ылдамдануу',
    'graphs-velocity-time-mixed': 'Аралаш',

    # Пайыздар: калькулятор менен > Туюнтуу - none of these 3 have a real
    # hand-built page yet.
    'percentages-expressing-converting-fractions': 'Бөлчөктөрдү айландыруу',
    'percentages-expressing-quantity': 'Чоңдук',
    'percentages-expressing-change': 'Өзгөрүү',

    # Пайыздар: калькулятор менен > Чоңдуктун пайызы - none of these 4
    # have a real hand-built page yet.
    'percentages-quantity-integer': 'Бүтүн сан',
    'percentages-quantity-decimal': 'Ондук бөлчөк',
    'percentages-quantity-reverse': 'Тескери',
    'percentages-quantity-fpr': 'Бөлчөк, пайыз жана катыш',

    # Пайыздар: калькулятор менен > Көбөйтүү жана азайтуу - none of these
    # 7 have a real hand-built page yet.
    'percentages-incdec-increase': 'Көбөйтүү',
    'percentages-incdec-decrease': 'Азайтуу',
    'percentages-incdec-mixed': 'Аралаш',
    'percentages-incdec-simple-interest': 'Жөнөкөй пайыз',
    'percentages-incdec-using-multiplier': 'Көбөйтүүчү менен',
    'percentages-incdec-reverse': 'Тескери',
    'percentages-incdec-marginal-tax': 'Чектик салык',

    # Пайыздар: калькулятор менен > Кайталанма пайыздык өзгөрүү - none of
    # these 5 have a real hand-built page yet.
    'percentages-repeated-change-increase-compound-interest': 'Көбөйтүү жана татаал пайыз',
    'percentages-repeated-change-decrease': 'Азайтуу',
    'percentages-repeated-change-increase-decrease': 'Көбөйтүү жана азайтуу',
    'percentages-repeated-change-reverse': 'Тескери',
    'percentages-repeated-change-mixed': 'Аралаш',

    # Пайыздар: калькулятордсуз > Туюнтуу - only 2 have a real
    # hand-built page yet ("Converting Fractions" is mirrored in via
    # MIRROR_NODES, not a flat leaf here).
    'percentages-noncalc-expressing-quantity': 'Чоңдук',
    'percentages-noncalc-expressing-change': 'Өзгөрүү',

    # Пайыздар: калькулятордсуз > Чоңдуктун пайызы - none of these 6
    # have a real hand-built page yet.
    'percentages-noncalc-quantity-10s': '10дор менен',
    'percentages-noncalc-quantity-5s': '5тер менен',
    'percentages-noncalc-quantity-integer-decimal': 'Бүтүн сан жана ондук бөлчөк',
    'percentages-noncalc-quantity-reverse': 'Тескери',
    'percentages-noncalc-quantity-fpr': 'Бөлчөк, пайыз жана катыш',
    'percentages-noncalc-quantity-fpr-frequency-trees': 'Бөлчөк, пайыз жана катыш: жыштык дарактары менен',

    # Пайыздар: калькулятордсуз > Көбөйтүү жана азайтуу - none of these 4
    # have a real hand-built page yet.
    'percentages-noncalc-incdec-increase': 'Көбөйтүү',
    'percentages-noncalc-incdec-decrease': 'Азайтуу',
    'percentages-noncalc-incdec-mixed': 'Аралаш',
    'percentages-noncalc-incdec-reverse': 'Тескери',

    # Катыш > Туюнтуу - all 3 slots, none with a real page yet.
    'ratio-expressing-division': 'Бөлүү',
    'ratio-expressing-simplifying': 'Жөнөкөйлөтүү',
    'ratio-expressing-1-to-n': '1:n',

    # Катыш > Катыштар жана чоңдуктар - only Reverse/Mixed are flat
    # leaves here ("Катышка бөлүү" is its own chevron-bearing child, see
    # below).
    'ratio-quantities-reverse': 'Тескери',
    'ratio-quantities-mixed': 'Аралаш',

    # Катыш > Катыштар жана чоңдуктар > Катышка бөлүү - all 4 slots,
    # none with a real page yet.
    'ratio-dividing-with-line-segments': 'Сызык кесиндилери менен',
    'ratio-dividing-fpr-calculator': 'Бөлчөк, пайыз жана катыш: калькулятор менен',
    'ratio-dividing-fpr-non-calculator': 'Бөлчөк, пайыз жана катыш: калькулятордсуз',
    'ratio-dividing-fpr-frequency-trees': 'Бөлчөк, пайыз жана катыш: жыштык дарактары менен',

    # Катыш > Түрлөндүрүү - all 4 slots, none with a real page yet.
    'ratio-manipulation-1-to-n': '1:n',
    'ratio-manipulation-comparing-parts': 'Бөлүктөрдү салыштыруу',
    'ratio-manipulation-combining': 'Бириктирүү',
    'ratio-manipulation-changing': 'Өзгөртүү',

    # Катыш > Аралаш - both slots, none with a real page yet.
    'ratio-mixed-foundation': 'Негизги деңгээл',
    'ratio-mixed-higher': 'Жогорку деңгээл',

    # Турмуштук колдонуулар > Баалар - both slots, none with a real
    # page yet.
    'real-life-prices-calculator': 'Калькулятор менен',
    'real-life-prices-non-calculator': 'Калькулятордсуз',

    # Турмуштук колдонуулар > Пайдалуу сатып алуу - both slots, none
    # with a real page yet.
    'real-life-best-buys-calculator': 'Калькулятор менен',
    'real-life-best-buys-non-calculator': 'Калькулятордсуз',

    # Турмуштук колдонуулар > Валюта курстары - both slots, none with a
    # real page yet.
    'real-life-exchange-rates-calculator': 'Калькулятор менен',
    'real-life-exchange-rates-non-calculator': 'Калькулятордсуз',

    # Турмуштук колдонуулар > Рецепттер - both slots, none with a real
    # page yet.
    'real-life-recipes-calculator': 'Калькулятор менен',
    'real-life-recipes-non-calculator': 'Калькулятордсуз',

    # Турмуштук колдонуулар > Аралаш - both slots, none with a real
    # page yet.
    'real-life-mixed-calculator': 'Калькулятор менен',
    'real-life-mixed-non-calculator': 'Калькулятордсуз',
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
