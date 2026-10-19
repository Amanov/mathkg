"""/directed_numbers/ in the «Төрт амал» layout (2026-10-19).

Жалпы keeps the files the old page linked plus the older activities
already filed under Сандар › Багытталган сандар › Эсептөөлөр (Bingo, XO,
Tarsia…), picked up from the database by title so nothing is renamed.
5-класс and 6-класс carry the three new grade packs; their files ship in
apps/resources/bundled_files/ (migration 0032 adds their Resource rows).
"""

import copy

from apps.resources.data.grade_topic_pages import IMAGE_DIR, TEACHER_NOTE, _item, _page

OLD_IMG = 'img/4-amal-BagyttalganSandar'

_general = [
    _item('Тереңдетүү', 0, 'Жеңил, орто, оор', 'Үч деңгээлдеги мисалдар.', 'Колдонуу',
          [('PPT', '4-Amal-BagyttalganSandarMenenJenilOrtoOOR.pptx')], OLD_IMG + 'JenilOrtoOor-Screenshot.png'),
    _item('Кызматташуу', 0, '1234 оюну', 'Командалар менен.', 'Колдонуу',
          [('PPT', '4-Amal-BagyttalganSandarMenen1234.pptx')], OLD_IMG + '1234-Screenshot.png'),
    _item('Кызматташуу', 0, 'Төрт катар', 'Жоопторду катар туташтырышат.', 'Колдонуу',
          [('PPT', '4-Amal-BagyttalganSandarMenenKataryMNTort.pptx')], 'img/4-amal-BagyttalganSandatKatarMNTort-Screenshot.png'),
]

# Older activities linked to Сандар › Багытталган сандар › Эсептөөлөр,
# matched by a word in their file title (case-insensitive). Files whose
# title the page already lists above are skipped.
LEGACY_ACTIVITIES = [
    ('bingo', 'Кызматташуу', 'Бинго', 'Бүт класс менен ойнойт.', 'Колдонуу', OLD_IMG + 'Bingo-Screenshot.png'),
    ('xo', 'Кызматташуу', 'X-O оюну', 'Эки команда, туура жооп үчүн белги коюшат.', 'Колдонуу', OLD_IMG + 'XO-Screenshot.png'),
    ('kaz', 'Кызматташуу', 'Казына издөө', 'Туура жооп кийинки тапшырмага алып барат.', 'Колдонуу',
     OLD_IMG + 'KazinaIzdoo-Screenshot.png'),
    ('tarsia', 'Байланыштыруу', 'Тарсия курак', 'Мисал менен жообун жанаштырышат.', 'Талдоо',
     OLD_IMG + 'TarsiaKurak-Screenshot.png'),
    ('labirint', 'Баалоо', 'Лабиринт', 'Туура жооптор аркылуу гана өтүшөт.', 'Баалоо', None),
    ('katany', 'Баалоо', 'Катаны тап', 'Даяр чыгарылыштан катаны таап, оңдошот.', 'Баалоо', None),
]
# Drawn fallback for activities without a screenshot.
LEGACY_SVG = {'labirint': 'sandar-labyrinth', 'katany': 'katany-tap'}

PACKS = [
    ('5-klass-butun-sandar-koshuu-kemituu-', 5, 'Кошуу жана кемитүү', {
        'sabak': '26 слайд: «Нарындагы кыш» окуясы, жип менен сан огу, термометр, сан огунда басуу.',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу оң, терс же нөл.',
    }),
    ('5-klass-butun-sandar-kobeytuu-boluu-', 5, 'Көбөйтүү жана бөлүү', {
        'sabak': '26 слайд: «Суу сактагычтын күндөлүгү» окуясы, эки түстүү капкактар, белгилер эрежеси.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу оң, терс же нөл.',
    }),
    ('6-klass-bagyttalgan-sandar-amaldardyn-tartibi-', 6, 'Амалдардын тартиби', {
        'sabak': '26 слайд: «Ала-Арчага жөө жүрүш» окуясы, «КаДа – БөКө – КоКе», (−3)² жана −3².',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: туюнтманы жообу боюнча сорттошот.',
    }),
]


