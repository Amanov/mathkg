"""Content for topic pages rendered with templates/resources/topic_materials.html.

A topic page lists its materials in sections. Each material has an SVG
thumbnail (templates/svg/topic/<page>/<name>.svg, inlined into the page)
and download buttons. A button only shows when its file exists as an
active Resource, matched by `Resource.title` the same way the older
hand-built templates do with `res|get_item:'filename'`.
"""

from django.urls import reverse

from apps.resources.data.four_basic_operations_grades import (
    GRADE_IMAGE_DIR,
    GRADE_ITEMS,
    GRADE_TEACHER_FILES,
)
from apps.resources.filenames import resource_for_title
from apps.resources.free_download import choose_free_resource

# Sections follow the 5E + 3C lesson model, each with the Bloom's taxonomy
# levels its materials actually reach. Placement comes from reading each
# PPTX (2026-10-09 review: /mnt/project-files/topic-page-svg/to-fractions/
# 5e-3c-analysis.md), not from the activity's name. Stage names match
# STAGES in apps/resources/lesson_flow.py on the landing-5e-3c-bloom branch
# (PR #3). Explore, Explain and Create materials were added 2026-10-09 to
# fill the gaps the review found.
BLOOM_LEVELS = ['Эстеп калуу', 'Түшүнүү', 'Колдонуу', 'Талдоо', 'Баалоо', 'Жаратуу']

# What each Bloom level asks of the pupil. The 2018 programme (below) names
# three levels of results: понимание, применение, анализ.
BLOOM_GUIDE = {
    'Эстеп калуу': 'Эрежени, фактыны эстейт',
    'Түшүнүү': 'Өз сөзү менен түшүндүрөт (программанын 1-деңгээли: түшүнүү)',
    'Колдонуу': 'Эрежени жаңы мисалдарда колдонот (2-деңгээл: колдонуу)',
    'Талдоо': 'Салыштырат, мыйзам ченемин табат (3-деңгээл: талдоо)',
    'Баалоо': 'Жооптун туура же ката экенин негиздейт',
    'Жаратуу': 'Өз тапшырмасын, суроосун түзөт',
}

# Source: МОН КР / Кыргызская академия образования, «Математика. Программа для
# общеобразовательных организаций 5–9 классы», Бишкек 2018. It has no outcome
# codes, so none are shown.
STANDARD_REF = {
    'document': 'КР Билим берүү жана илим министрлиги, Кыргыз билим берүү академиясы: '
    '«Математика. Программа для общеобразовательных организаций, 5–9 классы» (2018)',
    'grade': '5-класс, «Десятичные дроби и действия над ними»: «перевод десятичных дробей '
    'в обыкновенные»',
    'competency': 'Предметтик компетенттүүлүк: эсептөө («Вычислительная: различает числа. '
    'Производит арифметические … операции над числами»)',
}

# Designed thumbnails for the 16 activity slots. Keys match each item's
# `svg` name; values are static PNGs (960×624) that replace the inline SVG.
TO_FRACTIONS_IMAGES = {
    '1234': 'img/to-fractions/01-1234.png',
    'bingo': 'img/to-fractions/02-bingo.png',
    'korsot-ooba-jok': 'img/to-fractions/03-korsot.png',
    'cifra-tabyshmagy': 'img/to-fractions/04-cifra.png',
    'tushunduruu': 'img/to-fractions/05-tushundur.png',
    'jenil-orto-oor': 'img/to-fractions/06-jenil-orto-oor.png',
    'kazyna-jenil': 'img/to-fractions/07-kazyna-jenil.png',
    'kazyna-oor': 'img/to-fractions/08-kazyna-oor.png',
    'bingo-orun': 'img/to-fractions/09-bingo-orun.png',
    'katany-tap': 'img/to-fractions/10-katany-tap.png',
    'sandar-labyrinth': 'img/to-fractions/11-labirint.png',
    'tarsia-kurak': 'img/to-fractions/12-tarsia.png',
    'katary-menen-tort': 'img/to-fractions/13-katary-tort.png',
    '3-tutashtyr': 'img/to-fractions/14-3-tutashtyr.png',
    'jydymai': 'img/to-fractions/15-jydymai.png',
    'suroo-tuz': 'img/to-fractions/16-suroo-tuz.png',
}

