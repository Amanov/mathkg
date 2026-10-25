"""Grade packs shown on the site's «даярдалууда» pages (2026-10-24).

The site has hundreds of fine-grained pages (one per sub-skill). One grade
pack from /mnt/project-files/kitep-temalary/ teaches a whole group of them,
so each group below lists the pages it fills; operation_placeholder_view
renders the group's page in the «Төрт амал» layout instead of the
placeholder. A pack goes only on pages whose content it actually teaches
(checked against the page audit in sayt-mockup/bardyk-temalar/), so for
example the rectangle pack is not put on the circle or triangle pages.

Every pack has the same eleven files; they ship in
apps/resources/bundled_files/ (migrations 0035 onwards add their Resource rows) and
their previews in static/img/topic-pages/.
"""

import copy

from apps.resources.data.grade_topic_pages import IMAGE_DIR, TEACHER_NOTE, _item, _page

SUFFIXES = (
    'sabak.pptx', 'oyun-1234.pptx', 'oyun-atyshuu.pptx', 'ish-barak.pdf', 'katany-tap.pdf', 'labirint.pdf',
    'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf', 'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf',
)

PACKS = {
    'figuralar': {
        'prefix': '2-klass-figuralar-', 'grade': 2, 'subtopic': 'Тегиз жана көлөмдүү фигуралар',
        'sabak': '26 слайд: «Каракол: чоң атанын устаканасы» окуясы, таякча жана пластилин куб, кубдун жайылмасы.',
        'ish-barak': 'Жактарды, чокуларды, беттерди жана кырларды санашат; жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: фигураларды касиеттери боюнча топтошот.',
        'puzzle': ('Таякча табышмагы', 'Үч деңгээл: таякчалардан фигура түзүшөт.'),
    },
    'olchomdor': {
        'prefix': '3-klass-olchomdor-', 'grade': 3, 'subtopic': 'Узундук, масса жана көлөм',
        'sabak': '26 слайд: «Арстанбаптагы жаңгак түшүмү» окуясы, сызгыч, тараза жана өлчөөчү идиш.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: 1 метрден кыска, так 1 метр же узун.',
    },
    'simmetriya': {
        'prefix': '4-klass-simmetriya-', 'grade': 4, 'subtopic': 'Симметрия жана жылдыруу',
        'sabak': '26 слайд: «Караколдогу оюу дубал» окуясы, кагазды бүктөп кесүү, чакмак кагазда чагылдыруу жана жылдыруу.',
        'ish-barak': 'Үч бет: симметрия огу, чакмак кагазда чагылдыруу жана жылдыруу; жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: симметрия огунун саны боюнча.',
    },
    'ondu_orun': {
        'prefix': '5-klass-ondu-bolchok-orun-maani-', 'grade': 5, 'subtopic': 'Ондук бөлчөктөр: орун маанилери',
        'sabak': '26 слайд: «Караколдогу спорт күнү» окуясы, бүктөлгөн метр тилкеси, орун маанилер таблицасы, сан огу.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: салыштыруу жана тегеректөө.',
    },
    'ubakyt': {
        'prefix': '2-klass-ubakyt-', 'grade': 2, 'subtopic': 'Убакыт',
        'sabak': '26 слайд: «Ишемби: Токмокко, Зуура апага» окуясы, кагаз табак саат, убакыт сызыгындагы секирүүлөр.',
        'ish-barak': 'Саат окуу, жебелерди тартуу, октябрь календары; жооп ачкычы менен.',
        'karta-sorttoo': 'Саат сүрөтү, сандык убакыт жана сөз менен жазылган убакыт.',
    },
    'perimetr': {
        'prefix': '5-klass-perimetr-jana-ayant-', 'grade': 5, 'subtopic': 'Периметр жана аянт',
        'sabak': '26 слайд: «Кочкордогу шырдак» окуясы, жип жана кагаз чарчылар, L түрүндөгү фигура.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: периметрби, аянтпы, же экөө тең.',
    },
    'burchtar': {
        'prefix': '5-klass-burchtar-', 'grade': 5, 'subtopic': 'Бурчтар',
        'sabak': '26 слайд: «Жайлоодо боз үй тигүү» окуясы, транспортир, саламча жана төөнөгүч, керегенин X бурчтары.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: тар, тик, кең жана жайылган бурчтар.',
    },
    'fdp': {
        'prefix': '6-klass-bolchok-ondu-procent-', 'grade': 6, 'subtopic': 'Бөлчөк, ондук бөлчөк жана пайыз',
        'sabak': '26 слайд: «Ош базарындагы арзандатуулар» окуясы, 100 чарчы, бүктөлгөн тилке, кош сан огу.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: бирдей сандын үч жазылышы.',
    },
    'katysh': {
        'prefix': '6-klass-katysh-', 'grade': 6, 'subtopic': 'Катыш',
        'sabak': '26 слайд: «Кочкордогу шырдак» окуясы, эки түстүү буурчак, тилке модели, 2 : 3 жана 2/5.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: барабар катыштар.',
    },
    'bolchok_kb': {
        'prefix': '6-klass-bolchok-kobeytuu-boluu-', 'grade': 6, 'subtopic': 'Бөлчөктөрдү көбөйтүү жана бөлүү',
        'sabak': '26 слайд: «Сокулуктагы тойго боорсок» окуясы, бүктөлгөн кагаз тилкелер, аянт модели, 4 1/2 ÷ 3/4.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу 1ден кичине, 1ге барабар же 1ден чоң.',
    },
    'akcha': {
        'prefix': '4-klass-akcha-', 'grade': 4, 'subtopic': 'Акча',
        'sabak': '26 слайд: «Жалал-Абаддагы дүкөн» окуясы, кагаз акча жана капкак тыйындар, кайтарымды кошуп саноо.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: кайсы сатып алуу пайдалуураак.',
        'puzzle': ('Акча табышмагы', 'Үч деңгээл: тыйын жана кагаз акча менен төлөө жолдорун табышат.'),
    },
    'ondu_kk': {
        'prefix': '5-klass-ondu-koshuu-kemituu-', 'grade': 5, 'subtopic': 'Ондук бөлчөктөрдү кошуу жана кемитүү',
        'sabak': '26 слайд: «Ысык-Атага велосипед сапары» окуясы, орун маанилер таблицасында капкактар, чакмак кагазда мамыча.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу боюнча топтошот.',
    },
    'ondu_kb': {
        'prefix': '5-klass-ondu-kobeytuu-boluu-', 'grade': 5, 'subtopic': 'Ондук бөлчөктөрдү көбөйтүү жана бөлүү',
        'sabak': '26 слайд: «Баткендеги өрүк кургатуу» окуясы, орун маанилер таблицасы, 10 × 10 чарчы, кагаз тилкелер.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу баштапкы сандан чоңбу, кичинеби.',
    },
    'bolchok_t': {
        'prefix': '3-klass-bolchok-tushunugu-', 'grade': 3, 'subtopic': 'Бөлчөк түшүнүгү',
        'sabak': '26 слайд: «Баткенде өрүк кургатуу» окуясы, нан, кагаз тилкелер, бөлчөк дубалы жана сан огу.',
        'ish-barak': 'Сүрөттүү тапшырмалар жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Сүрөттүү карталар: бөлчөктү сүрөт, сөз жана сан менен дал келтиришет.',
    },
    'kvadrat': {
        'prefix': '6-klass-kvadrat-kub-daraja-', 'grade': 6, 'subtopic': 'Квадрат жана куб сандар',
        'sabak': '26 слайд: өрүк кургатуу окуясы, буурчак чарчылары, кант кубиктери, чакмак дептер.',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: квадрат, куб же экөө тең.',
    },
    'algebra': {
        'prefix': '6-klass-tamgaluu-tuyuntmalar-tendemeler-', 'grade': 6, 'subtopic': 'Тамгалуу туюнтмалар жана теңдемелер',
        'sabak': '26 слайд: «Таластагы буурчак түшүмү» окуясы, чөйчөк жана капкак менен тараза, 2x + 5 = 17.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: теңдемелерди тамыры боюнча топтошот.',
    },
    'maalymat': {
        'prefix': '6-klass-maalymat-diagramma-orto-maani-', 'grade': 6, 'subtopic': 'Маалымат, диаграмма жана орто маани',
        'sabak': '26 слайд: «Ош базарындагы жемиш дүкөнү» окуясы, стикерлерден диаграмма, капкак мунаралары менен орто маани.',
        'ish-barak': '18 тапшырма, мамычалуу диаграмма, сызыктуу график жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: орто маани, медиана, мода жана кулач.',
    },
}