def _pack_items(prefix, grade, subtopic, notes):
    def one(section, title, note, level, suffix, label='PDF A4'):
        ext = '.pptx' if label == 'PPT' else '.pdf'
        return _item(section, grade, title, note, level, [(label, prefix + suffix + ext)],
                     IMAGE_DIR + prefix + suffix + '.webp', subtopic=subtopic)

    return [
        one('Изилдөө', 'Цифра табышмагы', 'Үч деңгээл: бош орунга цифра коюшат.', 'Талдоо', 'cifra-tabyshmagy'),
        one('Түшүндүрүү', 'Сабактын презентациясы', notes['sabak'], 'Түшүнүү', 'sabak', 'PPT'),
        one('Тереңдетүү', 'Иш барак: Жеңил, Орто, Оор', notes['ish-barak'], 'Колдонуу', 'ish-barak'),
        one('Баалоо', 'Катаны тап', 'Алты окуучунун чыгарылышы: катаны таап, оңдошот.', 'Баалоо', 'katany-tap'),
        one('Баалоо', 'Туура же ката лабиринт', 'Туура жооптор аркылуу гана өтүшөт.', 'Баалоо', 'labirint'),
        one('Байланыштыруу', 'Домино', '12 карта: мисал менен жообу чынжыр түзөт.', 'Талдоо', 'domino'),
        one('Байланыштыруу', 'Карта сорттоо', notes['karta-sorttoo'], 'Талдоо', 'karta-sorttoo'),
        one('Кызматташуу', '1234 оюну', 'Командалар менен, 9 слайд.', 'Колдонуу', 'oyun-1234', 'PPT'),
        one('Кызматташуу', 'Атышуу', 'Эки команда, 25 слайд, ылдамдыксыз упай.', 'Колдонуу', 'oyun-atyshuu', 'PPT'),
    ]


_items = list(_general)
_teacher = []
for _prefix, _grade, _subtopic, _notes in PACKS:
    _items += _pack_items(_prefix, _grade, _subtopic, _notes)
    _teacher += [
        {'title': f'{_grade}-класс · {_subtopic}: класста колдонуу', 'note': TEACHER_NOTE,
         'files': [('PDF', _prefix + 'klassta-koldonuu.pdf')], 'grade': _grade},
        {'title': f'{_grade}-класс · {_subtopic}: мугалимдин картасы',
         'note': 'Типтүү каталар, чечүүчү суроо, чыгуу билети.',
         'files': [('PDF', _prefix + 'mugalim-kartasy.pdf')], 'grade': _grade},
    ]

DIRECTED_NUMBERS = _page('Багытталган сандар менен амалдар', 'directed_numbers',
                         'Сандар › Амалдардын тартиби', None, _items, teacher=_teacher)

NEW_FILES = [
    prefix + suffix
    for prefix, _, _, _ in PACKS
    for suffix in ('sabak.pptx', 'oyun-1234.pptx', 'oyun-atyshuu.pptx', 'ish-barak.pdf', 'katany-tap.pdf',
                   'labirint.pdf', 'domino.pdf', 'karta-sorttoo.pdf', 'cifra-tabyshmagy.pdf',
                   'klassta-koldonuu.pdf', 'mugalim-kartasy.pdf')
]


def _label(title):
    ext = title.rsplit('.', 1)[-1].upper()
    label = 'PPT' if ext == 'PPTX' else ext
    for size in ('A4', 'A5'):
        if size in title:
            return f'{label} {size}'
    return label


def directed_numbers_spec(titles):
    """The page spec plus Жалпы items for older activities in `titles`
    (Resource titles linked to Сандар › Багытталган сандар › Эсептөөлөр)."""
    spec = copy.deepcopy(DIRECTED_NUMBERS)
    listed = {name for s in spec['sections'] for i in s['items'] for _, name in i['files']}
    remaining = sorted(t for t in titles if t not in listed)
    sections = {s['title']: s for s in spec['sections']}
    for word, section, title, note, level, image in LEGACY_ACTIVITIES:
        files = [t for t in remaining if word in t.lower()]
        if not files:
            continue
        remaining = [t for t in remaining if t not in files]
        stem = LEGACY_SVG.get(word, 'legacy-' + word)
        sections[section]['items'].append({
            'title': title, 'note': note, 'level': level, 'grade': 0, 'subtopic': None,
            'files': [(_label(t), t) for t in files], 'svg': stem,
        })
        if image:
            spec['images'][stem] = image
    return spec
