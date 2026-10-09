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
# (PR #3). This page has no Explore, Explain or Create materials yet.
TO_FRACTIONS = {
    'title': 'Ондуктарды бөлчөккө айландыруу',
    'svg_dir': 'svg/topic/to-fractions',
    'file_prefix': 'Ekvivalenettuuluk_Onduktardan_menen_Bolchoktor-',
    'sections': [
        {
            'stage': '5E · 1',
            'title': 'Кызыктыруу',
            'title_en': 'Engage',
            'bloom': ['Эстеп калуу'],
            'summary': 'Мурунку билимди эске салуу: окуучулар 0,1 = 1/10 сыяктуу негизги айландырууларды '
            'билеби?',
            'items': [
                {
                    'title': '1234',
                    'note': 'Төрт кутуча: жөнөкөй ондуктан баштап үч орундуу ондукка чейин',
                    'svg': '1234',
                    'files': [('PPT', '1234.pptx')],
                },
                {
                    'title': 'Бинго',
                    'note': 'Бүт класс менен: мугалим ондукту айтат, окуучулар бөлчөгүн табат',
                    'svg': 'bingo',
                    'files': [('PPT', 'BingoOyunu.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 4',
            'title': 'Тереңдетүү',
            'title_en': 'Elaborate',
            'bloom': ['Колдонуу', 'Түшүнүү'],
            'summary': 'Айландырууну деңгээл боюнча машыгуу жана орундук маани аркылуу тереңдетүү.',
            'items': [
                {
                    'title': 'Жеңил, орто, оор',
                    'note': 'Үч деңгээлде 6дан суроо, деңгээлин окуучу өзү тандайт',
                    'svg': 'jenil-orto-oor',
                    'files': [('PPT', 'JenilOrtoOor.pptx')],
                },
                {
                    'title': 'Казына издөө',
                    'note': 'Жеңил: плакаттан плакатка, жооп кийинки суроону көрсөтөт',
                    'svg': 'kazyna-jenil',
                    'files': [
                        ('PPT', 'KazynaIzdoo_Jenil.pptx'),
                        ('PDF A4', 'KazynaIzdoo_Jenil.pdf'),
                    ],
                },
                {
                    'title': 'Казына издөө',
                    'note': 'Оор: плакаттан плакатка, жооп кийинки суроону көрсөтөт',
                    'svg': 'kazyna-oor',
                    'files': [('PPT', 'KazynaIzdoo_Oor.pptx'), ('PDF A4', 'KazynaIzdoo_OorA4.pdf')],
                },
                {
                    'title': 'Бинго',
                    'note': 'Цифранын орундук маанисин жөнөкөйлөтүлгөн бөлчөк менен жазышат',
                    'svg': 'bingo-orun',
                    'files': [('PPT', 'BingoOyunuOrundardynMaanisiMenen.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 5',
            'title': 'Баалоо',
            'title_en': 'Evaluate',
            'bloom': ['Талдоо', 'Баалоо', 'Жаратуу'],
            'summary': 'Окуучулар даяр жоопторду текшерип, туура же ката экенин негиздешет.',
            'items': [
                {
                    'title': 'Катаны тап',
                    'note': 'Чечилген мисалдагы каталарды таап, оңдошот',
                    'svg': 'katany-tap',
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
            'bloom': ['Талдоо'],
            'summary': 'Бир эле санды ондук жана бөлчөк түрүндө байланыштыруу.',
            'items': [
                {
                    'title': 'Тарсиа курак',
                    'note': 'Ондукту барабар бөлчөгү менен жанаштырып, үч бурчтук түзүшөт',
                    'svg': 'tarsia-kurak',
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
            'bloom': ['Колдонуу'],
            'summary': 'Жуп жана команда менен оюндар.',
            'items': [
                {
                    'title': 'Катары менен төрт',
                    'note': 'Жуп болуп: суроону тандап, жоопту торчодон белгилешет',
                    'svg': 'katary-menen-tort',
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
                    'files': [('PPT', '3Tutashtyr.pptx')],
                },
                {
                    'title': 'Жыдымай',
                    'note': 'Команда же жекеме-жеке: туура жоопту биринчи басышат',
                    'svg': 'jydymai',
                    'files': [('PPT', 'Jydymai.pptx')],
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
            items.append(
                {
                    'title': item['title'],
                    'note': item['note'],
                    'svg': f"{page['svg_dir']}/{item['svg']}.svg",
                    'links': links,
                }
            )
        sections.append({**section, 'items': items})
    return {
        'title': page['title'],
        'sections': sections,
    }
