"""One-page lesson set for mean, median, mode and range.

File names are the names in the statistics pack. They are not renamed.
"""

IMAGE = 'img/statistics-set/'

# (section, title, note, image, files)
# files: (label, filename)
CARDS = (
    ('Презентациялар', 'Сабак: «Кайсы команда жакшыраак?»',
     '27 слайд, 45 мүнөт. Кадам-кадам анимация, жооп аягында ачылат.',
     'thumb-deck-01.png',
     [('PPTX', 'statistika-sabak-mathkg.pptx')]),
    ('Тактадагы суроолор', 'Ооба… Жок… Балким…',
     'Жети ырастоо. Окуучу тактачасын көтөрөт.',
     'thumb-stat-OobaJokBalkim-1.png',
     [('PPTX', 'stat-OobaJokBalkim.pptx'), ('PDF', 'stat-OobaJokBalkim.pdf')]),
    ('Тактадагы суроолор', 'Көрсөт…',
     'Алты ачык суроо.',
     'thumb-stat-Korsot-1.png',
     [('PPTX', 'stat-Korsot.pptx'), ('PDF', 'stat-Korsot.pdf')]),
    ('Иш барактары', 'Кадам-кадам',
     'Жеңилден оорго. Жооптору өзүнчө.',
     'thumb-stat-KadamKadam-Jooptor-1.png',
     [('PDF', 'stat-KadamKadam-A4.pdf'), ('DOCX', 'stat-KadamKadam-A4.docx'),
      ('Жооптор', 'stat-KadamKadam-Jooptor-A4.pdf'),
      ('Жооптор DOCX', 'stat-KadamKadam-Jooptor-A4.docx')]),
    ('Иш барактары', 'Кодду ач',
     'Оюн түрүндөгү иш барак.',
     'thumb-stat-KoddoAch-Jooptor-1.png',
     [('PDF', 'stat-KoddoAch-A4.pdf'), ('DOCX', 'stat-KoddoAch-A4.docx'),
      ('Жооптор', 'stat-KoddoAch-Jooptor-A4.pdf'),
      ('Жооптор DOCX', 'stat-KoddoAch-Jooptor-A4.docx')]),
    ('Иш барактары', 'Бекемдөө',
     'Аралаш тапшырмалар.',
     'thumb-stat-Bekemdoo-Jooptor-1.png',
     [('PDF', 'stat-Bekemdoo-A4.pdf'), ('DOCX', 'stat-Bekemdoo-A4.docx'),
      ('Жооптор', 'stat-Bekemdoo-Jooptor-A4.pdf'),
      ('Жооптор DOCX', 'stat-Bekemdoo-Jooptor-A4.docx')]),
    ('Иш барактары', 'Туура же туура эмес лабиринт',
     'Туура жооптор аркылуу гана өтүшөт.',
     'thumb-stat-Labirint-A4-1.png',
     [('PDF', 'stat-Labirint-A4.pdf'), ('2 нуска A4', 'stat-Labirint-2bet-A4.pdf'),
      ('Жооптор', 'stat-Labirint-Jooptor-A4.pdf'), ('PPTX', 'stat-Labirint.pptx')]),
    ('Иш-аракеттер', 'Кенч издөө',
     '16 плакат.',
     'thumb-kench-poster-05.png',
     [('PPTX', 'stat-KenchIzdoo.pptx'), ('PDF', 'stat-KenchIzdoo.pdf')]),
    ('Иш-аракеттер', 'Карточкаларды ирге',
     'Төрт өлчөм: орточо, медиана, мода, кулач.',
     'thumb-stat-Kartochka-A4-1.png',
     [('PDF', 'stat-Kartochka-A4.pdf'), ('DOCX', 'stat-Kartochka-A4.docx'),
      ('Жооптор', 'stat-Kartochka-Jooptor-A4.pdf'),
      ('Жооптор DOCX', 'stat-Kartochka-Jooptor-A4.docx')]),
    ('Мугалим жетектеген', 'Блокбастер',
     'Команда оюну. Шилтемелер PPTX ичинде иштейт.',
     'thumb-stat-Blokbaster-01.png',
     [('PPTX', 'stat-Blokbaster.pptx'), ('PDF', 'stat-Blokbaster.pdf')]),
    ('Мугалим', 'Топтомду кантип колдонобуз',
     'Мугалим үчүн кыска жол.',
     'thumb-stat-MugalimUchun-A4-1.png',
     [('PDF', 'stat-MugalimUchun-A4.pdf'), ('DOCX', 'stat-MugalimUchun-A4.docx')]),
    ('Мугалим', 'Сабакты изилдөө топтому',
     'Сабакты чогуу талдоо үчүн.',
     'thumb-stat-SabaktyIzildoo-A4-1.png',
     [('PDF', 'stat-SabaktyIzildoo-A4.pdf'), ('DOCX', 'stat-SabaktyIzildoo-A4.docx')]),
    ('Мугалим', 'Жоопторду текшерүү',
     'Жооптордун тизмеси.',
     'thumb-stat-Labirint-Jooptor-A4-1.png',
     [('TXT', 'answer-verification.txt')]),
)

SECTION_ORDER = (
    'Презентациялар',
    'Тактадагы суроолор',
    'Иш барактары',
    'Иш-аракеттер',
    'Мугалим жетектеген',
    'Экзамен суроолору',
    'Мугалим',
)

NAMES = []
for _section, _title, _note, _image, files in CARDS:
    for _label, name in files:
        if name not in NAMES:
            NAMES.append(name)
