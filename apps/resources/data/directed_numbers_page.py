"""/directed_numbers/ in the «Төрт амал» layout (2026-10-19).

5-класс and 6-класс carry the three grade packs; their files ship in
apps/resources/bundled_files/ (migration 0032 adds their Resource rows).
The page's older files were built on goteachmaths templates and were taken
off the site on 2026-10-24 (migration 0033).
"""

from apps.resources.data.grade_topic_pages import IMAGE_DIR, TEACHER_NOTE, _item, _page

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


_items = []
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