def _pack_items(pack):
    prefix, grade, subtopic = pack['prefix'], pack['grade'], pack['subtopic']

    def one(section, title, note, level, suffix, label='PDF A4'):
        ext = '.pptx' if label == 'PPT' else '.pdf'
        return _item(section, grade, title, note, level, [(label, prefix + suffix + ext)],
                     IMAGE_DIR + prefix + suffix + '.webp', subtopic=subtopic)

    return [
        one('Изилдөө', *pack.get('puzzle', ('Цифра табышмагы', 'Үч деңгээл: бош орунга цифра коюшат.')),
            'Талдоо', 'cifra-tabyshmagy'),
        one('Түшүндүрүү', 'Сабактын презентациясы', pack['sabak'], 'Түшүнүү', 'sabak', 'PPT'),
        one('Тереңдетүү', 'Иш барак: Жеңил, Орто, Оор', pack['ish-barak'], 'Колдонуу', 'ish-barak'),
        one('Баалоо', 'Катаны тап', 'Алты окуучунун чыгарылышы: катаны таап, оңдошот.', 'Баалоо', 'katany-tap'),
        one('Баалоо', 'Туура же ката лабиринт', 'Туура жооптор аркылуу гана өтүшөт.', 'Баалоо', 'labirint'),
        one('Байланыштыруу', 'Домино', '12 карта: суроо менен жообу чынжыр түзөт.', 'Талдоо', 'domino'),
        one('Байланыштыруу', 'Карта сорттоо', pack['karta-sorttoo'], 'Талдоо', 'karta-sorttoo'),
        one('Кызматташуу', '1234 оюну', 'Командалар менен, 9 слайд.', 'Колдонуу', 'oyun-1234', 'PPT'),
        one('Кызматташуу', 'Атышуу', 'Эки команда, 25 слайд, ылдамдыксыз упай.', 'Колдонуу', 'oyun-atyshuu', 'PPT'),
    ]


