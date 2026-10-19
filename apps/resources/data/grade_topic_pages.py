"""Topic pages in the «Төрт амал» layout for single topics (2026-10-19).

Three pages, as approved samples for moving the rest of the site:
- /koshuu-1-digit/ keeps its four existing files and gains a lesson deck
  and a worksheet; all of it is grade 5 (decimals with one decimal place).
- /integers-adding-subtracting-1-2-digit/ reuses the grade 1 and grade 2
  packs already shipped for «Төрт амал», plus a two-digit lesson deck.
- /hcf-lcm-prime-factorisation-mixed/ carries the grade 6 prime
  factorisation pack.

New files ship in apps/resources/bundled_files/ (migration 0031 adds their
Resource rows). Existing files on /koshuu-1-digit/ have no inside-page
preview yet, so they keep the designed SVGs from svg/topic/to-fractions.
"""

import copy

from apps.resources.data.four_basic_operations_grades import GRADE_IMAGE_DIR, GRADE_ITEMS

IMAGE_DIR = 'img/topic-pages/'

STAGES = [
    ('5E · 2', 'Изилдөө', 'Explore', 'Сабактын башында: окуучулар өздөрү издешет.', ['Талдоо'],
     'Жетишпеген цифраны же жолду издөө.'),
    ('5E · 3', 'Түшүндүрүү', 'Explain', 'Мугалим үлгү менен көрсөтөт: буюм → сүрөт → сан.', ['Түшүнүү'],
     'Сабактын презентациясы.'),
    ('5E · 4', 'Тереңдетүү', 'Elaborate', 'Окуучу өз деңгээлиндеги тапшырманы тандайт.', ['Колдонуу'],
     'Жеңил, орто жана оор мисалдар.'),
    ('5E · 5', 'Баалоо', 'Evaluate', 'Даяр жоопту текшерип, туура же ката экенин негиздешет.', ['Баалоо'],
     'Катаны табуу жана туура жол менен өтүү.'),
    ('3C · 1', 'Байланыштыруу', 'Connect', 'Мисал менен жообун байланыштырышат.', ['Талдоо'],
     'Жанаштыруу жана сорттоо.'),
    ('3C · 2', 'Кызматташуу', 'Collaborate', 'Бүт класс менен, мугалим жетектейт.', ['Колдонуу'],
     'Мугалим жетектеген оюндар.'),
]

TEACHER_NOTE = '40 мүнөттүк план, буюмдар, доска, трекер.'


def _item(section, grade, title, note, level, files, image=None, svg=None, subtopic=None):
    stem = svg or files[0][1].rsplit('.', 1)[0]
    return section, {
        'title': title, 'note': note, 'level': level, 'files': files, 'svg': stem,
        'grade': grade, 'subtopic': subtopic, 'image': image,
    }


def _page(title, page_key, crumb, badge, items, teacher=()):
    sections = [
        {'stage': stage, 'title': name, 'title_en': name_en, 'when': when, 'bloom': bloom,
         'summary': summary, 'items': []}
        for stage, name, name_en, when, bloom, summary in STAGES
    ]
    images = {}
    for section_title, item in items:
        image = item.pop('image')
        if image:
            images[item['svg']] = image
        next(s for s in sections if s['title'] == section_title)['items'].append(item)
    return {
        'title': title,
        'crumb': crumb,
        'grade_badge': badge,
        'svg_dir': 'svg/topic/to-fractions',
        'file_prefix': '',
        'page_key': page_key,
        'images': images,
        'downloads_gated': True,
        'sections': [s for s in sections if s['items']],
        'teacher_resources': list(teacher),
    }


KOSHUU_1_DIGIT = _page('Ондуктарды кошуу (1 ондук орун)', 'koshuu_1_digit', 'Сандар › Ондуктар › Эсептөөлөр', '5-класс', [
    _item('Түшүндүрүү', 5, 'Сабактын презентациясы',
          '14 слайд: тилке модели, разряддар таблицасы, мамычалап кошуу.', 'Түшүнүү',
          [('PPT', 'koshuu-1-digit-LessonDeck.pptx')], IMAGE_DIR + 'koshuu-1-digit-LessonDeck.webp'),
    _item('Тереңдетүү', 5, 'Иш барак: Жеңил, Орто, Оор', 'Үч деңгээл, жооп ачкычы менен.', 'Колдонуу',
          [('PDF A4', 'koshuu-1-digit-print.pdf')], IMAGE_DIR + 'koshuu-1-digit-print.webp'),
    _item('Тереңдетүү', 5, 'Кутучалар', 'Ондуктарды кошуу көнүгүүсү.', 'Колдонуу',
          [('PPT', 'Onduktar_KoshuuKutuchalary.pptx'), ('PDF', 'Onduktar_KoshuuKutuchalary.pdf'),
           ('XLSX', 'Onduktar_KoshuuKutuchalary.xlsx')], svg='jenil-orto-oor'),
    _item('Байланыштыруу', 5, 'Тарсия курак', 'Мисал менен жообун жанаштырышат.', 'Талдоо',
          [('PPT', 'Onduktar_KoshuuTarsiaKurak.pptx'), ('PDF A4', 'Onduktar_KoshuuTarsiaKurakA4.pdf'),
           ('PDF A5', 'Onduktar_KoshuuTarsiaKurakA5.pdf')], svg='tarsia-kurak'),
    _item('Кызматташуу', 5, 'Бинго', 'Бүт класс менен ойнойт.', 'Колдонуу',
          [('PPT', 'Onduktar_KoshuuBingo.pptx')], svg='bingo'),
    _item('Кызматташуу', 5, '3кө туташтыр', 'Үч жоопту катар туташтырышат.', 'Колдонуу',
          [('PPT', 'Onduktar_Koshuu3Tutashtyr.pptx')], svg='3-tutashtyr'),
])

