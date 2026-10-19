"""Grade-level materials for the «Төрт амал» page (1–5-класс).

Each entry is (section title, item). The item has the usual topic-page
keys plus `grade` and `subtopic`; topic_pages.FOUR_BASIC_OPERATIONS adds
them to the first section with that title. The thumbnail is an inside
page of the file (an example slide or the tasks page), rendered to
static/img/four-basic-operations/klass/<file stem>.webp. The files
themselves ship in apps/resources/bundled_files/ and get their Resource
rows from migration 0029.
"""

GRADE_IMAGE_DIR = 'img/four-basic-operations/klass/'

K1A = '10 ичинде кошуу'
K1K = '10 ичинде кемитүү'
K2A = '100 ичинде кошуу жана кемитүү'
K2M = '2, 3, 4кө көбөйтүү жана бөлүү'
K3J = 'Көбөйтүү жадыбалы'
K3M = 'Мамыча түрүндө кошуу жана кемитүү'
K4 = 'Амалдардын тартиби (кашаа менен)'
K5 = 'Амалдардын тартиби (даража менен)'



def it(section, grade, subtopic, title, note, level, files):
    stem = files[0][1].rsplit('.', 1)[0]
    return section, {
        'title': title,
        'note': note,
        'svg': stem,
        'level': level,
        'files': files,
        'grade': grade,
        'subtopic': subtopic,
    }