def _teacher(pack):
    prefix, grade, subtopic = pack['prefix'], pack['grade'], pack['subtopic']
    return [
        {'title': f'{grade}-класс · {subtopic}: класста колдонуу', 'note': TEACHER_NOTE,
         'files': [('PDF', prefix + 'klassta-koldonuu.pdf')], 'grade': grade},
        {'title': f'{grade}-класс · {subtopic}: мугалимдин картасы',
         'note': 'Типтүү каталар, чечүүчү суроо, чыгуу билети.',
         'files': [('PDF', prefix + 'mugalim-kartasy.pdf')], 'grade': grade},
    ]


def _group(key, title, crumb, pack_keys, slugs):
    packs = [PACKS[k] for k in pack_keys]
    grades = sorted({p['grade'] for p in packs})
    badge = f'{grades[0]}-класс' if len(grades) == 1 else None
    items = [i for p in packs for i in _pack_items(p)]
    teacher = [t for p in packs for t in _teacher(p)]
    return {'spec': _page(title, 'pack_' + key, crumb, badge, items, teacher=teacher), 'slugs': slugs}


GROUPS = [
    _group('ubakyt', 'Убакыт', 'Өлчөмдөр › Убакыт', ['ubakyt'], [
        'time-reading-clocks', 'time-days-months-years', 'time-timetables', 'time-calculations', 'time-converting',
    ]),
    _group('figuralar', 'Тегиз жана көлөмдүү фигуралар', 'Геометрия › Фигуралар', ['figuralar'], [
        'geometry-classifying-vocabulary-classifying-shapes-2d-shapes',
        'geometry-classifying-vocabulary-vocabulary-2d-shapes',
        'geometry-classifying-vocabulary-vocabulary-3d-shapes',
    ]),
    _group('olchomdor', 'Узундук, масса жана көлөм бирдиктери', 'Өлчөмдөр', ['olchomdor'], [
        'systems-of-measurement-metric',
        'systems-of-measurement-conversion-factors',
    ]),
    _group('simmetriya', 'Симметрия жана фигураларды жылдыруу', 'Геометрия › Өзгөртүүлөр', ['simmetriya'], [
        'geometry-classifying-vocabulary-classifying-shapes-symmetry',
    ]),
    _group('ondu_orun', 'Ондук бөлчөктөр: орун маанилери, салыштыруу, тегеректөө', 'Сандар › Ондуктар', ['ondu_orun'], [
        'rounding-decimal-places',
    ]),
    _group('perimetr', 'Периметр жана аянт', 'Геометрия › Периметр жана аянт', ['perimetr'], [
        'geometry-area-perimeter-quadrilaterals-rectangle-area',
        'geometry-area-perimeter-quadrilaterals-rectangle-perimeter',
        'geometry-area-perimeter-quadrilaterals-rectangle-area-perimeter',
        'geometry-area-perimeter-compound-rectilinear-area',
        'geometry-area-perimeter-compound-rectilinear-perimeter',
        'geometry-area-perimeter-compound-rectilinear-mixed',
    ]),
    _group('burchtar', 'Бурчтар', 'Геометрия › Бурчтар', ['burchtar'], [
        'geometry-angles-angle-facts-vocabulary',
        'geometry-angles-angle-facts-on-straight-lines',
        'geometry-angles-angle-facts-around-a-point',
        'geometry-angles-angle-facts-vertically-opposite',
        'geometry-angles-drawing-measuring-both',
        'geometry-angles-drawing-measuring-drawing',
        'geometry-angles-drawing-measuring-estimating',
        'geometry-angles-drawing-measuring-measuring',
        'geometry-construction-angles-both',
        'geometry-construction-angles-drawing',
        'geometry-construction-angles-estimating',
        'geometry-construction-angles-measuring',
    ]),
    _group('katysh', 'Катыш', 'Сандар › Катыш', ['katysh'], [
        'ratio-expressing-simplifying',
        'ratio-expressing-division',
        'ratio-dividing-into-a-ratio',
        'ratio-manipulation-comparing-parts',
        'ratio-quantities-mixed',
        'ratio-mixed-foundation',
    ]),
    _group('fdpr', 'Бөлчөк, ондук бөлчөк, пайыз жана катыш', 'Сандар › Эквиваленттүүлүк', ['fdp', 'katysh'], [
        'fractions-to-ratios', 'fractions-with-ratios', 'fractions-to-all', 'fractions-with-all',
        'fractions-equiv-to-ratios', 'fractions-equiv-with-ratios', 'fractions-equiv-to-all',
        'fractions-equiv-fdpr', 'fractions-equiv-fpr',
        'percentages-to-ratios', 'percentages-with-ratios', 'percentages-to-all', 'percentages-with-all',
        'ratios-to-fractions', 'ratios-to-percentages', 'ratios-to-both',
        'ratios-with-fractions', 'ratios-with-percentages', 'ratios-with-both',
    ]),
    _group('fdp', 'Бөлчөк, ондук бөлчөк жана пайыз', 'Сандар › Эквиваленттүүлүк', ['fdp'], [
        'fractions-to-decimals', 'fractions-to-percentages', 'fractions-with-decimals', 'fractions-with-percentages',
        'percentages-to-fractions', 'percentages-to-decimals', 'percentages-with-fractions', 'percentages-with-decimals',
        'fractions-equiv-to-decimals', 'fractions-equiv-to-percentages', 'fractions-equiv-with-decimals',
        'fractions-equiv-with-percentages', 'fractions-equiv-fdp', 'fractions-equiv-fdp-ordering',
    ]),
    _group('bolchok_kb', 'Бөлчөктөрдү көбөйтүү жана бөлүү, аралаш сандар', 'Сандар › Бөлчөктөр › Эсептөөлөр',
           ['bolchok_kb'], [
        'unit-fractions-multiplying', 'unit-fractions-dividing', 'unit-fractions-multiplying-dividing',
        'unit-fractions-with-integers',
        'non-unit-fractions-multiplying', 'non-unit-fractions-dividing', 'non-unit-fractions-multiplying-dividing',
        'non-unit-fractions-with-cancelling', 'non-unit-fractions-with-integers',
    ]),
    _group('akcha', 'Акча: сатып алуу, кайтарым, эң пайдалуу баа', 'Өлчөмдөр › Акча', ['akcha'], [
        'measures-money-purchasing-non-calculator',
    ]),
    _group('ondu_kk', 'Ондук бөлчөктөрдү кошуу жана кемитүү', 'Сандар › Ондуктар › Эсептөөлөр', ['ondu_kk'], [
        'subtracting-1-digit', 'adding-subtracting-1-digit',
        'adding-1-2-digit', 'subtracting-1-2-digit', 'adding-subtracting-1-2-digit',
        'integers-adding-with-decimals', 'integers-subtracting-with-decimals',
        'integers-adding-subtracting-with-decimals',
    ]),
    _group('ondu_kb', 'Ондук бөлчөктөрдү көбөйтүү жана бөлүү', 'Сандар › Ондуктар › Эсептөөлөр', ['ondu_kb'], [
        'multiplying-1-digit', 'dividing-1-digit', 'multiplying-dividing-1-digit', 'mixed-1-digit',
        'dividing-by-less-than-1', 'multiplying-1-2-digit', 'dividing-1-2-digit', 'multiplying-dividing-1-2-digit',
        'mixed-1-2-digit', 'multiplying-dividing-10-100-1000',
        'integers-multiplying-with-decimals', 'integers-dividing-with-decimals',
        'integers-multiplying-dividing-with-decimals', 'integers-dividing-divisor-less-than-1-with-decimals',
        'integers-mixed-with-decimals', 'multiplying-with-integers', 'dividing-with-integers',
        'multiplying-dividing-with-integers', 'mixed-with-integers', 'dividing-divisor-less-than-1-with-integers',
    ]),
    _group('bolchok_t', 'Бөлчөк түшүнүгү', 'Сандар › Бөлчөктөр', ['bolchok_t'], []),
    _group('kvadrat', 'Квадрат жана куб сандар, даража', 'Сандар › Даражалар', ['kvadrat'], [
        'indices-introduction', 'indices-square-numbers', 'indices-cube-numbers',
        'evaluating-roots-square', 'evaluating-roots-square-cube',
    ]),
    _group('algebra', 'Тамгалуу туюнтмалар жана теңдемелер', 'Алгебра', ['algebra'], [
        'algebra-intro-definitions',
        'algebra-intro-notation',
        'algebra-forming-expr-linear',
        'algebra-manipulation-forming-linear',
        'algebra-manipulation-notation',
        'algebra-manipulation-notation-adding',
        'algebra-manipulation-expressions-adding',
        'algebra-substitution-symbols-positive',
        'algebra-substitution-without-indices-positive',
        'algebra-linear-forming',
        'algebra-linear-variable-one-side-non-calculator',
        'algebra-linear-variable-one-side-calculator',
        'algebra-linear-var1side-noncalc-1step',
        'algebra-linear-var1side-noncalc-2step',
        'algebra-linear-var1side-calc-1step',
        'algebra-linear-var1side-calc-2step',
    ]),
    _group('maalymat', 'Маалымат, диаграмма жана орто маани', 'Дата', ['maalymat'], [
        'data-collecting-introduction',
        'data-frequency-tables-ungrouped-data-creating-reading',
        'data-representing-pictograms',
        'data-representing-bar-charts-single',
        'data-representing-bar-charts-calculating-averages',
        'data-representing-line-graphs-time-series',
        'data-representing-mixed-foundation',
        'data-analysing-mean-from-a-list',
        'data-analysing-median',
        'data-analysing-mode-range-mode',
        'data-analysing-mode-range-range',
        'data-analysing-from-a-bar-chart',
        'data-analysing-comparing-using-mmmr',
    ]),
]

