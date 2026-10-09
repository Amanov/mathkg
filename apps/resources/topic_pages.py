"""Content for topic pages rendered with templates/resources/topic_materials.html.

A topic page lists its materials in sections. Each material has an SVG
thumbnail (templates/svg/topic/<page>/<name>.svg, inlined into the page)
and download buttons. A button only shows when its file exists as an
active Resource, matched by `Resource.title` the same way the older
hand-built templates do with `res|get_item:'filename'`.
"""

from django.urls import reverse

# Sections follow the 5E + 3C lesson model, each with the Bloom's taxonomy
# levels it mainly works on. Stage names, summaries and Bloom levels match
# STAGES in apps/resources/lesson_flow.py on the landing-5e-3c-bloom branch
# (PR #3). Only stages this page has materials for are listed.
TO_FRACTIONS = {
    'title': 'Ондуктарды бөлчөккө айландыруу',
    'breadcrumb': ['Сандар', 'Ондуктар', 'Эквиваленттүүлүк'],
    'svg_dir': 'svg/topic/to-fractions',
    'file_prefix': 'Ekvivalenettuuluk_Onduktardan_menen_Bolchoktor-',
    'sections': [
        {
            'stage': '5E · 1',
            'title': 'Кызыктыруу',
            'title_en': 'Engage',
            'bloom': ['Эстеп калуу'],
            'summary': 'Мурунку билимди эске салып, сабакка кызыгууну ойготуу.',
            'items': [
                {
                    'title': 'Жеңил, орто, оор',
                    'note': 'Үч деңгээлдеги көрсөтмө суроолор',
                    'svg': 'jenil-orto-oor',
                    'files': [('PPT', 'JenilOrtoOor.pptx')],
                },
                {
                    'title': '1234',
                    'note': 'Төрт жооптун ичинен туурасын тандашат',
                    'svg': '1234',
                    'files': [('PPT', '1234.pptx')],
                },
            ],
        },
        {
            'stage': '5E · 4',
            'title': 'Тереңдетүү',
            'title_en': 'Elaborate',
            'bloom': ['Колдонуу', 'Талдоо'],
            'summary': 'Билимди жаңы маселелерде бышыктоо, деңгээл боюнча машыгуу.',
            'items': [
                {
                    'title': 'Катары менен төрт',
                    'note': '2 деңгээлде',
                    'svg': 'katary-menen-tort',
                    'files': [
                        ('PPT', 'KataryMenenTort.pptx'),
                        ('PDF A4', 'KataryMenenTortA4.pdf'),
                        ('PDF A5', 'KataryMenenTortA5.pdf'),
                        ('PDF A6', 'KataryMenenTortA6.pdf'),
                    ],
                },
                {
                    'title': 'Сандар менен лабиринт',
                    'note': 'Туура жоопторду ээрчип, чыгууну табышат',
                    'svg': 'sandar-labyrinth',
                    'files': [
                        ('PPT', 'SandarMNLabyrinth.pptx'),
                        ('PDF A4', 'SandarMNLabyrinthA4.pdf'),
                        ('PDF A5', 'SandarMNLabyrinthA5.pdf'),
                        ('PDF A6', 'SandarMNLabyrinthA6.pdf'),
                    ],
                },
                {
                    'title': 'Тарсиа курак',
                    'note': 'Жооптору дал келген үч бурчтуктарды бириктиришет',
                    'svg': 'tarsia-kurak',
                    'files': [
                        ('PPT', 'TarsiaKurak.pptx'),
                        ('PDF A4', 'TarsiaKurakA4.pdf'),
                        ('PDF A5', 'TarsiaKurakA5.pdf'),
                    ],
                },
            ],
        },
        {
            'stage': '5E · 5',
            'title': 'Баалоо',
            'title_en': 'Evaluate',
            'bloom': ['Баалоо'],
            'summary': 'Түшүнүүнү текшерүү жана кийинки кадамды чечүү.',
            'items': [
                {
                    'title': 'Катаны тап',
                    'note': 'Окуучулар чечилген мисалдагы катаны издешет',
                    'svg': 'katany-tap',
                    'files': [
                        ('PPT', 'KatanyTap.pptx'),
                        ('PDF A4', 'KatanyTapA4.pdf'),
                        ('PDF A5', 'KatanyTapA5.pdf'),
                    ],
                }
            ],
        },
        {
            'stage': '3C · 1',
            'title': 'Байланыштыруу',
            'title_en': 'Connect',
            'bloom': ['Талдоо'],
            'summary': 'Түшүнүктөрдү бири-бирине жана турмушка байланыштыруу.',
            'items': [
                {
                    'title': '3-ту туташтыр',
                    'note': 'Суроо жана жооп тору',
                    'svg': '3-tutashtyr',
                    'files': [('PPT', '3Tutashtyr.pptx')],
                }
            ],
        },
        {
            'stage': '3C · 2',
            'title': 'Кызматташуу',
            'title_en': 'Collaborate',
            'bloom': ['Колдонуу', 'Талдоо'],
            'summary': 'Топтук жана жуп менен иштөө, мугалим жетектеген оюндар.',
            'items': [
                {
                    'title': 'Казына издөө',
                    'note': 'Жеңил',
                    'svg': 'kazyna-jenil',
                    'files': [
                        ('PPT', 'KazynaIzdoo_Jenil.pptx'),
                        ('PDF A4', 'KazynaIzdoo_Jenil.pdf'),
                    ],
                },
                {
                    'title': 'Казына издөө',
                    'note': 'Оор',
                    'svg': 'kazyna-oor',
                    'files': [('PPT', 'KazynaIzdoo_Oor.pptx'), ('PDF A4', 'KazynaIzdoo_OorA4.pdf')],
                },
                {
                    'title': 'Бинго',
                    'note': 'Бүт класс менен, слайддар',
                    'svg': 'bingo',
                    'files': [('PPT', 'BingoOyunu.pptx')],
                },
                {
                    'title': 'Бинго',
                    'note': 'Орундук мааниси менен',
                    'svg': 'bingo-orun',
                    'files': [('PPT', 'BingoOyunuOrundardynMaanisiMenen.pptx')],
                },
                {
                    'title': 'Жыдымай',
                    'note': 'Туура жоопту биринчи болуп басышат',
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
        'breadcrumb': page['breadcrumb'],
        'sections': sections,
    }
