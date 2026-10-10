"""Content for topic pages rendered with templates/resources/topic_materials.html.

A topic page lists its materials in sections. Each material has an SVG
thumbnail (templates/svg/topic/<page>/<name>.svg, inlined into the page)
and download buttons. A button only shows when its file exists as an
active Resource, matched by `Resource.title` the same way the older
hand-built templates do with `res|get_item:'filename'`.
"""

from django.urls import reverse

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

TO_FRACTIONS = {
    'title': 'Ондуктарды бөлчөккө айландыруу',
    'svg_dir': 'svg/topic/to-fractions',
    'file_prefix': 'Ekvivalenettuuluk_Onduktardan_menen_Bolchoktor-',
    'standard': STANDARD_REF,
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


def build_topic_page(page, resources, user):
    """Resolve a page spec into template context: svg paths and real links.

    Logged-out visitors see the same buttons, pointing at registration,
    so they can tell what formats exist before signing up.
    """
    register_url = reverse('register')
    sections = []
    for section in page['sections']:
        items = []
        for item in section['items']:
            links = []
            for label, name in item['files']:
                resource = resources.get(page['file_prefix'] + name)
                if not resource:
                    continue
                if user.is_authenticated:
                    url = reverse('download_resource', kwargs={'pk': resource.id})
                else:
                    url = register_url
                links.append({'label': label, 'url': url})
            svg_path = f"{page['svg_dir']}/{item['svg']}.svg"
            items.append(
                {
                    'title': item['title'],
                    'note': item['note'],
                    'svg': svg_path,
                    'level': item['level'],
                    'links': links,
                }
            )
        sections.append({**section, 'items': items})
    return {
        'title': page['title'],
        'sections': sections,
        'bloom_guide': [(level, BLOOM_GUIDE[level]) for level in BLOOM_LEVELS],
        'standard': page.get('standard'),
    }