# The Эквиваленттүүлүк pages with their own named views (see views/ekvivalenttuuluk.py).
FDP = next(g['spec'] for g in GROUPS if g['spec']['page_key'] == 'pack_fdp')
FDPR = next(g['spec'] for g in GROUPS if g['spec']['page_key'] == 'pack_fdpr')

SLUG_PAGES = {slug: group['spec'] for group in GROUPS for slug in group['slugs']}

# Database-driven pages (/resources/topic/<topic>/<subtopic>/[<subsubtopic>/])
# that are still empty, keyed by their slugs. The pack shows only while the
# page has no resources of its own (see views/topics.py).
_BY_KEY = {group['spec']['page_key'][len('pack_'):]: group['spec'] for group in GROUPS}
PATH_PAGES = {path: _BY_KEY[key] for path, key in [
    (('number', 'decimals', 'place-value'), 'ondu_orun'),
    (('number', 'decimals', 'ordering-decimals'), 'ondu_orun'),
    (('number', 'equivalence', 'fraction-decimal-percentage'), 'fdp'),
    (('number', 'equivalence', 'ordering-fractions-decimals-percentages'), 'fdp'),
    (('number', 'equivalence', 'fraction-percentage-ratio'), 'fdpr'),
    (('number', 'equivalence', 'fraction-decimal-percentage-ratio'), 'fdpr'),
    (('number', 'fractions', 'mixed-numbers-improper-fractions'), 'bolchok_kb'),
    (('number', 'fractions', 'reciprocals'), 'bolchok_kb'),
    (('number', 'measures', 'measuring-lines'), 'olchomdor'),
    (('number', 'fractions', 'introduction'), 'bolchok_t'),
    (('number', 'fractions', 'fractions-as-words'), 'bolchok_t'),
    (('number', 'indices-surds', 'indices-roots-integers'), 'kvadrat'),
    (('number', 'measures', 'reading-scales'), 'olchomdor'),
    (('geometry', 'transformations', 'reflection'), 'simmetriya'),
    (('geometry', 'transformations', 'translation'), 'simmetriya'),
    (('geometry', 'transformations', 'line-symmetry'), 'simmetriya'),
    (('statistics', 'analysing', 'mixed'), 'maalymat'),
    (('statistics', 'representing', 'mixed'), 'maalymat'),
]}

NEW_FILES = [pack['prefix'] + suffix for pack in PACKS.values() for suffix in SUFFIXES]


def page_for(slug, page_title):
    """The group page for a placeholder slug (or a PATH_PAGES key), with the
    page's own title in the menu path above the heading, or None if no pack
    fits it yet."""
    spec = PATH_PAGES.get(slug) if isinstance(slug, tuple) else SLUG_PAGES.get(slug)
    if spec is None:
        return None
    spec = copy.copy(spec)
    spec['crumb'] = f"{spec['crumb']} › {page_title}"
    return spec
