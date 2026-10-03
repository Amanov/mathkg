from django.http import Http404
from django.shortcuts import render

# Placeholder slots of Decimals > Arithmetic: 1 Digit. Кошуу and Кемитүү
# are real card pages (koshuu_1_digit_view, subtracting_1_digit_view);
# the rest have no material yet. Shares that page's exact visual chrome (see
# templates/resources/onduktar/operation_placeholder.html) so navigating
# between a real operation and a "coming soon" one feels like the same
# page family, not two different systems. Each gets its own short URL
# (config/urls.py), matching koshuu-1-digit/'s own convention, instead of
# the long generic /resources/topic/number/... path.
OPERATION_PLACEHOLDER_TITLES = {
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
    # none of these 4 have a real hand-built page yet.
    'area-volume-conversion-area': 'Аянт',
    'area-volume-conversion-volume': 'Көлөм',
    'area-volume-conversion-mixed': 'Аралаш',
    'area-volume-conversion-scale-areas': 'Масштабдуу аянттар',

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

    # Пайыздар: калькуляторсуз > Туюнтуу - only 2 have a real
    # hand-built page yet ("Converting Fractions" is mirrored in via
    # MIRROR_NODES, not a flat leaf here).
    'percentages-noncalc-expressing-quantity': 'Чоңдук',
    'percentages-noncalc-expressing-change': 'Өзгөрүү',

    # Пайыздар: калькуляторсуз > Чоңдуктун пайызы - none of these 6
    # have a real hand-built page yet.
    'percentages-noncalc-quantity-10s': '10дор менен',
    'percentages-noncalc-quantity-5s': '5тер менен',
    'percentages-noncalc-quantity-integer-decimal': 'Бүтүн сан жана ондук бөлчөк',
    'percentages-noncalc-quantity-reverse': 'Тескери',
    'percentages-noncalc-quantity-fpr': 'Бөлчөк, пайыз жана катыш',
    'percentages-noncalc-quantity-fpr-frequency-trees': 'Бөлчөк, пайыз жана катыш: жыштык дарактары менен',

    # Пайыздар: калькуляторсуз > Көбөйтүү жана азайтуу - none of these 4
    # have a real hand-built page yet.
    'percentages-noncalc-incdec-increase': 'Көбөйтүү',
    'percentages-noncalc-incdec-decrease': 'Азайтуу',
    'percentages-noncalc-incdec-mixed': 'Аралаш',
    'percentages-noncalc-incdec-reverse': 'Тескери',

    # Катыш > Туюнтуу - all 3 slots, none with a real page yet.
    'ratio-expressing-division': 'Бөлүү',
    'ratio-expressing-simplifying': 'Жөнөкөйлөтүү',
    'ratio-expressing-1-to-n': '1:n',

    # Катыш > Катыштар жана чоңдуктар - all 7 are flat leaves at this
    # one level (an earlier pass wrongly nested the last 4 under
    # "Катышка бөлүү" as its own category).
    'ratio-dividing-into-a-ratio': 'Катышка бөлүү',
    'ratio-quantities-reverse': 'Тескери',
    'ratio-quantities-mixed': 'Аралаш',
    'ratio-dividing-with-line-segments': 'Сызык кесиндилери менен',
    'ratio-dividing-fpr-calculator': 'Бөлчөк, пайыз жана катыш: калькулятор менен',
    'ratio-dividing-fpr-non-calculator': 'Бөлчөк, пайыз жана катыш: калькуляторсуз',
    'ratio-dividing-fpr-frequency-trees': 'Бөлчөк, пайыз жана катыш: жыштык дарактары менен',

    # Катыш > Өзгөртүп түзүү - all 4 slots, none with a real page yet.
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
    'real-life-prices-non-calculator': 'Калькуляторсуз',

    # Турмуштук колдонуулар > Пайдалуу сатып алуу - both slots, none
    # with a real page yet.
    'real-life-best-buys-calculator': 'Калькулятор менен',
    'real-life-best-buys-non-calculator': 'Калькуляторсуз',

    # Турмуштук колдонуулар > Валюта курстары - both slots, none with a
    # real page yet.
    'real-life-exchange-rates-calculator': 'Калькулятор менен',
    'real-life-exchange-rates-non-calculator': 'Калькуляторсуз',

    # Турмуштук колдонуулар > Рецепттер - both slots, none with a real
    # page yet.
    'real-life-recipes-calculator': 'Калькулятор менен',
    'real-life-recipes-non-calculator': 'Калькуляторсуз',

    # Турмуштук колдонуулар > Аралаш - both slots, none with a real
    # page yet.
    'real-life-mixed-calculator': 'Калькулятор менен',
    'real-life-mixed-non-calculator': 'Калькуляторсуз',

    # Алгебра > Киришүү - all 3 flat slots, none with a real page yet.
    'algebra-intro-definitions': 'Аныктамалар',
    'algebra-intro-notation': 'Белгилөөлөр',
    'algebra-intro-manipulating-formulae': 'Формулаларды түрлөндүрүү',

    # Алгебра > Киришүү > Туюнтмаларды түзүү - all 3 slots, none with a
    # real page yet.
    'algebra-forming-expr-function-machines': 'Функция машиналары менен',
    'algebra-forming-expr-linear': 'Сызыктуу',
    'algebra-forming-expr-quadratic': 'Квадраттык',

    # Алгебра > Теңдемелер: сызыктуу - all 8 flat slots, none with a
    # real page yet.
    'algebra-linear-forming': 'Түзүү',
    'algebra-linear-variable-one-side-calculator': 'Белгисиз бир жагында: калькулятор менен',
    'algebra-linear-variable-one-side-non-calculator': 'Белгисиз бир жагында: калькуляторсуз',
    'algebra-linear-variable-both-sides': 'Белгисиз эки жагында',
    'algebra-linear-rational': 'Рационалдык',
    'algebra-linear-mixed': 'Аралаш',
    'algebra-linear-inequalities': 'Барабарсыздыктар',
    'algebra-linear-unknown-indices': 'Белгисиз даражалар менен',

    # Алгебра > Теңдемелер: квадраттык - all 13 slots, none with a real
    # page yet.
    'algebra-quadratic-forming': 'Түзүү',
    'algebra-quadratic-factorisation-double-brackets': 'Көбөйтүүчүлөргө ажыратуу: эки кашаа менен',
    'algebra-quadratic-b-zero': 'b = 0',
    'algebra-quadratic-c-zero': 'c = 0',
    'algebra-quadratic-completing-square': 'Толук квадратка келтирүү',
    'algebra-quadratic-rational': 'Рационалдык',
    'algebra-quadratic-formula': 'Квадраттык теңдеме формуласы',
    'algebra-quadratic-no-solution': 'Чечими жок теңдемелер',
    'algebra-quadratic-mixed': 'Аралаш',
    'algebra-quadratic-trial-improvement': 'Сыноо жана жакшыртуу',
    'algebra-quadratic-iteration': 'Кайталануу',
    'algebra-quadratic-by-intersection': 'Кесилишүү аркылуу',
    'algebra-quadratic-inequalities': 'Барабарсыздыктар',

    # Алгебра > Теңдемелер: системасы - all 5 flat slots, none with a
    # real page yet.
    'algebra-simultaneous-forming': 'Түзүү',
    'algebra-simultaneous-substitution': 'Алмаштыруу',
    'algebra-simultaneous-mixed': 'Аралаш',
    'algebra-simultaneous-graphically': 'Графикалык жол менен',
    'algebra-simultaneous-linear-non-linear': 'Сызыктуу жана сызыктуу эмес',

    # Теңдемелер: сызыктуу > Кашаа менен - all 3 slots, none with a
    # real page yet.
    'algebra-linear-brackets-without-coefficients': 'Коэффициентсиз',
    'algebra-linear-brackets-with-coefficients': 'Коэффициент менен',
    'algebra-linear-brackets-multiple': 'Бир нече',

    # Теңдемелер: сызыктуу > Түзүү - all 3 slots, none with a real page
    # yet.
    'algebra-linear-forming-shapes-angles-real-life': 'Фигуралар, бурчтар жана турмуштук маселелер',
    'algebra-linear-forming-function-machines': 'Функция машиналары менен',
    'algebra-linear-forming-functions-sequences': 'Функциялар жана ырааттуулуктар менен',

    # Теңдемелер: сызыктуу > Белгисиз бир жагында: калькулятор менен -
    # all 4 slots, none with a real page yet.
    'algebra-linear-var1side-calc-1step': '1-кадам',
    'algebra-linear-var1side-calc-2step': '2-кадам',
    'algebra-linear-var1side-calc-3step': '3-кадам',
    'algebra-linear-var1side-calc-mixed': 'Аралаш',

    # Теңдемелер: сызыктуу > Белгисиз бир жагында: калькуляторсуз - all
    # 4 slots, none with a real page yet.
    'algebra-linear-var1side-noncalc-1step': '1-кадам',
    'algebra-linear-var1side-noncalc-2step': '2-кадам',
    'algebra-linear-var1side-noncalc-3step': '3-кадам',
    'algebra-linear-var1side-noncalc-rational': 'Рационалдык',

    # Теңдемелер: сызыктуу > Белгисиз эки жагында - all 4 slots, none
    # with a real page yet.
    'algebra-linear-var-both-sides-without-brackets': 'Кашаасыз',
    'algebra-linear-var-both-sides-with-brackets': 'Кашаа менен',
    'algebra-linear-var-both-sides-graphical-intersections': 'Графиктердин кесилиши',
    'algebra-linear-var-both-sides-parallel-lines': 'Параллель сызыктар менен',

    # Теңдемелер: квадраттык > Көбөйтүүчүлөргө ажыратуу: эки кашаа
    # менен - both slots, none with a real page yet.
    'algebra-quadratic-factorisation-without-coefficients': 'Коэффициентсиз',
    'algebra-quadratic-factorisation-with-coefficients': 'Коэффициент менен',

    # Теңдемелер: квадраттык > b = 0 - all 3 slots, none with a real
    # page yet.
    'algebra-quadratic-b-zero-rearranging': 'Кайра жайгаштыруу',
    'algebra-quadratic-b-zero-difference-of-squares': 'Эки квадраттын айырмасы',
    'algebra-quadratic-b-zero-mixed': 'Аралаш',

    # Теңдемелер: квадраттык > Рационалдык - both slots, none with a
    # real page yet.
    'algebra-quadratic-rational-without-coefficients': 'Коэффициентсиз',
    'algebra-quadratic-rational-with-coefficients': 'Коэффициент менен',

    # Теңдемелер: системасы > Жоюу ыкмасы - all 3 slots, none with a
    # real page yet.
    'algebra-simultaneous-elimination-without-balancing': 'Коэффициенттерди теңдөөсүз',
    'algebra-simultaneous-elimination-with-balancing': 'Коэффициенттерди теңдөө менен',
    'algebra-simultaneous-elimination-negative-only': 'Терс коэффициенттер гана',

    # Теңдемелер: системасы > Сызыктуу жана сызыктуу эмес - both slots,
    # none with a real page yet.
    'algebra-simultaneous-linear-non-linear-algebraically': 'Алгебралык жол менен',
    'algebra-simultaneous-linear-non-linear-graphically': 'Графикалык жол менен',

    # Функциялар - "ЖРТ" flat slot (localized from the reference's
    # "IGCSE"), none with a real page yet.
    'algebra-functions-igcse': 'ЖРТ',

    # Функциялар > Түзүү - all 7 slots, none with a real page yet.
    'algebra-functions-forming-expressions': 'Туюнтмалар',
    'algebra-functions-forming-simple-functions': 'Жөнөкөй функциялар',
    'algebra-functions-forming-changing-subject': 'Формуланын өзгөрмөсүн алмаштыруу',
    'algebra-functions-forming-composite-linear': 'Татаал функция: сызыктуу',
    'algebra-functions-forming-inverse': 'Тескери функция',
    'algebra-functions-forming-composite-inverse': 'Татаал жана тескери функциялар',
    'algebra-functions-forming-composite-quadratics': 'Татаал функция: квадраттык менен',

    # Функциялар > Маанисин эсептөө - all 10 slots, none with a real
    # page yet.
    'algebra-functions-evaluating-simple-machines': 'Жөнөкөй функция машиналары',
    'algebra-functions-evaluating-graphing': 'Графигин түзүү',
    'algebra-functions-evaluating-equations-sequences': 'Теңдемелер жана ырааттуулуктар менен',
    'algebra-functions-evaluating-linear': 'Сызыктуу',
    'algebra-functions-evaluating-indices': 'Даражалар менен',
    'algebra-functions-evaluating-composite': 'Татаал функция',
    'algebra-functions-evaluating-inverse': 'Тескери функция',
    'algebra-functions-evaluating-composite-inverse': 'Татаал жана тескери функциялар',
    'algebra-functions-evaluating-solving-equations': 'Теңдемелерди чечүү',
    'algebra-functions-evaluating-iteration': 'Кайталануу',

    # Графиктер: абстракттуу - 5 flat slots, none with a real page yet.
    # The other 5 reference items (Quadratic, Circles, Other
    # Non-Linear, Transformations, Differentiation) are chevron-bearing
    # categories left empty pending screenshots of their own contents.
    'algebra-graphs-abstract-coordinates': 'Координаттар',
    'algebra-graphs-abstract-linear-calculating': 'Сызыктуу: эсептөө',
    'algebra-graphs-abstract-linear-plotting': 'Сызыктуу: чиймелөө',
    'algebra-graphs-abstract-linear-reading': 'Сызыктуу: окуу',
    'algebra-graphs-abstract-linear-mixed': 'Сызыктуу: аралаш',

    # Графиктер: турмуштук - 4 flat slots, none with a real page yet.
    # The other 5 reference items (Conversion Graphs, Cost
    # Relationships, Distance-Time: Constant/Variable Speeds,
    # Velocity-Time) are chevron-bearing categories left empty pending
    # screenshots of their own contents.
    'algebra-graphs-real-life-depth-time': 'Тереңдик-Убакыт',
    'algebra-graphs-real-life-volume-time': 'Көлөм-Убакыт',
    'algebra-graphs-real-life-mixed': 'Аралаш',
    'algebra-graphs-real-life-mixed-distance-velocity': 'Аралаш: аралык жана ылдамдык',

    # Барабарсыздыктар - 2 flat slots, none with a real page yet. The
    # other 2 reference items (Linear, Graphical) are chevron-bearing
    # categories left empty pending screenshots of their own contents.
    'algebra-inequalities-quadratic': 'Квадраттык',
    'algebra-inequalities-trial-improvement': 'Сыноо жана жакшыртуу',

    # Өзгөртүп түзүү - 2 flat slots, none with a real page yet. The other
    # 9 reference items are chevron-bearing categories left empty
    # pending screenshots of their own contents.
    'algebra-manipulation-notation': 'Белгилөө',
    'algebra-manipulation-changing-subject': 'Формуланын өзгөрмөсүн алмаштыруу',

    # Ырааттуулуктар - 9 flat slots, none with a real page yet. The
    # remaining reference item (Linear) is a chevron-bearing category
    # left empty pending a screenshot of its own contents.
    'algebra-sequences-introduction': 'Киришүү',
    'algebra-sequences-with-graphs': 'Графиктер менен',
    'algebra-sequences-equations-functions': 'Теңдемелер жана функциялар менен',
    'algebra-sequences-quadratic': 'Квадраттык',
    'algebra-sequences-linear-quadratic': 'Сызыктуу жана квадраттык',
    'algebra-sequences-geometric': 'Геометриялык',
    'algebra-sequences-fibonacci': 'Фибоначчи',
    'algebra-sequences-special': 'Атайын',
    'algebra-sequences-mixed': 'Аралаш',

    # Ордуна коюу (renamed from "Коюу") - 2 flat slots, none with a
    # real page yet. The other 3 reference items (Using Symbols,
    # Without Indices, With Indices) are chevron-bearing categories
    # left empty pending screenshots of their own contents.
    'algebra-substitution-with-calculator': 'Калькулятор менен',
    'algebra-substitution-vectors': 'Векторлор',

    # Ордуна коюу > Белгилерди колдонуу / Даражасыз / Даража менен - 6
    # distinct Positive/Negative slots plus 1 shared Mixed slot (same
    # page, 3 nav locations), none with a real page yet.
    'algebra-substitution-symbols-positive': 'Оң',
    'algebra-substitution-symbols-negative': 'Терс',
    'algebra-substitution-without-indices-positive': 'Оң',
    'algebra-substitution-without-indices-negative': 'Терс',
    'algebra-substitution-with-indices-positive': 'Оң',
    'algebra-substitution-with-indices-negative': 'Терс',
    'algebra-substitution-mixed': 'Аралаш',

    # Графиктер: абстракттуу > Координаттар - all 6 slots, none with a
    # real page yet. "Координаттар" itself was previously a flat leaf
    # (see 'algebra-graphs-abstract-coordinates' above, now orphaned -
    # left in place, same as 'algebra-quadratic-rational') before a
    # further screenshot showed it has its own chevron children.
    'algebra-graphs-abstract-coordinates-reading': 'Окуу',
    'algebra-graphs-abstract-coordinates-reading-plotting': 'Окуу жана чиймелөө',
    'algebra-graphs-abstract-coordinates-midpoint-endpoint': 'Кесиндинин орто жана учтук чекиттери',
    'algebra-graphs-abstract-coordinates-segments-ratio': 'Кесиндилер жана катыш',
    'algebra-graphs-abstract-coordinates-geometric-problems': 'Геометриялык маселелер',
    'algebra-graphs-abstract-coordinates-with-pythagoras': 'Пифагор менен',

    # Графиктер: абстракттуу > Сызыктуу: эсептөө - 9 flat slots, none
    # with a real page yet. The remaining reference item (From
    # Coordinates) is a chevron-bearing category left empty pending a
    # screenshot of its own contents.
    'algebra-graphs-abstract-linear-calc-functions-graphs': 'Функциялар жана графиктер',
    'algebra-graphs-abstract-linear-calc-gradient-intercept': 'Кыйшаюусун жана кесилиш чекитин аныктоо',
    'algebra-graphs-abstract-linear-calc-evaluating-coordinates': 'Координаттарды эсептөө',
    'algebra-graphs-abstract-linear-calc-evaluating-intersections': 'Кесилишүүлөрдү эсептөө',
    'algebra-graphs-abstract-linear-calc-parallel': 'Параллель',
    'algebra-graphs-abstract-linear-calc-perpendicular': 'Перпендикуляр',
    'algebra-graphs-abstract-linear-calc-parallel-perpendicular': 'Параллель жана перпендикуляр',
    'algebra-graphs-abstract-linear-calc-mixed': 'Аралаш',
    'algebra-graphs-abstract-linear-calc-identifying-graphs': 'Графиктерди аныктоо',

    # Графиктер: абстракттуу > Сызыктуу: чиймелөө - all 8 slots, none
    # with a real page yet.
    'algebra-graphs-abstract-linear-plot-with-functions': 'Функциялар менен',
    'algebra-graphs-abstract-linear-plot-with-sequences': 'Ырааттуулуктар менен',
    'algebra-graphs-abstract-linear-plot-cover-up': 'Жабуу ыкмасы',
    'algebra-graphs-abstract-linear-plot-gradient': 'Сызыктын кыйшаюусу',
    'algebra-graphs-abstract-linear-plot-gradient-intercept-method': 'Кыйшаюу-кесилиш ыкмасы',
    'algebra-graphs-abstract-linear-plot-table-of-values': 'Маанилер таблицасы ыкмасы',
    'algebra-graphs-abstract-linear-plot-inequalities': 'Барабарсыздыктар',
    'algebra-graphs-abstract-linear-plot-simultaneous': 'Теңдемелер системасы',

    # Графиктер: абстракттуу > Сызыктуу: окуу - only 4 slots built so
    # far (reference screenshot was cut off after these - a 5th row
    # read "Identifying..." with nothing after, flagged to the user).
    'algebra-graphs-abstract-linear-read-horizontal-vertical': 'Горизонталдык жана вертикалдык',
    'algebra-graphs-abstract-linear-read-gradient': 'Сызыктын кыйшаюусу',
    'algebra-graphs-abstract-linear-read-equation': 'Сызыктын теңдемеси',
    'algebra-graphs-abstract-linear-read-evaluating-intersections': 'Кесилишүүлөрдү эсептөө',

    # Графиктер: абстракттуу > Квадраттык - all 5 slots, none with a
    # real page yet.
    'algebra-graphs-abstract-quadratic-plotting': 'Чиймелөө',
    'algebra-graphs-abstract-quadratic-significant-points': 'Маанилүү чекиттер',
    'algebra-graphs-abstract-quadratic-turning-points': 'Толук квадратка келтирүү менен бурулуш чекиттери',
    'algebra-graphs-abstract-quadratic-solving-by-intersection': 'Кесилишүү аркылуу чечүү',
    'algebra-graphs-abstract-quadratic-simultaneous': 'Теңдемелер системасы',

    # Графиктер: абстракттуу > Тегеректер - both slots, none with a
    # real page yet.
    'algebra-graphs-abstract-circles-equation': 'Теңдеме',
    'algebra-graphs-abstract-circles-tangent': 'Жанама',

    # Графиктер: абстракттуу > Башка сызыктуу эмес - all 6 slots, none
    # with a real page yet.
    'algebra-graphs-abstract-other-nonlinear-plotting': 'Чиймелөө',
    'algebra-graphs-abstract-other-nonlinear-identifying-nonlinear': 'Аныктоо: сызыктуу эмес',
    'algebra-graphs-abstract-other-nonlinear-identifying-proportional': 'Аныктоо: пропорционалдык',
    'algebra-graphs-abstract-other-nonlinear-estimating-gradient': 'Кыйшаюуну болжолдоо',
    'algebra-graphs-abstract-other-nonlinear-exponential-functions': 'Көрсөткүчтүү функциялар',
    'algebra-graphs-abstract-other-nonlinear-trig-functions': 'Тригонометриялык функциялар',

    # Графиктер: абстракттуу > Өзгөртүүлөр - both slots, none with a
    # real page yet.
    'algebra-graphs-abstract-transformations-gcse': 'GCSE',
    'algebra-graphs-abstract-transformations-igcse': 'ЖРТ',

    # Графиктер: турмуштук > Айландыруу графиктери - 2 confirmed slots
    # (reference screenshot was cut off after these, flagged to the
    # user), none with a real page yet.
    'algebra-graphs-real-life-conversion-reading': 'Окуу',
    'algebra-graphs-real-life-conversion-plotting-reading': 'Чиймелөө жана окуу',

    # Графиктер: турмуштук > Баа катыштары - 2 confirmed slots (cut off
    # in the reference), none with a real page yet.
    'algebra-graphs-real-life-cost-introduction': 'Киришүү',
    'algebra-graphs-real-life-cost-with-equations': 'Теңдемелер менен',

    # Графиктер: турмуштук > Аралык-Убакыт: турактуу ылдамдык - 2
    # confirmed slots (cut off in the reference), none with a real page
    # yet.
    'algebra-graphs-real-life-distance-time-constant-reading': 'Окуу',
    'algebra-graphs-real-life-distance-time-constant-plotting-reading': 'Чиймелөө жана окуу',

    # Графиктер: турмуштук > Ылдамдык-Убакыт - all 3 slots, none with a
    # real page yet.
    'algebra-graphs-real-life-velocity-time-distance': 'Аралык',
    'algebra-graphs-real-life-velocity-time-acceleration': 'Ылдамдануу',
    'algebra-graphs-real-life-velocity-time-mixed': 'Аралаш',

    # Барабарсыздыктар > Сызыктуу - all 6 slots, none with a real page
    # yet.
    'algebra-inequalities-linear-forming': 'Түзүү',
    'algebra-inequalities-linear-evaluating': 'Эсептөө',
    'algebra-inequalities-linear-representing': 'Чагылдыруу',
    'algebra-inequalities-linear-solving-single': 'Чечүү: жалгыз',
    'algebra-inequalities-linear-solving-single-double': 'Чечүү: жалгыз жана кош',
    'algebra-inequalities-linear-mixed': 'Аралаш',

    # Барабарсыздыктар > Графикалык - 2 confirmed slots (reference
    # screenshot was cut off after these, flagged to the user).
    'algebra-inequalities-graphical-shade-wanted': 'Керектүү аймакты боёо',
    'algebra-inequalities-graphical-shade-unwanted': 'Керексиз аймакты боёо',

    # Өзгөртүп түзүү > Туюнтма түзүү - all 3 slots, none with a real page
    # yet.
    'algebra-manipulation-forming-function-machines': 'Функция машиналары менен',
    'algebra-manipulation-forming-linear': 'Сызыктуу',
    'algebra-manipulation-forming-quadratic': 'Квадраттык',

    # Өзгөртүп түзүү > Алгебралык бөлчөктөр - all 6 slots, none with a
    # real page yet.
    'algebra-manipulation-fractions-adding-subtracting': 'Кошуу жана кемитүү',
    'algebra-manipulation-fractions-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'algebra-manipulation-fractions-mixed': 'Аралаш',
    'algebra-manipulation-fractions-simplifying': 'Жөнөкөйлөтүү',
    'algebra-manipulation-fractions-simplifying-with-factorisation': 'Жөнөкөйлөтүү: көбөйтүүчүлөргө ажыратуу менен',
    'algebra-manipulation-fractions-simplifying-difference-squares': 'Жөнөкөйлөтүү: эки квадраттын айырмасы',

    # Өзгөртүп түзүү > Формуланын өзгөрмөсүн алмаштыруу (was previously a
    # flat leaf, see 'algebra-manipulation-changing-subject' above, now
    # orphaned - left in place, same as 'algebra-quadratic-rational')
    # before a further screenshot showed it has its own chevron
    # children - all 4 slots, none with a real page yet.
    'algebra-manipulation-changing-subject-manipulating-formulae': 'Формулаларды түрлөндүрүү',
    'algebra-manipulation-changing-subject-function-machine': 'Функция машинасын колдонуу',
    'algebra-manipulation-changing-subject-without-factorisation': 'Көбөйтүүчүлөргө ажыратуусуз',
    'algebra-manipulation-changing-subject-with-factorisation': 'Көбөйтүүчүлөргө ажыратуу менен',

    # Өзгөртүп түзүү > Бир кашааны ачуу - all 7 slots, none with a real
    # page yet.
    'algebra-manipulation-expand-single-without-coefficients': 'Коэффициентсиз',
    'algebra-manipulation-expand-single-with-coefficients': 'Коэффициент менен',
    'algebra-manipulation-expand-single-with-indices': 'Даражалар менен',
    'algebra-manipulation-expand-single-multiple': 'Көп кашаалар',
    'algebra-manipulation-expand-single-mixed': 'Аралаш',
    'algebra-manipulation-expand-single-factorisation-without-indices': 'Көбөйтүүчүлөргө ажыратуу менен: даражасыз',
    'algebra-manipulation-expand-single-factorisation-with-indices': 'Көбөйтүүчүлөргө ажыратуу менен: даража менен',

    # Өзгөртүп түзүү > Эки жана үч кашааны ачуу - all 7 slots, none with a
    # real page yet.
    'algebra-manipulation-expand-double-triple-double-without-coefficients': 'Эки кашаа: коэффициентсиз',
    'algebra-manipulation-expand-double-triple-double-with-coefficients': 'Эки кашаа: коэффициент менен',
    'algebra-manipulation-expand-double-triple-with-factorisation': 'Көбөйтүүчүлөргө ажыратуу менен',
    'algebra-manipulation-expand-double-triple-squares': 'Квадраттар',
    'algebra-manipulation-expand-double-triple-triple': 'Үч кашаа',
    'algebra-manipulation-expand-double-triple-mixed': 'Аралаш ачуу',
    'algebra-manipulation-expand-double-triple-with-surds': 'Тамырлар менен',

    # Өзгөртүп түзүү > Бир кашаага ажыратуу - both slots, none with a
    # real page yet.
    'algebra-manipulation-factorise-single-without-indices': 'Даражасыз',
    'algebra-manipulation-factorise-single-with-indices': 'Даража менен',

    # Өзгөртүп түзүү > Эки кашаага ажыратуу - all 7 slots, none with a
    # real page yet.
    'algebra-manipulation-factorise-double-quadratic-without-coefficients': 'Квадраттык: коэффициентсиз',
    'algebra-manipulation-factorise-double-quadratic-with-coefficients': 'Квадраттык: коэффициент менен',
    'algebra-manipulation-factorise-double-with-expanding': 'Ачуу менен',
    'algebra-manipulation-factorise-double-completing-square': 'Толук квадратка келтирүү',
    'algebra-manipulation-factorise-double-difference-squares': 'Эки квадраттын айырмасы',
    'algebra-manipulation-factorise-double-mixed': 'Аралаш ажыратуу',
    'algebra-manipulation-factorise-double-grouping': 'Топтоштуруу',

    # Өзгөртүп түзүү > Белгилөө (was previously a flat leaf, see
    # 'algebra-manipulation-notation' above, now orphaned - left in
    # place, same as 'algebra-quadratic-rational') before a further
    # screenshot showed it has its own chevron children - all 14
    # slots, none with a real page yet.
    'algebra-manipulation-notation-adding': 'Кошуу',
    'algebra-manipulation-notation-adding-brackets': 'Кошуу: кашаа менен',
    'algebra-manipulation-notation-adding-indices': 'Кошуу: даража менен',
    'algebra-manipulation-notation-multiplying': 'Көбөйтүү',
    'algebra-manipulation-notation-multiplying-adding': 'Көбөйтүү жана кошуу',
    'algebra-manipulation-notation-dividing': 'Бөлүү',
    'algebra-manipulation-notation-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'algebra-manipulation-notation-squared-cubed': 'Квадрат жана куб',
    'algebra-manipulation-notation-mixed-arithmetic': 'Аралаш арифметика',
    'algebra-manipulation-notation-negative-fractional-indices': 'Терс жана бөлчөк даражалар менен',
    'algebra-manipulation-notation-rational-with-factorisation': 'Рационалдык: көбөйтүүчүлөргө ажыратуу менен',
    'algebra-manipulation-notation-rational-difference-squares': 'Рационалдык: эки квадраттын айырмасы',
    'algebra-manipulation-notation-mixed': 'Аралаш',
    'algebra-manipulation-notation-mixed-all': 'Аралаш: баары',

    # Өзгөртүп түзүү > Бир кашаага ажыратуу - 2 more slots found on a
    # fuller screenshot (the first one missed these), none with a real
    # page yet.
    'algebra-manipulation-factorise-single-expanding-without-indices': 'Ачуу менен: даражасыз',
    'algebra-manipulation-factorise-single-expanding-with-indices': 'Ачуу менен: даража менен',

    # Өзгөртүп түзүү > Аралаш - both slots, none with a real page yet.
    'algebra-manipulation-mixed-foundation': 'Негизги деңгээл',
    'algebra-manipulation-mixed-higher': 'Жогорку деңгээл',

    # Ырааттуулуктар > Сызыктуу - all 4 slots, none with a real page
    # yet.
    'algebra-sequences-linear-introduction': 'Киришүү',
    'algebra-sequences-linear-evaluating-terms': 'Мүчөлөрдү эсептөө',
    'algebra-sequences-linear-from-2-terms': '2 мүчөдөн',
    'algebra-sequences-linear-summing': 'Суммалоо (ЖРТ)',

    # Өзгөртүп түзүү > Туюнтмаларды жөнөкөйлөтүү - all 13 slots, none
    # with a real page yet.
    'algebra-manipulation-expressions-adding': 'Кошуу',
    'algebra-manipulation-expressions-adding-brackets': 'Кошуу: кашаа менен',
    'algebra-manipulation-expressions-adding-indices': 'Кошуу: даража менен',
    'algebra-manipulation-expressions-multiplying': 'Көбөйтүү',
    'algebra-manipulation-expressions-multiplying-adding': 'Көбөйтүү жана кошуу',
    'algebra-manipulation-expressions-dividing': 'Бөлүү',
    'algebra-manipulation-expressions-multiplying-dividing': 'Көбөйтүү жана бөлүү',
    'algebra-manipulation-expressions-squared-cubed': 'Квадрат жана куб',
    'algebra-manipulation-expressions-mixed-arithmetic': 'Аралаш арифметика',
    'algebra-manipulation-expressions-negative-fractional-indices': 'Терс жана бөлчөк даражалар менен',
    'algebra-manipulation-expressions-rational-with-factorisation': 'Рационалдык: көбөйтүүчүлөргө ажыратуу менен',
    'algebra-manipulation-expressions-rational-difference-squares': 'Рационалдык: эки квадраттын айырмасы',
    'algebra-manipulation-expressions-mixed-all': 'Аралаш: баары',

    # Геометрия > Бурчтар > Бурч фактылары - 6 slots, none with a real
    # page yet.
    'geometry-angles-angle-facts-vocabulary': 'Терминология',
    'geometry-angles-angle-facts-around-a-point': 'Чекиттин тегерегинде',
    'geometry-angles-angle-facts-on-straight-lines': 'Түз сызыктарда',
    'geometry-angles-angle-facts-vertically-opposite': 'Вертикаль бурчтар',
    'geometry-angles-angle-facts-triangles': 'Үч бурчтуктар',
    'geometry-angles-angle-facts-mixed': 'Аралаш',

    # Геометрия > Бурчтар > Чийүү жана өлчөө - 4 slots, none with a
    # real page yet.
    'geometry-angles-drawing-measuring-drawing': 'Чийүү',
    'geometry-angles-drawing-measuring-measuring': 'Өлчөө',
    'geometry-angles-drawing-measuring-both': 'Чийүү жана өлчөө',
    'geometry-angles-drawing-measuring-estimating': 'Болжолдоо',

    # Геометрия > Бурчтар > Тегерек теоремалары - 10 slots, none with a
    # real page yet.
    'geometry-angles-circle-theorems-vocabulary': 'Терминология',
    'geometry-angles-circle-theorems-alternate-segment': 'Алмашма сегмент',
    'geometry-angles-circle-theorems-at-circumference': 'Тегеректин четинде',
    'geometry-angles-circle-theorems-cyclic-quadrilaterals': 'Циклдик төрт бурчтуктар',
    'geometry-angles-circle-theorems-tangents-chords': 'Жанамалар жана хордалар',
    'geometry-angles-circle-theorems-combined': 'Айкалышкан',
    'geometry-angles-circle-theorems-mixed': 'Аралаш',
    'geometry-angles-circle-theorems-with-pythagoras': 'Пифагор менен',
    'geometry-angles-circle-theorems-with-trigonometry': 'Тригонометрия менен',
    'geometry-angles-circle-theorems-intersecting-chords': 'Кесилишкен хордалар (ЖРТ)',

    # Геометрия > Бурчтар > Параллель сызыктар - 2 known slots
    # (screenshot was cut off), none with a real page yet.
    'geometry-angles-parallel-lines-introduction': 'Киришүү',
    'geometry-angles-parallel-lines-solving-equations': 'Теңдемелерди чечүү',

    # Геометрия > Бурчтар > Көп бурчтуктар - 5 flat slots plus "Аралаш"
    # category's own 2 slots, none with a real page yet.
    'geometry-angles-polygons-triangles': 'Үч бурчтуктар',
    'geometry-angles-polygons-quadrilaterals': 'Төрт бурчтуктар',
    'geometry-angles-polygons-special-quadrilaterals': 'Атайын төрт бурчтуктар',
    'geometry-angles-polygons-regular': 'Туура',
    'geometry-angles-polygons-irregular': 'Туура эмес',
    'geometry-angles-polygons-mixed-without-circle-theorems': 'Тегерек теоремаларысыз',
    'geometry-angles-polygons-mixed-with-circle-theorems': 'Тегерек теоремалары менен',

    # Геометрия > Азимут - all 5 slots, none with a real page yet.
    'geometry-bearings-cardinal-points': 'Негизги багыттар',
    'geometry-bearings-measuring': 'Өлчөө',
    'geometry-bearings-with-scale-drawings': 'Масштабдуу сүрөт менен',
    'geometry-bearings-calculating': 'Эсептөө',
    'geometry-bearings-with-trigonometry': 'Тригонометрия менен',

    # Геометрия > Координаттар - all 6 slots, none with a real page yet.
    'geometry-coordinates-reading': 'Окуу',
    'geometry-coordinates-reading-plotting': 'Окуу жана белгилөө',
    'geometry-coordinates-midpoint-endpoint': 'Кесиндинин орто жана чеки чекиттери',
    'geometry-coordinates-line-segments-ratio': 'Кесиндилер жана катыш',
    'geometry-coordinates-geometric-problems': 'Геометриялык маселелер',
    'geometry-coordinates-with-pythagoras': 'Пифагор менен',

    # Геометрия > Пифагор - 11 flat slots, none with a real page yet.
    'geometry-pythagoras-introduction': 'Киришүү',
    'geometry-pythagoras-finding-a-or-b': 'A же B табуу',
    'geometry-pythagoras-finding-a-b-or-c': 'A, B же C табуу',
    'geometry-pythagoras-isosceles-triangles': 'Тең бүйрүүчү үч бурчтуктар',
    'geometry-pythagoras-real-life': 'Турмуштук маселелер',
    'geometry-pythagoras-3d': '3D',
    'geometry-pythagoras-coordinates': 'Координаттар',
    'geometry-pythagoras-mixed': 'Аралаш',
    'geometry-pythagoras-shape-perimeters': 'Фигуралардын периметрлери',
    'geometry-pythagoras-with-surds': 'Тамырлар менен',
    'geometry-pythagoras-with-circle-theorems': 'Тегерек теоремалары менен',

    # Геометрия > Пифагор > Тригонометрия менен - 2 flat slots, none
    # with a real page yet.
    'geometry-pythagoras-with-trigonometry-or': 'Тригонометрия же Пифагор',
    'geometry-pythagoras-with-trigonometry-and': 'Тригонометрия жана Пифагор',

    # Геометрия > Окшоштук - "Окшош үч бурчтуктар" and "Узундук, аянт
    # жана көлөм масштаб көбөйткүчтөрү" turned out to be categories,
    # their url_name entries below are now orphaned (see urls.py).
    'geometry-similarity-similar-2d-shapes': 'Окшош 2D фигуралар',
    'geometry-similarity-similar-triangles': 'Окшош үч бурчтуктар',
    'geometry-similarity-congruent-triangles': 'Тең үч бурчтуктар',
    'geometry-similarity-length-area-volume-scale-factors': 'Узундук, аянт жана көлөм масштаб көбөйткүчтөрү',

    # Геометрия > Окшоштук > Окшош үч бурчтуктар - 2 flat slots, none
    # with a real page yet.
    'geometry-similarity-similar-triangles-abstract': 'Абстракттуу',
    'geometry-similarity-similar-triangles-real-life': 'Турмуштук',

    # Геометрия > Окшоштук > Узундук, аянт жана көлөм масштаб
    # көбөйткүчтөрү - 3 flat slots, none with a real page yet.
    'geometry-similarity-length-area-volume-scale-factors-length-area': 'Узундук жана аянт',
    'geometry-similarity-length-area-volume-scale-factors-length-volume': 'Узундук жана көлөм',
    'geometry-similarity-length-area-volume-scale-factors-length-area-volume': 'Узундук, аянт жана көлөм',

    # Геометрия > Өзгөртүүлөр > Чоңойтуу - 7 flat slots, none with a
    # real page yet.
    'geometry-transformations-enlargement-positive': 'Оң',
    'geometry-transformations-enlargement-negative': 'Терс',
    'geometry-transformations-enlargement-fractional': 'Бөлчөк',
    'geometry-transformations-enlargement-negative-fractional': 'Терс бөлчөк',
    'geometry-transformations-enlargement-ray-method': 'Нур ыкмасы',
    'geometry-transformations-enlargement-mixed-foundation': 'Аралаш: Негизги деңгээл',
    'geometry-transformations-enlargement-mixed-higher': 'Аралаш: Жогорку деңгээл',

    # Геометрия > Өзгөртүүлөр > Аралаш - 2 flat slots, none with a real
    # page yet.
    'geometry-transformations-mixed-foundation': 'Негизги деңгээл',
    'geometry-transformations-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Тригонометрия - 7 flat slots, none with a real page
    # yet.
    'geometry-trigonometry-introduction': 'Киришүү',
    'geometry-trigonometry-graphs': 'Графиктер',
    'geometry-trigonometry-choosing-a-ratio': 'Катышты тандоо',
    'geometry-trigonometry-isosceles-triangles': 'Тең бүйрүүчү үч бурчтуктар',
    'geometry-trigonometry-without-calculator': 'Калькуляторсуз',
    'geometry-trigonometry-with-circle-theorems': 'Тегерек теоремалары менен',
    'geometry-trigonometry-area-rule': 'Аянт эрежеси',

    # Геометрия > Тригонометрия > Синус жана косинус катыштары - 2 flat
    # slots, none with a real page yet.
    'geometry-trigonometry-sine-cosine-ratios-lengths': 'Узундуктар',
    'geometry-trigonometry-sine-cosine-ratios-angles': 'Бурчтар',

    # Геометрия > Тригонометрия > Тангенс катышы - 2 flat slots, none
    # with a real page yet.
    'geometry-trigonometry-tangent-ratio-lengths': 'Узундуктар',
    'geometry-trigonometry-tangent-ratio-angles': 'Бурчтар',

    # Геометрия > Тригонометрия > Бардык катыштар - 2 flat slots, none
    # with a real page yet.
    'geometry-trigonometry-all-ratios-lengths': 'Узундуктар',
    'geometry-trigonometry-all-ratios-angles': 'Бурчтар',

    # Геометрия > Тригонометрия > Бардык катыштар > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-trigonometry-all-ratios-mixed-or': 'Узундуктар же бурчтар',
    'geometry-trigonometry-all-ratios-mixed-and': 'Узундуктар жана бурчтар',

    # Геометрия > Тригонометрия > Турмуштук маселелер - 4 flat slots,
    # none with a real page yet.
    'geometry-trigonometry-real-life-elevation-depression': 'Көтөрүлүү жана түшүү бурчтары',
    'geometry-trigonometry-real-life-practical-problems': 'Практикалык маселелер',
    'geometry-trigonometry-real-life-3d': '3D',
    'geometry-trigonometry-real-life-with-bearings': 'Азимут менен',

    # Геометрия > Тригонометрия > Синус жана косинус эрежелери - 5 flat
    # slots, none with a real page yet.
    'geometry-trigonometry-sine-cosine-rules-sine-rule': 'Синус эрежеси',
    'geometry-trigonometry-sine-cosine-rules-cosine-rule-lengths': 'Косинус эрежеси: узундуктар',
    'geometry-trigonometry-sine-cosine-rules-cosine-rule-angles': 'Косинус эрежеси: бурчтар',
    'geometry-trigonometry-sine-cosine-rules-cosine-rule-mixed': 'Косинус эрежеси: аралаш',
    'geometry-trigonometry-sine-cosine-rules-solving-any-triangle': 'Каалаган үч бурчтукту чыгаруу',

    # Геометрия > Векторлор - all 5 slots, none with a real page yet.
    'geometry-vectors-translation': 'Жылдыруу',
    'geometry-vectors-expressing': 'Туюнтуу',
    'geometry-vectors-substitution': 'Коюу',
    'geometry-vectors-around-shapes': 'Фигуралардын тегерегинде',
    'geometry-vectors-proofs': 'Далилдөөлөр',

    # Геометрия > Көлөм жана бет аянты - 3 flat slots, none with a
    # real page yet.
    'geometry-volume-surface-area-vocabulary': 'Терминология',
    'geometry-volume-surface-area-introduction-to-volume': 'Көлөмгө киришүү',
    'geometry-volume-surface-area-nets': 'Жайылмалар',

    # Геометрия > Көлөм жана бет аянты > Конус - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-cone-volume': 'Көлөм',
    'geometry-volume-surface-area-cone-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Конус > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-cone-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-cone-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Параллелепипед - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-cuboid-volume': 'Көлөм',
    'geometry-volume-surface-area-cuboid-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Параллелепипед > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-cuboid-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-cuboid-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Цилиндр - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-cylinder-volume': 'Көлөм',
    'geometry-volume-surface-area-cylinder-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Цилиндр > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-cylinder-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-cylinder-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Призма - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-prism-volume': 'Көлөм',
    'geometry-volume-surface-area-prism-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Призма > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-prism-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-prism-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Кесилген конус - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-frustum-volume': 'Көлөм',
    'geometry-volume-surface-area-frustum-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Кесилген конус > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-frustum-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-frustum-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Пирамида - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-pyramid-volume': 'Көлөм',
    'geometry-volume-surface-area-pyramid-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Пирамида > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-pyramid-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-pyramid-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Сфера - 2 flat slots,
    # none with a real page yet.
    'geometry-volume-surface-area-sphere-volume': 'Көлөм',
    'geometry-volume-surface-area-sphere-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Сфера > Аралаш - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-sphere-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-sphere-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Цилиндр жана призма - 2 flat
    # slots, none with a real page yet.
    'geometry-volume-surface-area-cylinder-prism-volume': 'Көлөм',
    'geometry-volume-surface-area-cylinder-prism-surface-area': 'Бет аянты',

    # Геометрия > Көлөм жана бет аянты > Цилиндр жана призма > Аралаш -
    # 2 flat slots, none with a real page yet.
    'geometry-volume-surface-area-cylinder-prism-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-cylinder-prism-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Көлөм жана бет аянты > Аралаш (top-level sibling to
    # Конус/Параллелепипед/etc) - 2 flat slots, none with a real page
    # yet.
    'geometry-volume-surface-area-mixed-foundation': 'Негизги деңгээл',
    'geometry-volume-surface-area-mixed-higher': 'Жогорку деңгээл',

    # Геометрия > Бурчтар > Аралаш - all 2 slots, none with a real
    # page yet.
    'geometry-angles-mixed-without-circle-theorems': 'Тегерек теоремаларысыз',
    'geometry-angles-mixed-with-circle-theorems': 'Тегерек теоремалары менен',

    # Геометрия > Аянт жана периметр > Тегеректер - all 10 slots,
    # none with a real page yet.
    'geometry-area-perimeter-circles-vocabulary': 'Терминология',
    'geometry-area-perimeter-circles-area': 'Аянт',
    'geometry-area-perimeter-circles-area-in-terms-of-pi': 'π аркылуу аянт',
    'geometry-area-perimeter-circles-circumference': 'Тегеректин узундугу',
    'geometry-area-perimeter-circles-area-circumference': 'Аянт жана тегеректин узундугу',
    'geometry-area-perimeter-circles-arc-length': 'Жаанын узундугу',
    'geometry-area-perimeter-circles-sector-area': 'Сектордун аянты',
    'geometry-area-perimeter-circles-arcs-sectors': 'Жаалар жана секторлор',
    'geometry-area-perimeter-circles-mixed': 'Аралаш',
    'geometry-area-perimeter-circles-comparative-pie-charts': 'Салыштырма тоорт диаграммалар',

    # Геометрия > Аянт жана периметр > Татаал: түз сызыктуу - all 3
    # slots, none with a real page yet.
    'geometry-area-perimeter-compound-rectilinear-area': 'Аянт',
    'geometry-area-perimeter-compound-rectilinear-perimeter': 'Периметр',
    'geometry-area-perimeter-compound-rectilinear-mixed': 'Аралаш',

    # Геометрия > Аянт жана периметр > Татаал: көп бурчтуктуу - all 3
    # slots, none with a real page yet.
    'geometry-area-perimeter-compound-polygonal-area': 'Аянт',
    'geometry-area-perimeter-compound-polygonal-perimeter': 'Периметр',
    'geometry-area-perimeter-compound-polygonal-perimeter-with-pythagoras': 'Периметр: Пифагор менен',

    # Геометрия > Аянт жана периметр > Татаал: тегеректер менен - all
    # 3 slots, none with a real page yet.
    'geometry-area-perimeter-compound-with-circles-area': 'Аянт',
    'geometry-area-perimeter-compound-with-circles-perimeter': 'Периметр',
    'geometry-area-perimeter-compound-with-circles-mixed': 'Аралаш',

    # Геометрия > Аянт жана периметр > Төрт бурчтуктар - 6 slots, none
    # with a real page yet.
    'geometry-area-perimeter-quadrilaterals-vocabulary': 'Терминология',
    'geometry-area-perimeter-quadrilaterals-rectangle-area': 'Тик бурчтук: аянт',
    'geometry-area-perimeter-quadrilaterals-rectangle-perimeter': 'Тик бурчтук: периметр',
    'geometry-area-perimeter-quadrilaterals-rectangle-area-perimeter': 'Тик бурчтук: аянт жана периметр',
    'geometry-area-perimeter-quadrilaterals-parallelogram': 'Параллелограмм',
    'geometry-area-perimeter-quadrilaterals-trapezium': 'Трапеция',

    # Геометрия > Аянт жана периметр > Үч бурчтуктар - 2 known slots
    # (screenshot was cut off), none with a real page yet.
    'geometry-area-perimeter-triangles-area': 'Аянт',
    'geometry-area-perimeter-triangles-area-using-sine-rule': 'Синус эрежеси менен аянт',

    # Геометрия > Аянт жана периметр > Аралаш - all 4 slots, none
    # with a real page yet.
    'geometry-area-perimeter-mixed-polygons': 'Көп бурчтуктар',
    'geometry-area-perimeter-mixed-polygons-with-pythagoras': 'Көп бурчтуктар: Пифагор менен',
    'geometry-area-perimeter-mixed-polygons-circles': 'Көп бурчтуктар жана тегеректер',
    'geometry-area-perimeter-mixed-polygons-circles-with-pythagoras': 'Көп бурчтуктар жана тегеректер: Пифагор менен',

    # Геометрия > Классификациялоо жана терминология > Фигураларды
    # классификациялоо - 4 known slots (screenshot was cut off), none
    # with a real page yet.
    'geometry-classifying-vocabulary-classifying-shapes-diagonals': 'Диагоналдар',
    'geometry-classifying-vocabulary-classifying-shapes-symmetry': 'Симметрия',
    'geometry-classifying-vocabulary-classifying-shapes-quadrilaterals': 'Төрт бурчтуктар',
    'geometry-classifying-vocabulary-classifying-shapes-2d-shapes': '2D фигуралар',

    # Геометрия > Классификациялоо жана терминология > Терминология -
    # all 5 slots, none with a real page yet.
    'geometry-classifying-vocabulary-vocabulary-angles': 'Бурчтар',
    'geometry-classifying-vocabulary-vocabulary-circles': 'Тегеректер',
    'geometry-classifying-vocabulary-vocabulary-2d-shapes': '2D фигуралар',
    'geometry-classifying-vocabulary-vocabulary-3d-shapes': '3D фигуралар',
    'geometry-classifying-vocabulary-vocabulary-sketching-diagrams': 'Диаграммаларды чийүү',

    # Геометрия > Курулуштар > Бурчтар - all 4 slots, none with a
    # real page yet.
    'geometry-construction-angles-drawing': 'Чийүү',
    'geometry-construction-angles-measuring': 'Өлчөө',
    'geometry-construction-angles-both': 'Чийүү жана өлчөө',
    'geometry-construction-angles-estimating': 'Болжолдоо',

    # Геометрия > Курулуштар > Көп бурчтуктар - 2 known slots, none
    # with a real page yet.
    'geometry-construction-polygons-triangles': 'Үч бурчтуктар',
    'geometry-construction-polygons-quadrilaterals': 'Төрт бурчтуктар',

    # Геометрия > Курулуштар > Бисектрисалар - all 3 slots, none with
    # a real page yet.
    'geometry-construction-bisectors-line': 'Сызык',
    'geometry-construction-bisectors-angle': 'Бурч',
    'geometry-construction-bisectors-mixed': 'Аралаш',

    # Дата > Талдоо - 4 flat slots, none with a real page yet.
    'data-analysing-median': 'Медиана',
    'data-analysing-from-a-bar-chart': 'Тилке диаграммадан',
    'data-analysing-choosing-an-average': 'Орточону тандоо',
    'data-analysing-comparing-using-mmmr': 'Салыштыруу: орточо, медиана, мода жана диапазон менен',

    # Дата > Талдоо > Орточо - 3 flat slots, none with a real page yet.
    'data-analysing-mean-from-a-list': 'Тизмеден',
    'data-analysing-mean-reverse': 'Тескери',
    'data-analysing-mean-adjusting': 'Тууралоо',

    # Дата > Талдоо > Мода жана диапазон - 2 flat slots, none with a
    # real page yet.
    'data-analysing-mode-range-mode': 'Мода',
    'data-analysing-mode-range-range': 'Диапазон',

    # Дата > Талдоо > Кварталдар - 3 flat slots, none with a real page
    # yet.
    'data-analysing-quartiles-introduction': 'Киришүү',
    'data-analysing-quartiles-with-box-plots': 'Куту диаграммалары менен',
    'data-analysing-quartiles-box-plots': 'Куту диаграммалары',

    # Дата > Чогултуу - 6 flat slots, none with a real page yet.
    'data-collecting-introduction': 'Киришүү',
    'data-collecting-vocabulary': 'Терминология',
    'data-collecting-types-of-data': 'Маалымат түрлөрү',
    'data-collecting-questionnaires': 'Анкеталар',
    'data-collecting-stratified-sampling': 'Катмарланган тандоо',
    'data-collecting-capture-recapture': 'Кармап-кайра кармоо',

    # Дата > Жыштык таблицалары > Топтоштурулбаган берилиштер -
    # "Топтоштурулган берилиштер" turned out to be a category, its own
    # entry below is now orphaned.
    'data-frequency-tables-grouped-data': 'Топтоштурулган берилиштер',
    'data-frequency-tables-ungrouped-data-creating-reading': 'Түзүү жана окуу',
    'data-frequency-tables-ungrouped-data-calculating-averages': 'Орточолорду эсептөө',

    # Дата > Жыштык таблицалары > Топтоштурулган берилиштер - 2 flat
    # slots, none with a real page yet.
    'data-frequency-tables-grouped-data-creating-reading': 'Түзүү жана окуу',
    'data-frequency-tables-grouped-data-calculating-averages': 'Орточолорду эсептөө',

    # Дата > Жыштык таблицалары > Эки багыттуу таблицалар - 3 flat
    # slots, none with a real page yet.
    'data-frequency-tables-two-way-tables-creating-reading': 'Түзүү жана окуу',
    'data-frequency-tables-two-way-tables-with-probability': 'Ыктымалдуулук менен',
    'data-frequency-tables-two-way-tables-with-bar-charts': 'Тилке диаграммалар менен',

    # Дата > Көрсөтүү - 6 flat slots, none with a real page yet.
    'data-representing-frequency-polygons': 'Жыштык көп бурчтуктары',
    'data-representing-histograms': 'Гистограммалар',
    'data-representing-line-graphs-time-series': 'Сызыктуу графиктер / Убакыт катарлары',
    'data-representing-pictograms': 'Пиктограммалар',
    'data-representing-scatter-graphs': 'Чачыранды диаграммалар',
    'data-representing-stem-leaf-diagrams': 'Сабак-жалбырак диаграммалары',

    # Дата > Көрсөтүү > Тилке диаграммалары - 6 flat slots, none with a
    # real page yet.
    'data-representing-bar-charts-single': 'Жалгыз',
    'data-representing-bar-charts-dual': 'Кош',
    'data-representing-bar-charts-composite': 'Татаал',
    'data-representing-bar-charts-vertical-line-charts': 'Вертикалдуу сызык диаграммалары',
    'data-representing-bar-charts-calculating-averages': 'Орточолорду эсептөө',
    'data-representing-bar-charts-with-two-way-tables': 'Эки багыттуу таблицалар менен',

    # Дата > Көрсөтүү > Куту диаграммалары - 3 flat slots, none with a
    # real page yet.
    'data-representing-box-plots-with-quartiles': 'Кварталдар менен',
    'data-representing-box-plots-creating-reading': 'Түзүү жана окуу',
    'data-representing-box-plots-with-graphs': 'Графиктер менен',

    # Дата > Көрсөтүү > Топтолгон жыштык графиктери - 2 flat slots, none
    # with a real page yet.
    'data-representing-cumulative-frequency-graphs-introduction': 'Киришүү',
    'data-representing-cumulative-frequency-graphs-with-box-plots': 'Куту диаграммалары менен',

    # Дата > Көрсөтүү > Жыштык дарактары - 3 flat slots, none with a
    # real page yet.
    'data-representing-frequency-trees-introduction': 'Киришүү',
    'data-representing-frequency-trees-with-fpr': 'Бөлчөк, пайыз жана катыш менен',
    'data-representing-frequency-trees-with-probability-trees': 'Ыктымалдуулук дарактары менен',

    # Дата > Көрсөтүү > Тегерек диаграммалар - 3 flat slots, none with a
    # real page yet.
    'data-representing-pie-charts-reading': 'Окуу',
    'data-representing-pie-charts-scaling-method': 'Масштабдоо ыкмасы',
    'data-representing-pie-charts-proportional-method': 'Пропорциялык ыкма',
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