GRADE_ITEMS = [
    # ---- 1-класс
    it('Түшүндүрүү', 1, K1A, 'Сабактын презентациясы', '48 слайд, 2 сабак: таш, бурчак, жумуртка кутусу (он-кадр), «5 жана дагы».', 'Түшүнүү',
       [('PPT', '1-klass-10-ichinde-koshuu-sabak-v5.pptx')]),
    it('Түшүндүрүү', 1, K1K, 'Сабактын презентациясы', '26 слайд: Тыйын жана Помпон менен айылдагы бакча.', 'Түшүнүү',
       [('PPT', '1-klass-10-ichinde-kemituu-sabak.pptx')]),
    it('Изилдөө', 1, K1A, 'Цифралык табышмак', 'Бош кутучага цифра коюп, мисалды толукташат.', 'Талдоо',
       [('PDF A4', '1-klass-koshuu-cifra-tabyshmagy-v4.pdf')]),
    it('Изилдөө', 1, K1K, 'Цифралык табышмак', 'Кемитүүдө жетишпеген цифраны издешет.', 'Талдоо',
       [('PDF A4', '1-klass-10-ichinde-kemituu-cifra-tabyshmagy.pdf')]),
    it('Тереңдетүү', 1, K1A, 'Иш барак: Жеңил, Орто, Оор', 'Үч деңгээл бир бетте, жооп ачкычы менен.', 'Колдонуу',
       [('PDF A4', '1-klass-10-ichinde-koshuu-ish-barak-v4.pdf')]),
    it('Тереңдетүү', 1, K1K, 'Иш барак: Жеңил, Орто, Оор', 'Үч деңгээл, тилке модели менен.', 'Колдонуу',
       [('PDF A4', '1-klass-10-ichinde-kemituu-ish-barak.pdf')]),
    it('Баалоо', 1, K1A, 'Катаны тап', 'Чечилген мисалдагы катаны таап, оңдошот.', 'Баалоо',
       [('PDF A4', '1-klass-koshuu-katany-tap-v4.pdf')]),
    it('Баалоо', 1, K1A, 'Туура же ката лабиринт', 'Туура мисалдар аркылуу гана өтүшөт.', 'Баалоо',
       [('PDF A4', '1-klass-koshuu-labirint-v4.pdf')]),
    it('Баалоо', 1, K1K, 'Туура же ката лабиринт', 'Кемитүү мисалдары менен лабиринт.', 'Баалоо',
       [('PDF A4', '1-klass-10-ichinde-kemituu-labirint.pdf')]),
    it('Байланыштыруу', 1, K1A, 'Тарсия', 'Мисалды жообу менен жанаштырып, фигура түзүшөт.', 'Талдоо',
       [('PDF A4', '1-klass-koshuu-tarsia-v4.pdf')]),
    it('Байланыштыруу', 1, K1A, 'Карта сорттоо', 'Карталарды туура/ката боюнча топторго бөлүшөт.', 'Талдоо',
       [('PDF A4', '1-klass-koshuu-karta-sorttoo-v4.pdf')]),
    it('Байланыштыруу', 1, K1K, 'Домино', 'Мисалды жообу менен улап, чынжыр түзүшөт.', 'Талдоо',
       [('PDF A4', '1-klass-10-ichinde-kemituu-domino.pdf')]),
    it('Кызматташуу', 1, K1A, 'Бинго', 'Бүт класс менен: мугалим мисал айтат.', 'Колдонуу',
       [('PPT', '1-klass-koshuu-bingo-v4.pptx')]),
    it('Кызматташуу', 1, K1A, 'Айып сокку', 'Туура жооп + түшүндүрүү = упай.', 'Колдонуу',
       [('PPT', '1-klass-koshuu-penalti-v5.pptx')]),
    it('Кызматташуу', 1, K1A, '1234 оюну', 'Төрт бурчтагы төрт суроо, топтор менен.', 'Колдонуу',
       [('PPT', '1-klass-koshuu-1234-v4.pptx')]),
    it('Кызматташуу', 1, K1K, 'Атышуу', 'Экиден чыгып жооп беришет, ылдамдыксыз.', 'Колдонуу',
       [('PPT', '1-klass-10-ichinde-kemituu-oyun-atyshuu.pptx')]),
    # ---- 2-класс
    it('Түшүндүрүү', 2, K2A, 'Сабактын презентациясы', '26 слайд: санак таякчалар, 10/1 сомдук тыйындар, оозеки ыкма.', 'Түшүнүү',
       [('PPT', '2-klass-100-ichinde-sabak-v2.pptx')]),
    it('Түшүндүрүү', 2, K2M, 'Сабактын презентациясы', '26 слайд: мектеп китепканасы, кагаз табак жана бурчак.', 'Түшүнүү',
       [('PPT', '2-klass-kobeytuu-2-3-4-sabak.pptx')]),
    it('Изилдөө', 2, K2A, 'Цифралык табышмак', 'Жетишпеген цифраларды табышат.', 'Талдоо',
       [('PDF A4', '2-klass-100-ichinde-cifra-tabyshmagy-v2.pdf')]),
    it('Тереңдетүү', 2, K2A, 'Иш барак: Жеңил, Орто, Оор', '4 бет, жооп ачкычы менен.', 'Колдонуу',
       [('PDF A4', '2-klass-100-ichinde-ish-barak-v2.pdf')]),
    it('Тереңдетүү', 2, K2M, 'Иш барак: Жеңил, Орто, Оор', 'Топтор жана тилке модели.', 'Колдонуу',
       [('PDF A4', '2-klass-kobeytuu-2-3-4-ish-barak.pdf')]),
    it('Баалоо', 2, K2A, 'Катаны тап', 'Каталарды таап, оңдошот.', 'Баалоо',
       [('PDF A4', '2-klass-100-ichinde-katany-tap-v2.pdf')]),
    it('Баалоо', 2, K2M, 'Туура же ката лабиринт', 'Туура мисалдар аркылуу өтүшөт.', 'Баалоо',
       [('PDF A4', '2-klass-kobeytuu-2-3-4-labirint.pdf')]),
    it('Байланыштыруу', 2, K2A, 'Домино', 'Мисал менен жоопту улап чыгышат.', 'Талдоо',
       [('PDF A4', '2-klass-100-ichinde-domino-v2.pdf')]),
    it('Байланыштыруу', 2, K2M, 'Карта сорттоо', 'Карталарды топторго бөлүшөт.', 'Талдоо',
       [('PDF A4', '2-klass-kobeytuu-2-3-4-karta-sorttoo.pdf')]),
    it('Кызматташуу', 2, K2A, '1234 оюну', 'Топтор менен төрт суроо.', 'Колдонуу',
       [('PPT', '2-klass-100-ichinde-oyun-1234-v2.pptx')]),
    it('Кызматташуу', 2, K2M, 'Атышуу', 'Экиден чыгып жооп беришет.', 'Колдонуу',
       [('PPT', '2-klass-kobeytuu-2-3-4-oyun-atyshuu.pptx')]),
    # ---- 3-класс
    it('Түшүндүрүү', 3, K3J, 'Сабактын презентациясы', '26 слайд: 4 × 8 = 4 топ, 8ден; массив чакмак дептерде.', 'Түшүнүү',
       [('PPT', '3-klass-jadybal-sabak-v2.pptx')]),
    it('Түшүндүрүү', 3, K3M, 'Сабактын презентациясы', '26 слайд: базардагы дүкөн, 100/10/1 сомдук кагаз акча.', 'Түшүнүү',
       [('PPT', '3-klass-mamycha-koshuu-kemituu-sabak.pptx')]),
    it('Изилдөө', 3, K3J, 'Цифралык табышмак', 'Жадыбалдагы жетишпеген цифралар.', 'Талдоо',
       [('PDF A4', '3-klass-jadybal-cifra-tabyshmagy-v2.pdf')]),
    it('Тереңдетүү', 3, K3J, 'Иш барак: Жеңил, Орто, Оор', '4 бет, жооп ачкычы менен.', 'Колдонуу',
       [('PDF A4', '3-klass-jadybal-ish-barak-v2.pdf')]),
    it('Тереңдетүү', 3, K3M, 'Иш барак: Жеңил, Орто, Оор', 'Мамыча түрүндө эсептөө.', 'Колдонуу',
       [('PDF A4', '3-klass-mamycha-koshuu-kemituu-ish-barak.pdf')]),
    it('Баалоо', 3, K3J, 'Туура же ката лабиринт', 'Туура мисалдар аркылуу өтүшөт.', 'Баалоо',
       [('PDF A4', '3-klass-jadybal-labirint-v2.pdf')]),
    it('Баалоо', 3, K3M, 'Катаны тап', 'Мамычадагы каталарды табышат.', 'Баалоо',
       [('PDF A4', '3-klass-mamycha-koshuu-kemituu-katany-tap.pdf')]),
    it('Байланыштыруу', 3, K3J, 'Домино', 'Мисал менен жоопту улап чыгышат.', 'Талдоо',
       [('PDF A4', '3-klass-jadybal-domino-v2.pdf')]),
    it('Байланыштыруу', 3, K3M, 'Карта сорттоо', 'Карталарды топторго бөлүшөт.', 'Талдоо',
       [('PDF A4', '3-klass-mamycha-koshuu-kemituu-karta-sorttoo.pdf')]),
    it('Кызматташуу', 3, K3J, '1234 оюну', 'Топтор менен төрт суроо.', 'Колдонуу',
       [('PPT', '3-klass-jadybal-oyun-1234-v2.pptx')]),
    it('Кызматташуу', 3, K3M, 'Атышуу', 'Экиден чыгып жооп беришет.', 'Колдонуу',
       [('PPT', '3-klass-mamycha-koshuu-kemituu-oyun-atyshuu.pptx')]),
    # ---- 4-класс
    it('Түшүндүрүү', 4, K4, 'Сабактын презентациясы', '39 слайд, 2 сабак: бөтөлкө капкактары, «Адегенде болжолдо», кашаа.', 'Түшүнүү',
       [('PPT', '4-klass-amaldardyn-tartibi-sabak-v6.pptx')]),
    it('Тереңдетүү', 4, K4, 'Иш барак: Жеңил, Орто, Оор', 'Үч деңгээл жана тилке модели, жооп ачкычы менен.', 'Колдонуу',
       [('PDF A4', '4-klass-ish-baragy-v3.pdf')]),
    it('Баалоо', 4, K4, 'Чечүүчү суроолор', 'Сабактын ортосунда: ар бир туура эмес жооп бир катаны көрсөтөт.', 'Баалоо',
       [('PDF', '1-chechuuchu-suroolor.pdf')]),
    # ---- 5-класс
    it('Түшүндүрүү', 5, K5, 'Сабактын презентациясы', '34 слайд: 1–10дун квадраттары, «Адегенде болжолдо».', 'Түшүнүү',
       [('PPT', '5-klass-amaldardyn-tartibi-sabak-v6.pptx')]),
    it('Тереңдетүү', 5, K5, 'Иш барак: Жеңил, Орто, Оор', 'Үч деңгээл жана тилке модели, жооп ачкычы менен.', 'Колдонуу',
       [('PDF A4', '5-klass-ish-baragy-v3.pdf')]),
    it('Баалоо', 5, K5, 'Тестке даярдык', 'Блок тести жана «Ойлонуп көр» рефлексиясы.', 'Баалоо',
       [('PDF A4', '5-klass-testke-dayardyk-v3.pdf')]),
    it('Баалоо', 5, K5, 'Чыгуу билеттери', 'Сабактын аягында 3 суроо, A6 карточка.', 'Баалоо',
       [('PDF A6', '3b-chyguu-biletteri-A6.pdf')]),
    it('Байланыштыруу', 5, K5, 'Ката карталары', 'Ар бир ката коду үчүн карта жана суроо.', 'Талдоо',
       [('PDF', '2-kata-kartalary.pdf')]),
    it('Кызматташуу', 5, K5, 'Оюндар жана ишмердиктер', '19 слайд: туура жана түшүндүрдү = 2 упай.', 'Колдонуу',
       [('PPT', '5-klass-oyundar-aktivduuluktor-v5.pptx')]),
]

# (grade, subtopic, file) for the teacher guide panel.
GRADE_TEACHER_FILES = [
    (1, K1A, '1-klass-10-ichinde-koshuu-klassta-koldonuu.pdf'),
    (4, K4, '4-klass-amaldardyn-tartibi-klassta-koldonuu-1-sabak.pdf'),
    (5, K5, '5-klass-amaldardyn-tartibi-klassta-koldonuu-1-sabak.pdf'),
]