K1A, K1K, K2A = '10 ичинде кошуу', '10 ичинде кемитүү', '100 ичинде кошуу жана кемитүү'
_integers = [
    _item('Түшүндүрүү', 2, 'Сабактын презентациясы: 2 орундуу сандар',
          '13 слайд: тилке модели, мамычалап кошуу жана кемитүү.', 'Түшүнүү',
          [('PPT', 'integers-adding-subtracting-1-2-digit-LessonDeck.pptx')],
          IMAGE_DIR + 'integers-adding-subtracting-1-2-digit-LessonDeck.webp', subtopic=K2A),
]
for _section, _src in GRADE_ITEMS:
    if _src['subtopic'] in (K1A, K1K, K2A):
        _i = copy.deepcopy(_src)
        _integers.append(_item(_section, _i['grade'], _i['title'], _i['note'], _i['level'], _i['files'],
                               f"{GRADE_IMAGE_DIR}{_i['svg']}.webp", subtopic=_i['subtopic']))

INTEGERS_ADD_SUB_1_2_DIGIT = _page(
    'Кошуу жана кемитүү: 1 жана 2 орундуу сандар', 'integers_adding_subtracting_1_2_digit',
    'Сандар › Бүтүн сандар › Эсептөөлөр', None, _integers, teacher=[
        {'title': '1-класс · 10 ичинде кошуу: класста колдонуу', 'note': TEACHER_NOTE,
         'files': [('PDF', '1-klass-10-ichinde-koshuu-klassta-koldonuu.pdf')], 'grade': 1},
        {'title': '2-класс · 100 ичинде: класста колдонуу', 'note': TEACHER_NOTE,
         'files': [('PDF', '2-klass-100-ichinde-klassta-koldonuu-v2.pdf')], 'grade': 2},
    ])

P6 = '6-klass-jonokoy-kobeytuuchuler-'


def _six(section, title, note, level, suffix, label='PDF A4'):
    ext = '.pptx' if label == 'PPT' else '.pdf'
    return _item(section, 6, title, note, level, [(label, P6 + suffix + ext)], IMAGE_DIR + P6 + suffix + '.webp')


HCF_LCM_PRIME_FACTORISATION = _page(
    'Эң чоң орток бөлүүчү жана эң кичине орток эселик', 'hcf_lcm_prime_factorisation_mixed',
    'Сандар › Бөлүүчүлөр, эселиктер жана жөнөкөй сандар', '6-класс', [
        _six('Изилдөө', 'Цифра табышмагы', 'Үч деңгээл: бош орунга цифра коюшат.', 'Талдоо', 'cifra-tabyshmagy'),
        _six('Түшүндүрүү', 'Сабактын презентациясы',
             '26 слайд: «Белек баштыктар» окуясы, көбөйтүүчү дарагы, эң чоң орток бөлүүчү жана эң кичине орток эселик.',
             'Түшүнүү', 'sabak', 'PPT'),
        _six('Тереңдетүү', 'Иш барак: Жеңил, Орто, Оор', '18 тапшырма жана тилке модели, жооп ачкычы менен.',
             'Колдонуу', 'ish-barak'),
        _six('Баалоо', 'Катаны тап', 'Алты окуучунун чыгарылышы: катаны таап, оңдошот.', 'Баалоо', 'katany-tap'),
        _six('Баалоо', 'Туура же ката лабиринт', 'Туура жооптор аркылуу гана өтүшөт.', 'Баалоо', 'labirint'),
        _six('Байланыштыруу', 'Домино', '12 карта: мисал менен жообу чынжыр түзөт.', 'Талдоо', 'domino'),
        _six('Байланыштыруу', 'Карта сорттоо', '12 карта: жөнөкөй жана курама сандар.', 'Талдоо', 'karta-sorttoo'),
        _six('Кызматташуу', '1234 оюну', 'Командалар менен, 9 слайд.', 'Колдонуу', 'oyun-1234', 'PPT'),
        _six('Кызматташуу', 'Атышуу', 'Эки команда, 25 слайд, ылдамдыксыз упай.', 'Колдонуу', 'oyun-atyshuu', 'PPT'),
    ], teacher=[
        {'title': '6-класс: класста колдонуу', 'note': TEACHER_NOTE,
         'files': [('PDF', P6 + 'klassta-koldonuu.pdf')], 'grade': 6},
        {'title': '6-класс: мугалимдин картасы', 'note': 'Типтүү каталар М1–М5, чечүүчү суроо, чыгуу билети.',
         'files': [('PDF', P6 + 'mugalim-kartasy.pdf')], 'grade': 6},
    ])

GRADE_TOPIC_PAGES = (KOSHUU_1_DIGIT, INTEGERS_ADD_SUB_1_2_DIGIT, HCF_LCM_PRIME_FACTORISATION)

# Files this module adds to the site (migration 0031 creates their rows).
NEW_FILES = [
    'koshuu-1-digit-LessonDeck.pptx',
    'koshuu-1-digit-print.pdf',
    'integers-adding-subtracting-1-2-digit-LessonDeck.pptx',
    '2-klass-100-ichinde-klassta-koldonuu-v2.pdf',
] + [P6 + s for s in (
    'sabak.pptx', 'oyun-1234.pptx', 'oyun-atyshuu.pptx', 'ish-barak.pdf', 'katany-tap.pdf', 'labirint.pdf',
    'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf', 'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf',
)]