TO_FRACTIONS = {
    'title': 'Ондуктарды бөлчөккө айландыруу',
    'svg_dir': 'svg/topic/to-fractions',
    'file_prefix': 'Ekvivalenettuuluk_Onduktardan_menen_Bolchoktor-',
    'images': TO_FRACTIONS_IMAGES,
    # Same gate as templates/components/operation_block.html: logged-out
    # visitors can see the page, but the file buttons become a register
    # prompt, and an expired subscription shows the renew prompt.
    'downloads_gated': True,
    'standard': STANDARD_REF,
    # Pedagogy guides that cut across every stage above, rather than
    # belonging to one - shown in the teacher guide panel.
    'teacher_resources': [
        {
            'title': 'Сингапур математикасынын ыкмалары',
            'note': '6 класстык ыкма: КСБ прогресс, бар-модель, сан байланыштары, жумалык '
            'кайталоо, 4 кадамдуу ой жүгүртүү, математикалык сүйлөшүү.',
            'files': [('PPT', 'SingaporeMathYkmalary.pptx')],
        },
    ],
    'sections': [
        {
            'stage': '5E · 1',
            'title': 'Кызыктыруу',
            'title_en': 'Engage',
            'when': 'Сабактын башында, 5–7 мүнөт: мурунку билимди текшерип, кызыгууну ойготуу.',
            'bloom': ['Эстеп калуу'],
            'summary': 'Мурунку билимди эске салуу: окуучулар 0,1 = 1/10 сыяктуу негизги айландырууларды '
            'билеби?',
            'items': [
                {
                    'title': '1234',
                    'note': 'Төрт кутуча: жөнөкөй ондуктан баштап үч орундуу ондукка чейин',
                    'svg': '1234',
                    'level': 'Эстеп калуу',
                    'files': [('PPT', '1234.pptx')],
                },
                {
                    'title': 'Бинго',
                    'note': 'Бүт класс менен: мугалим ондукту айтат, окуучулар бөлчөгүн табат',
                    'svg': 'bingo',
                    'level': 'Эстеп калуу',
                    'files': [('PPT', 'BingoOyunu.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 2',
            'title': 'Изилдөө',
            'title_en': 'Explore',
            'when': 'Эрежени айтуудан мурун: окуучулар жуп же топ болуп мисалдарды изилдеп, мыйзам ченемдүүлүктү өздөрү табышат.',
            'bloom': ['Түшүнүү', 'Талдоо'],
            'summary': 'Эрежени айтпай туруп, окуучулар ондук менен бөлчөктүн байланышын өздөрү '
            'табышат.',
            'items': [
                {
                    'title': 'Көрсөт / Ооба, жок, балким',
                    'note': 'Тактачага жооп көрсөтүп, ар бир пикирди негиздешет',
                    'svg': 'korsot-ooba-jok',
                    'level': 'Түшүнүү',
                    'files': [
                        ('PPT', 'IzildooKorsotOobaJok.pptx'),
                        ('PDF', 'IzildooKorsotOobaJok.pdf'),
                    ],
                },
                {
                    'title': 'Цифра табышмагы',
                    'note': 'Бош кутучаларга цифра коюп, ½ке барабар бөлчөктөрдү издешет',
                    'svg': 'cifra-tabyshmagy',
                    'level': 'Талдоо',
                    'files': [
                        ('PPT', 'CifraTabyshmagy.pptx'),
                        ('PDF A5', 'CifraTabyshmagy.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '5E · 3',
            'title': 'Түшүндүрүү',
            'title_en': 'Explain',
            'when': 'Изилдөөдөн кийин: мугалим эрежени жана үлгүнү көрсөтөт, окуучулар «Сенин кезегиң» менен текшерет.',
            'bloom': ['Түшүнүү', 'Колдонуу'],
            'summary': 'Орундук маани → бөлүмү 10, 100, 1000 → жөнөкөйлөтүү: үлгү жана «Сенин '
            'кезегиң».',
            'items': [
                {
                    'title': 'Түшүндүрүү презентациясы',
                    'note': 'Эреже, үч үлгү (0,6; 0,35; 0,125) жана ар биринен кийин өз алдынча мисал',
                    'svg': 'tushunduruu',
                    'level': 'Түшүнүү',
                    'files': [
                        ('PPT', 'TushunduruuPrezentaciya.pptx'),
                        ('PDF', 'TushunduruuPrezentaciya.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '5E · 4',
            'title': 'Тереңдетүү',
            'title_en': 'Elaborate',
            'when': 'Негизги машыгуу: окуучу өз деңгээлиндеги тапшырманы аткарат (программа сунуштаган деңгээлдик дифференциация).',
            'bloom': ['Колдонуу', 'Түшүнүү'],
            'summary': 'Айландырууну деңгээл боюнча машыгуу жана орундук маани аркылуу тереңдетүү.',
            'items': [
                {
                    'title': 'Жеңил, орто, оор',
                    'note': 'Үч деңгээлде 6дан суроо, деңгээлин окуучу өзү тандайт',
                    'svg': 'jenil-orto-oor',
                    'level': 'Колдонуу',
                    'files': [('PPT', 'JenilOrtoOor.pptx')],
                },
                {
                    'title': 'Казына издөө',
                    'note': 'Жеңил: плакаттан плакатка, жооп кийинки суроону көрсөтөт',
                    'svg': 'kazyna-jenil',
                    'level': 'Колдонуу',
                    'files': [
                        ('PPT', 'KazynaIzdoo_Jenil.pptx'),
                        ('PDF A4', 'KazynaIzdoo_Jenil.pdf'),
                    ],
                },
                {
                    'title': 'Казына издөө',
                    'note': 'Оор: плакаттан плакатка, жооп кийинки суроону көрсөтөт',
                    'svg': 'kazyna-oor',
                    'level': 'Колдонуу',
                    'files': [('PPT', 'KazynaIzdoo_Oor.pptx'), ('PDF A4', 'KazynaIzdoo_OorA4.pdf')],
                },
                {
                    'title': 'Бинго',
                    'note': 'Цифранын орундук маанисин жөнөкөйлөтүлгөн бөлчөк менен жазышат',
                    'svg': 'bingo-orun',
                    'level': 'Түшүнүү',
                    'files': [('PPT', 'BingoOyunuOrundardynMaanisiMenen.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 5',
            'title': 'Баалоо',
            'title_en': 'Evaluate',
            'when': 'Сабактын аягында же темадан кийин: окуучулар каталарды таап, жоопту негиздешет.',
            'bloom': ['Талдоо', 'Баалоо', 'Жаратуу'],
            'summary': 'Окуучулар даяр жоопторду текшерип, туура же ката экенин негиздешет.',
            'items': [
                {
                    'title': 'Катаны тап',
                    'note': 'Чечилген мисалдагы каталарды таап, оңдошот',
                    'svg': 'katany-tap',
                    'level': 'Баалоо',
                    'files': [
                        ('PPT', 'KatanyTap.pptx'),
                        ('PDF A4', 'KatanyTapA4.pdf'),
                        ('PDF A5', 'KatanyTapA5.pdf'),
                    ],
                },
                {
                    'title': 'Сандар менен лабиринт',
                    'note': 'Туура айландырылган бөлмөлөр аркылуу гана өтүшөт; аягында өз лабиринтин '
                    'түзүшөт',
                    'svg': 'sandar-labyrinth',
                    'level': 'Баалоо',
                    'files': [
                        ('PPT', 'SandarMNLabyrinth.pptx'),
                        ('PDF A4', 'SandarMNLabyrinthA4.pdf'),
                        ('PDF A5', 'SandarMNLabyrinthA5.pdf'),
                        ('PDF A6', 'SandarMNLabyrinthA6.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '3C · 1',
            'title': 'Байланыштыруу',
            'title_en': 'Connect',
            'when': 'Бир эле санды ондук жана бөлчөк түрүндө байланыштырып, тема аралык байланышты көрүшөт.',
            'bloom': ['Талдоо'],
            'summary': 'Бир эле санды ондук жана бөлчөк түрүндө байланыштыруу.',
            'items': [
                {
                    'title': 'Тарсиа курак',
                    'note': 'Ондукту барабар бөлчөгү менен жанаштырып, үч бурчтук түзүшөт',
                    'svg': 'tarsia-kurak',
                    'level': 'Талдоо',
                    'files': [
                        ('PPT', 'TarsiaKurak.pptx'),
                        ('PDF A4', 'TarsiaKurakA4.pdf'),
                        ('PDF A5', 'TarsiaKurakA5.pdf'),
                    ],
                }
            ],
        },
        {
            'stage': '3C · 2',
            'title': 'Кызматташуу',
            'title_en': 'Collaborate',
            'when': 'Жуп же топ менен оюн: программа жуп, топтук жана фронталдык иштөөнү сунуштайт.',
            'bloom': ['Колдонуу'],
            'summary': 'Жуп жана команда менен оюндар.',
            'items': [
                {
                    'title': 'Катары менен төрт',
                    'note': 'Жуп болуп: суроону тандап, жоопту торчодон белгилешет',
                    'svg': 'katary-menen-tort',
                    'level': 'Колдонуу',
                    'files': [
                        ('PPT', 'KataryMenenTort.pptx'),
                        ('PDF A4', 'KataryMenenTortA4.pdf'),
                        ('PDF A5', 'KataryMenenTortA5.pdf'),
                        ('PDF A6', 'KataryMenenTortA6.pdf'),
                    ],
                },
                {
                    'title': '3-ту туташтыр',
                    'note': 'Эки команда кезек менен жооп берип, торчодон орун алат',
                    'svg': '3-tutashtyr',
                    'level': 'Колдонуу',
                    'files': [('PPT', '3Tutashtyr.pptx')],
                },
                {
                    'title': 'Жыдымай',
                    'note': 'Команда же жекеме-жеке: туура жоопту биринчи басышат',
                    'svg': 'jydymai',
                    'level': 'Колдонуу',
                    'files': [('PPT', 'Jydymai.pptx')],
                },
            ],
        },
        {
            'stage': '3C · 3',
            'title': 'Жаратуу',
            'title_en': 'Create',
            'when': 'Тереңдетилген деңгээл же үй тапшырмасы: окуучулар өз суроосун, карталарын түзүшөт.',
            'bloom': ['Жаратуу'],
            'summary': 'Окуучулар өздөрү суроо, домино карталарын түзүп, классташтарына беришет.',
            'items': [
                {
                    'title': 'Суроо түз',
                    'note': 'Ондукту бөлчөккө айландырып, жөнөкөйлөтүүнү талап кылган суроо жана '
                    'өз домино карталарын түзүшөт',
                    'svg': 'suroo-tuz',
                    'level': 'Жаратуу',
                    'files': [
                        ('PPT', 'SurooTuz.pptx'),
                        ('Домино', 'SurooTuzKartalar.pptx'),
                        ('PDF A5', 'SurooTuz.pdf'),
                    ],
                },
            ],
        },
    ],
}


# Same lesson-page shape as TO_FRACTIONS. Materials stay in the order they
# had on the older four_basic_operations page; only the section they sit in
# changes. `page_key` is the stored free-download row. That row still points
# at this page's free file: amaldar_tartibi_ozun_tuz_v2.pptx.
FOUR_BASIC_IMAGES = {
    'intro': 'img/four-basic-operations/01-intro.png',
    'jenil-orto-oor': 'img/four-basic-operations/02-jenil-orto-oor.png',
    'amaldar-tartibi': 'img/four-basic-operations/03-amaldar-tartibi.png',
    'cifra': 'img/four-basic-operations/04-cifra.png',
    'katany-tap': 'img/four-basic-operations/05-katany-tap.png',
    'labyrinth': 'img/four-basic-operations/06-labyrinth.png',
    'practice-1': 'img/four-basic-operations/07-practice-1.png',
    'practice-2': 'img/four-basic-operations/08-practice-2.png',
    'decision': 'img/four-basic-operations/09-decision.png',
    'tarsia': 'img/four-basic-operations/10-tarsia.png',
    'compare': 'img/four-basic-operations/11-compare.png',
    'bingo': 'img/four-basic-operations/12-bingo.png',
    'penalty': 'img/four-basic-operations/13-penalty.png',
    'race': 'img/four-basic-operations/14-race.png',
    'show-example': 'img/four-basic-operations/15-show-example.png',
}

FOUR_BASIC_OPERATIONS = {
    'title': 'Төрт амал',
    'svg_dir': 'svg/topic/four-basic-operations',
    'file_prefix': '',
    'page_key': 'four_basic_operations',
    'images': FOUR_BASIC_IMAGES,
    'downloads_gated': True,
    'sections': [
        {
            'stage': '5E · 3',
            'title': 'Түшүндүрүү',
            'title_en': 'Explain',
            'when': 'Сабактын башында: мугалим төрт амалды үлгү менен көрсөтөт.',
            'bloom': ['Түшүнүү'],
            'summary': 'Кошуу, кемитүү, көбөйтүү жана бөлүүнүн үлгүсү.',
            'items': [
                {
                    'title': 'Сабактын көрсөтүү - түшүндүрүү',
                    'note': 'Мугалим төрт амалды (+ − × ÷) үлгү менен көрсөтөт.',
                    'svg': 'intro',
                    'level': 'Түшүнүү',
                    'files': [('PPT', '4-Amal-intro.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 4',
            'title': 'Тереңдетүү',
            'title_en': 'Elaborate',
            'when': 'Окуучу өз деңгээлиндеги тапшырманы тандайт.',
            'bloom': ['Колдонуу'],
            'summary': 'Жеңил, орто жана оор мисалдар.',
            'items': [
                {
                    'title': 'Жеңил, орто, оор',
                    'note': 'Үч деңгээл: жеңил, орто, оор.',
                    'svg': 'jenil-orto-oor',
                    'level': 'Колдонуу',
                    'files': [('PPT', '4-amal-JenilOrtoOor.pptx')],
                },
            ],
        },
        {
            'stage': '3C · 3',
            'title': 'Жаратуу',
            'title_en': 'Create',
            'when': 'Тереңдетилген деңгээл же үй тапшырмасы: окуучулар өз мисалын түзүшөт.',
            'bloom': ['Жаратуу'],
            'summary': 'Берилген сандардан жообу 10 болгон мисал түзүшөт.',
            'items': [
                {
                    'title': 'Амалдар тартиби: Өзүң түз',
                    'note': '4, 2, 3 жана 6 сандарын бир жолудан колдонуп, жообу 10 болгон мисал түзүшөт.',
                    'svg': 'amaldar-tartibi',
                    'level': 'Жаратуу',
                    'files': [('PPT', 'amaldar_tartibi_ozun_tuz_v2.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 2',
            'title': 'Изилдөө',
            'title_en': 'Explore',
            'when': 'Бош кутучаларга цифра коюп, мисалды өздөрү толукташат.',
            'bloom': ['Талдоо'],
            'summary': 'Жетишпеген цифраны издөө.',
            'items': [
                {
                    'title': 'Цифралык табышмак',
                    'note': '3 деңгээлде.',
                    'svg': 'cifra',
                    'level': 'Талдоо',
                    'files': [
                        ('PPT', '4-amal-sandyk-bashkatyrma.pptx'),
                        ('PDF A6', '4-amal-sandyk-bashkatyrmaA6.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '5E · 5',
            'title': 'Баалоо',
            'title_en': 'Evaluate',
            'when': 'Даяр жоопту текшерип, туура же ката экенин негиздешет.',
            'bloom': ['Баалоо'],
            'summary': 'Катаны табуу жана туура мисалдар аркылуу өтүү.',
            'items': [
                {
                    'title': 'Катаны тап',
                    'note': 'Чечилген мисалдагы каталарды таап, оңдошот.',
                    'svg': 'katany-tap',
                    'level': 'Баалоо',
                    'files': [
                        ('PPT', '4-Amal-katanytapTarsia.pptx'),
                        ('PDF A4', '4-Amal-katanytapTarsiaA4.pdf'),
                        ('PDF A5', '4-Amal-katanytapTarsiaA5.pdf'),
                    ],
                },
                {
                    'title': 'Туура же Ката лабиринт',
                    'note': 'Туура мисалдар аркылуу гана өтүшөт.',
                    'svg': 'labyrinth',
                    'level': 'Баалоо',
                    'files': [
                        ('PPT', '4-amal-tuuraKataLabirinth.pptx'),
                        ('PDF A4', '4-amal-tuuraKataLabirinthA4.pdf'),
                        ('PDF A5', '4-amal-tuuraKataLabirinthA5.pdf'),
                        ('PDF A6', '4-amal-tuuraKataLabirinthA6.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '5E · 4',
            'title': 'Тереңдетүү',
            'title_en': 'Elaborate',
            'when': 'Өз алдынча машыгуу.',
            'bloom': ['Колдонуу'],
            'summary': 'Тема боюнча көнүгүүлөр.',
            'items': [
                {
                    'title': 'Теманын көнүгүүсү 1',
                    'note': 'Тема боюнча биринчи көнүгүү.',
                    'svg': 'practice-1',
                    'level': 'Колдонуу',
                    'files': [
                        ('PPT', '4-amal-kondumA.pptx'),
                        ('PDF A5', '4-amal-kondumAA5.pdf'),
                    ],
                },
                {
                    'title': 'Теманын көнүгүүсү 2',
                    'note': 'Тема боюнча экинчи көнүгүү.',
                    'svg': 'practice-2',
                    'level': 'Колдонуу',
                    'files': [
                        ('PPT', '4-Amal - FourFour.pptx'),
                        ('PDF A4', '4-Amal - FourFourA4.pdf'),
                        ('PDF A5', '4-Amal - FourFourA5.pdf'),
                        ('PDF A6', '4-Amal - FourFourA6.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '5E · 5',
            'title': 'Баалоо',
            'title_en': 'Evaluate',
            'when': 'Мисал туурабы же катабы — окуучу чечим чыгарат.',
            'bloom': ['Баалоо'],
            'summary': 'Туура же ката жоопту айырмалоо.',
            'items': [
                {
                    'title': 'Чечим чыгаруу',
                    'note': 'Туура же ката экенин белгилешет.',
                    'svg': 'decision',
                    'level': 'Баалоо',
                    'files': [
                        ('PPT', '4-Amal-TuuraJeKata.pptx'),
                        ('PDF A4', '4-Amal-TuuraJeKataA4.pdf'),
                        ('PDF A5', '4-Amal-TuuraJeKataA5.pdf'),
                        ('PDF A6', '4-Amal-TuuraJeKataA6.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '3C · 1',
            'title': 'Байланыштыруу',
            'title_en': 'Connect',
            'when': 'Мисал менен жообун жана эки мисалды өз ара байланыштырышат.',
            'bloom': ['Талдоо'],
            'summary': 'Мисалды жообу менен жанаштыруу жана салыштыруу.',
            'items': [
                {
                    'title': 'Тарсия курак',
                    'note': 'Мисал менен жообун жанаштырып, үч бурчтук түзүшөт.',
                    'svg': 'tarsia',
                    'level': 'Талдоо',
                    'files': [
                        ('PPT', '4-Amal-TarsiaKurak.pptx'),
                        ('PDF A4', '4-Amal-TarsiaKurakA4.pdf'),
                        ('PDF A5', '4-Amal-TarsiaKurakA5.pdf'),
                    ],
                },
                {
                    'title': 'Салыштыруу',
                    'note': 'Эки мисалды салыштырып, чоң, кичине же барабар экенин табышат.',
                    'svg': 'compare',
                    'level': 'Талдоо',
                    'files': [
                        ('PPT', '4-Amal - Salyshtyr.pptx'),
                        ('PDF A4', '4-Amal - SalyshtyrA4.pdf'),
                        ('PDF A5', '4-Amal - SalyshtyrA5.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '3C · 2',
            'title': 'Кызматташуу',
            'title_en': 'Collaborate',
            'when': 'Бүт класс менен, мугалим жетектейт.',
            'bloom': ['Колдонуу'],
            'summary': 'Мугалим жетектеген оюндар.',
            'items': [
                {
                    'title': 'Бинго',
                    'note': 'Бүт класс менен: мугалим мисал айтат, окуучулар жообун табат.',
                    'svg': 'bingo',
                    'level': 'Колдонуу',
                    'files': [('PPT', '4-Amal-BingoOyunu.pptx')],
                },
                {
                    'title': 'Айып сокку',
                    'note': 'Туура жооп берсе, айып сокку урат.',
                    'svg': 'penalty',
                    'level': 'Колдонуу',
                    'files': [('PPT', '4-Amal-AyipSokku.pptx')],
                },
                {
                    'title': 'Жыдымай оюну',
                    'note': 'Туура жоопту биринчи басышат.',
                    'svg': 'race',
                    'level': 'Колдонуу',
                    'files': [('PPT', '4-Amal-JydymaiOyunu.pptx')],
                },
                {
                    'title': 'Мисал көрсөт',
                    'note': 'Мугалим мисал көрсөтөт, окуучулар жооп берет.',
                    'svg': 'show-example',
                    'level': 'Колдонуу',
                    'files': [('PPT', '4-Amal-MisalKorsot.pptx')],
                },
            ],
        },
    ],
}


# A simpler page than TO_FRACTIONS: this skill (using a calculator with
# fractions) isn't taught through the 5E + 3C lesson flow, so sections are
# grouped by resource type instead of lesson stage. Items still carry a
# Bloom level - the template needs it for the ladder/staircase - chosen by
# what each activity actually asks the pupil to do.
def _add_grade_items(page, grade_items, teacher_files, image_dir):
    """Put grade-level items into the first section with the same title.

    Items already on the page get grade 0 and show under the «Жалпы» tab.
    """
    for section in page['sections']:
        for item in section['items']:
            item.setdefault('grade', 0)
    for section_title, item in grade_items:
        section = next(s for s in page['sections'] if s['title'] == section_title)
        section['items'].append(item)
        page['images'][item['svg']] = f"{image_dir}{item['svg']}.webp"
    page['teacher_resources'] = page.get('teacher_resources', []) + [
        {
            'title': f'{grade}-класс · {subtopic}: класста колдонуу',
            'note': '40 мүнөттүк план, буюмдар, доска, трекер.',
            'files': [('PDF', name)],
            'grade': grade,
        }
        for grade, subtopic, name in teacher_files
    ]


_add_grade_items(FOUR_BASIC_OPERATIONS, GRADE_ITEMS, GRADE_TEACHER_FILES, GRADE_IMAGE_DIR)

# The page's older «Жалпы» files were built on goteachmaths templates and
# were taken off the site on 2026-10-24 (migration 0033 hides their rows).
# Only our own «Өзүң түз» deck stays in Жалпы.
KEEP_GENERAL_FILES = {'amaldar_tartibi_ozun_tuz_v2.pptx'}


def _drop_old_general_items(page):
    for section in page['sections']:
        section['items'] = [
            item for item in section['items']
            if item.get('grade') or any(name in KEEP_GENERAL_FILES for _label, name in item['files'])
        ]
    page['sections'] = [s for s in page['sections'] if s['items']]


_drop_old_general_items(FOUR_BASIC_OPERATIONS)

# Tab labels for pages whose items carry a grade; 0 = materials for any grade.
GRADE_LABELS = {0: 'Жалпы', 1: '1-класс', 2: '2-класс', 3: '3-класс', 4: '4-класс', 5: '5-класс', 6: '6-класс'}


CALCULATOR_FRACTIONS = {
    'title': 'Калькулятордо бөлчөктөр',
    'svg_dir': 'svg/topic/calculator-fractions',
    'file_prefix': 'KalkulyatorKoldonuu_Bolchoktor-',
    'model_label': 'Блум',
    'stages_label': 'Материалдардын түрлөрү',
    'sections': [
        {
            'stage': '1',
            'title': 'Иш баракчалар',
            'title_en': 'Worksheets',
            'when': 'Өз алдынча же үй тапшырмасы катары.',
            'bloom': ['Баалоо'],
            'summary': 'Эсептегич менен чыгарылган мисалдарды текшерип, каталарды табуу.',
            'items': [
                {
                    'title': 'Катаны тап',
                    'note': 'Эсептегич менен чыгарылган мисалдардагы каталарды таап, оңдошот',
                    'svg': 'katany-tap',
                    'level': 'Баалоо',
                    'files': [('PPT', 'KatanyTap.pptx')],
                },
            ],
        },
        {
            'stage': '2',
            'title': 'Ишмердиктер',
            'title_en': 'Activities',
            'when': 'Жуп же кичине топ менен, 15-20 мүнөт.',
            'bloom': ['Талдоо'],
            'summary': 'Эсептегич менен чыгарылган жооптор боюнча дал келген кесимдерди табуу.',
            'items': [
                {
                    'title': 'Тарсия курак',
                    'note': 'Мисал менен жообун тамга боюнча дал келтиришет; каалаганда кесип жанаштырса да болот',
                    'svg': 'tarsia-kurak',
                    'level': 'Талдоо',
                    'files': [('PPT', 'TarsiaKurak.pptx')],
                },
            ],
        },
        {
            'stage': '3',
            'title': 'Мугалим жетектеген оюндар',
            'title_en': 'Teacher-led activities',
            'when': 'Бүт класс менен, тактага чыгарылып ойнолот.',
            'bloom': ['Колдонуу'],
            'summary': 'Мугалим мисал окуйт же көрсөтөт, окуучулар эсептегич менен чыгарышат.',
            'items': [
                {
                    'title': 'Бинго: Ыкма',
                    'note': 'Окуучулар 3×3 тор тартышат, мисалдар бирден көрсөтүлөт, жооптор боюнча торду толтурушат',
                    'svg': 'bingo-ykma',
                    'level': 'Колдонуу',
                    'files': [('PPT', 'BingoYkma.pptx')],
                },
                {
                    'title': 'Жыдымай',
                    'note': '«Даярсыңбы? Старт!» — эки команда тең эсептегич менен тез жана так чыгарат',
                    'svg': 'jydymai',
                    'level': 'Колдонуу',
                    'files': [('PPT', 'Jydymai.pptx')],
                },
            ],
        },
    ],
}


def _page_file_groups(page):
    groups = []
    for section in page['sections']:
        for item in section['items']:
            groups.append(item['files'])
    for res in page.get('teacher_resources', []):
        groups.append(res['files'])
    return groups


def _page_candidates(page, resources):
    prefix = page['file_prefix']
    ordered = []
    seen = set()
    for files in _page_file_groups(page):
        for _label, name in files:
            resource = resource_for_title(resources, prefix + name)
            if resource and resource.id not in seen:
                seen.add(resource.id)
                ordered.append(resource)
    return ordered


def _resolve_links(file_prefix, files, resources, user, register_url, free_id):
    links = []
    for label, name in files:
        resource = resource_for_title(resources, file_prefix + name)
        if not resource:
            continue
        free = bool(free_id and resource.id == free_id)
        if free or user.is_authenticated:
            url = reverse('download_resource', kwargs={'pk': resource.id})
        else:
            url = register_url
        links.append({'label': label, 'url': url, 'free': free})
    return links


def build_topic_page(page, resources, user):
    """Resolve a page spec into template context: svg paths and real links.

    Logged-out visitors see the same buttons, pointing at registration,
    so they can tell what formats exist before signing up. One file on
    the page is the exception: it stays a real download for everyone.
    """
    register_url = reverse('register')
    images = page.get('images') or {}
    page_key = page.get('page_key') or page['file_prefix']
    free = choose_free_resource(page_key, _page_candidates(page, resources))
    free_id = free.id if free else None
    sections = []
    for section in page['sections']:
        items = []
        for item in section['items']:
            links = _resolve_links(
                page['file_prefix'], item['files'], resources, user, register_url, free_id,
            )
            svg_path = f"{page['svg_dir']}/{item['svg']}.svg"
            items.append(
                {
                    'title': item['title'],
                    'note': item['note'],
                    'svg': svg_path,
                    'image': images.get(item['svg']),
                    'level': item['level'],
                    'level_num': BLOOM_LEVELS.index(item['level']) + 1,
                    'links': links,
                    'has_locked': any(not link['free'] for link in links),
                    'grade': item.get('grade'),
                    'subtopic': item.get('subtopic'),
                }
            )
        sections.append({**section, 'items': items})

    teacher_resources = []
    for res in page.get('teacher_resources', []):
        links = _resolve_links(
            page['file_prefix'], res['files'], resources, user, register_url, free_id,
        )
        if links:
            teacher_resources.append({
                'title': res['title'],
                'note': res['note'],
                'links': links,
                'has_locked': any(not link['free'] for link in links),
                'grade': res.get('grade', 0),
            })

    grade_nums = sorted({i['grade'] for s in sections for i in s['items'] if i['grade'] is not None})
    grades = []
    if len(grade_nums) > 1:
        grades = [
            {
                'num': g,
                'label': GRADE_LABELS[g],
                'count': sum(1 for s in sections for i in s['items'] if i['grade'] == g),
            }
            for g in grade_nums
        ]

    return {
        'title': page['title'],
        # Menu path above the title and a grade badge for single-grade pages.
        'crumb': page.get('crumb'),
        'grade_badge': page.get('grade_badge'),
        # The same topic in the grades before and after (data/spiral.py).
        'strands': page.get('strands', []),
        # Grade tabs (empty for pages without grade-level items).
        'grades': grades,
        'model_label': page.get('model_label', '5E + 3C жана Блум'),
        'stages_label': page.get('stages_label', 'Сабактын этаптары (5E + 3C)'),
        'sections': sections,
        'bloom_guide': [(level, BLOOM_GUIDE[level]) for level in BLOOM_LEVELS],
        # Staircase above the list: how many materials reach each level.
        'bloom_steps': [
            {
                'num': n,
                'level': level,
                'count': sum(1 for s in sections for i in s['items'] if i['level'] == level),
            }
            for n, level in enumerate(BLOOM_LEVELS, 1)
        ],
        'downloads_gated': page.get('downloads_gated', False),
        'uses_mk_zoom': bool(images),
        'standard': page.get('standard'),
        # Cross-cutting pedagogy guides (e.g. Singapore Math strategies)
        # that apply across every Bloom stage - shown in the teacher
        # guide panel, not tagged to one section, since they don't
        # belong to a single stage the way a student activity does.
        'teacher_resources': teacher_resources,
    }
