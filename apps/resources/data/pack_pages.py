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
    'kolom': {
        'prefix': '5-klass-kolom-', 'grade': 5, 'subtopic': 'Көлөм жана бет аянты',
        'sabak': '26 слайд: «Өзгөндөгү күрүч кутулары» окуясы, кант кесектеринен кутуча, сүт кутусунун жайылмасы, литр.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: көлөм, бет аянты жана бирдиктер.',
    },
    'ylldamdyk': {
        'prefix': '5-klass-ylldamdyk-', 'grade': 5, 'subtopic': 'Ылдамдык, убакыт жана аралык',
        'sabak': '26 слайд: «Балыкчыга жайкы поезд» окуясы, короодо басып өз ылдамдыгыңды ченөө, эки шкалалуу жол сызыгы.',
        'ish-barak': '18 тапшырма жана тилке модели: эки этаптуу жол, жакындашуу жана кууп жетүү, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: ылдамдык, убакыт же аралыкты табуу.',
    },
    'koordinattar': {
        'prefix': '6-klass-koordinattar-', 'grade': 6, 'subtopic': 'Координаталык тегиздик',
        'sabak': '26 слайд: «Чолпон-Атадагы таш сүрөттөр» окуясы, жип менен тор, чекиттерди окуу жана белгилөө, төрт чейрек.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: чекиттер чейреги жана огу боюнча.',
    },
    'masshtab': {
        'prefix': '6-klass-masshtab-', 'grade': 6, 'subtopic': 'Масштаб',
        'sabak': '26 слайд: «Сары-Челекке саякат» окуясы, 1 : 100 класстын планы, шарттуу карта жана эки сан огу.',
        'ish-barak': '18 тапшырма, сызгыч менен ченелүүчү карта жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: масштаб, картадагы жана чыныгы аралык.',
    },
    'okshosh': {
        'prefix': '6-klass-okshosh-muchular-', 'grade': 6, 'subtopic': 'Окшош мүчөлөр жана туюнтмаларды жөнөкөйлөтүү',
        'sabak': '26 слайд: «Чаткалдагы бал» окуясы, картон алгебра плиткалары, 3(x + 4) = 3x + 12.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: бирдей туюнтмаларды табуу.',
    },
    'aylana': {
        'prefix': '6-klass-aylana-tegerek-', 'grade': 6, 'subtopic': 'Айлана жана тегерек',
        'sabak': '26 слайд: «Кара-Балтадагы тегерек гүлзар» окуясы, жип менен айлананы ченөө, тегеректи 8 секторго кесүү.',
        'ish-barak': '18 тапшырма жана тилке модели, π ≈ 3,14, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: айлананын узундугу же тегеректин аянты.',
    },
    'turmushtuk': {
        'prefix': '6-klass-turmushtuk-eseptoo-', 'grade': 6, 'subtopic': 'Турмуштук эсептөөлөр: баа, рецепт, валюта',
        'sabak': '26 слайд: «Аламүдүн базарында базарлык» окуясы, палоо рецептин 10 кишиге эсептөө, пайдалуу сатып алуу, мисал курс менен валюта.',
        'ish-barak': '18 тапшырма жана 6 тилке модели «1 бирдикке», жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: көбөйтүү, бөлүү же «адегенде 1 бирдик».',
    },
    'uch_burchtuk': {
        'prefix': '5-klass-uch-burchtuk-ayanty-', 'grade': 5, 'subtopic': 'Үч бурчтуктун, параллелограммдын жана трапециянын аянты',
        'sabak': '26 слайд: «Кара-Балтадагы мектеп гүлзары» окуясы, чакмак кагазды кесип жылдыруу, a × h ÷ 2 жана (a + b) × h ÷ 2.',
        'ish-barak': '18 тапшырма, чакмак кагаздагы фигуралар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 фигура чакмак кагазда: аянты боюнча топтошот.',
    },
    'payyz': {
        'prefix': '6-klass-payyz-', 'grade': 6, 'subtopic': 'Пайыз: чоңдуктун пайызы, арзандатуу жана кымбаттоо',
        'sabak': '26 слайд: «Ноокаттагы китеп жарманкеси» окуясы, 10 × 10 тордо буурчак, 10% жана 1% аркылуу каалаган пайыз, пайыздык тилке.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: арзандатуу, кымбаттоо жана пайыз менен туюнтуу.',
    },
    'birdikter': {
        'prefix': '4-klass-birdikterdi-almashtyruu-', 'grade': 4, 'subtopic': 'Узундук, масса жана сыйымдуулук бирдиктерин алмаштыруу',
        'sabak': '26 слайд: «Кайыңдыдагы кант кызылчасы» окуясы, жумуртка кутусу жана капкактар (ц, т), кагаз метр, 1 литрлик бөтөлкө.',
        'ish-barak': '18 тапшырма жана тилке модели: мм–км, г–т, мл–л, аралаш бирдиктерди кошуу, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: бирдей чоңдуктарды табуу.',
    },
    'maalymat3': {
        'prefix': '3-klass-maalymat-chogultuu-', 'grade': 3, 'subtopic': 'Маалымат чогултуу: суроо, чийме белгилер жана жыштык таблицасы',
        'sabak': '26 слайд: «Ат-Башыдагы оюндар күнү» окуясы, капкактарды бештен топтоо, чийме белгилер, ● = 2 пиктограмма.',
        'ish-barak': '18 тапшырма, жыштык таблицасы жана пиктограмма, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: чийме белгилер, сан жана пиктограмманы дал келтирүү.',
    },
    'venn': {
        'prefix': '5-klass-venn-diagrammalary-', 'grade': 5, 'subtopic': 'Көптүктөр жана Венн диаграммалары',
        'sabak': '26 слайд: «Ат-Башыдагы мектеп ийримдери» окуясы, жип менен эки тегерек, Венн жана Кэрролл диаграммалары.',
        'ish-barak': '18 тапшырма, Венн жана Кэрролл диаграммалары, тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 сан Венн диаграммасына: «жуп» жана «3кө бөлүнөт».',
    },
    'tegerektoo': {
        'prefix': '4-klass-tegerektoo-boljoldoo-', 'grade': 4, 'subtopic': 'Тегеректөө жана болжолдоо',
        'sabak': '26 слайд: «Жети-Өгүздөгү алма бакчасы» окуясы, кагаз тилкедеги сан огу, жарым жол эрежеси, жоопту болжолдоп текшерүү.',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: болжолдуу жооп ≈ 600, 6 000 же 60 000.',
    },
    'kop_kb': {
        'prefix': '4-klass-kop-orunduu-kobeytuu-boluu-', 'grade': 4, 'subtopic': 'Көп орундуу сандарды көбөйтүү жана бөлүү',
        'sabak': '26 слайд: «Суусамырдагы кымыз майрамы» окуясы, чакмак кагаз тилкелери, тор ыкмасы, мамычада көбөйтүү, калдык менен бөлүү.',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: көбөйтүүнү жана бөлүүнү жообу боюнча топтоо.',
    },
    'm1000': {
        'prefix': '5-klass-10-100-1000-', 'grade': 5, 'subtopic': '10, 100, 1000ге көбөйтүү жана бөлүү',
        'sabak': '26 слайд: «Кеминдеги тигүү цехи» окуясы, кагаз разряд таблицасы, цифралар жылат, үтүр ордунда калат, бирдиктерди алмаштыруу.',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: 0,5 м, 5 м же 50 мге барабар.',
    },
    'tuz_teskeri': {
        'prefix': '6-klass-tuz-teskeri-proporciya-', 'grade': 6, 'subtopic': 'Түз жана тескери пропорциялуулук',
        'sabak': '26 слайд: «Тоңдогу ашар» окуясы, 24 капкакты кайра топтоо, катыш таблицалары, жумушчулар жана күндөр.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: түз, тескери же экөө тең эмес.',
    },
    'bolchok_kk': {
        'prefix': '5-klass-bolchok-koshuu-kemituu-', 'grade': 5, 'subtopic': 'Бөлчөктөрдү кошуу жана кемитүү',
        'sabak': '26 слайд: «Кара-Кулжада тосмо боёо» окуясы, бүктөлгөн кагаз тилкелер, жумуртка кутусу, бөлчөк дубалы, 1/3 + 1/4 = 7/12.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: суммасы же айырмасы боюнча топтоо.',
    },
    'tegerek_diagramma': {
        'prefix': '6-klass-tegerek-diagramma-', 'grade': 6, 'subtopic': 'Тегерек диаграммалар',
        'sabak': '26 слайд: «Таш-Көмүрдөгү ашкана» окуясы, 36 чарчылуу кагаз тилкеден тегерек, бурчту окуучуга айлантуу, эки класстын диаграммасын салыштыруу.',
        'ish-barak': '18 тапшырма жана 6 тегерек диаграмма, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: бурч, пайыз жана окуучулардын саны боюнча топтоо.',
    },
    'geometriya3': {
        'prefix': '3-klass-geometriyalyk-terminder-', 'grade': 3, 'subtopic': 'Бурчтар, төрт бурчтуктар жана тегерек',
        'sabak': '26 слайд: «Кызыл-Кыяда ордо аянтчасы» окуясы, бүктөлгөн кагаз менен бурчту текшерүү, жип менен тегерек чийүү, радиус жана диаметр.',
        'ish-barak': '3 бет тапшырма жана чакмак кагазда чийүү, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: төрт бурчтуктарды бурчтары жана жактары боюнча топтоо.',
    },
    'maani_eseptoo': {
        'prefix': '6-klass-maanisin-eseptoo-', 'grade': 6, 'subtopic': 'Туюнтманын маанисин эсептөө',
        'sabak': '26 слайд: «Кербендеги аба ырайы бурчу» окуясы, терс сандарды кашаага коюу, x² жана −x², формула F = 9C ÷ 5 + 32.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: туюнтмаларды маанисине жараша топтоо.',
    },
    'eki_tarap': {
        'prefix': '6-klass-tendemeler-eki-tarap-', 'grade': 6, 'subtopic': 'Теңдемелер: функция машинасы жана белгисиз эки тарапта',
        'sabak': '26 слайд: «Тамгадагы чычырканак» окуясы, функция машинасы алдыга жана артка, чөйчөк жана капкак таразасы, 5x + 3 = 2x + 15.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: теңдемелерди тамырына жараша топтоо.',
    },
    'tamga_kb': {
        'prefix': '6-klass-tamgaluu-kobeytuu-boluu-', 'grade': 6, 'subtopic': 'Тамгалуу мүчөлөрдү көбөйтүү жана бөлүү',
        'sabak': '26 слайд: «Канттагы плитка цехи» окуясы, чакмак кагаздан плиткалар, 2a × 3b = 6ab, 12ab ÷ 4a = 3b, аянт модели.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: = 12ab, = 12a² же = 12a боюнча топтоо.',
    },
    'katysh_1n': {
        'prefix': '6-klass-katysh-1-n-', 'grade': 6, 'subtopic': 'Катыш: 1 : n түрү, бириктирүү жана өзгөрүү',
        'sabak': '26 слайд: «Аравандагы тандыр нан» окуясы, үч түстүү капкактар, 2 : 3 жана 4 : 5 катыштарын бириктирүү (8 : 12 : 15), 1 : n түрү.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: катыштарды 1 : n түрүнө жараша топтоо.',
    },
    'anketa': {
        'prefix': '6-klass-anketa-eki-tarap-tablica-', 'grade': 6, 'subtopic': 'Анкета, эки тараптуу таблица жана орточо маани',
        'sabak': '26 слайд: «Жумгалдагы мектеп гезити» окуясы, жумуртка кутусунан эки тараптуу таблица, чөйчөктөрдү теңдөө, жыштык таблицасынан орточо маани.',
        'ish-barak': '18 тапшырма, таблица жана диаграммалар, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: орточо маани өсөт, азаят же өзгөрбөйт.',
    },
    # Packs made earlier (2026-10-18/19) for the book topics; the first three
    # keep their «-v2» file names.
    'k100': {
        'prefix': '2-klass-100-ichinde-', 'tail': '-v2', 'grade': 2, 'subtopic': '100 ичинде кошуу жана кемитүү',
        'sabak': 'Ондуктар жана бирдиктер, сан огунда секирүү, тилке модели.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: мисалдарды жообу боюнча топтошот.',
    },
    'jadybal': {
        'prefix': '3-klass-jadybal-', 'tail': '-v2', 'grade': 3, 'subtopic': 'Көбөйтүү жадыбалы',
        'sabak': 'Топтор, массивдер жана тилке модели менен көбөйтүү жадыбалы.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: көбөйтүү жана бөлүү мисалдарын жообу боюнча топтошот.',
    },
    'bolunuu': {
        'prefix': '6-klass-bolunuu-belgileri-', 'tail': '-v2', 'grade': 6, 'subtopic': 'Бөлүнүү белгилери',
        'sabak': '2, 3, 5, 9 жана 10го бөлүнүү белгилери, бөлүүчүлөр жана эселиктер.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: сандарды бөлүнүү белгиси боюнча топтошот.',
    },
    'kemituu10': {
        'prefix': '1-klass-10-ichinde-kemituu-', 'grade': 1, 'subtopic': '10 ичинде кемитүү',
        'sabak': 'Таштар, капкактар жана он уячалуу кутуча менен кемитүү.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: кемитүү мисалдарын жообу боюнча топтошот.',
    },
    'kob234': {
        'prefix': '2-klass-kobeytuu-2-3-4-', 'grade': 2, 'subtopic': '2, 3, 4кө көбөйтүү жана бөлүү',
        'sabak': 'Бирдей топтор, массивдер жана тилке модели.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: мисалдарды жообу боюнча топтошот.',
    },
    'mamycha': {
        'prefix': '3-klass-mamycha-koshuu-kemituu-', 'grade': 3, 'subtopic': 'Мамыча менен кошуу жана кемитүү',
        'sabak': 'Орун маанилер таблицасы, алмаштыруу, мамыча менен эсептөө.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: мисалдарды жообу боюнча топтошот.',
    },
    'sandyn_bolugu': {
        'prefix': '3-klass-sandyn-bolugu-', 'grade': 3, 'subtopic': 'Сандын бөлүгү',
        'sabak': 'Тилке модели менен сандын бөлүгүн табуу.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: бөлчөктү жана сандын бөлүгүн дал келтиришет.',
    },
    'million': {
        'prefix': '4-klass-million-ichinde-', 'grade': 4, 'subtopic': 'Миллион ичиндеги сандар',
        'sabak': 'Разряддар, окуу жана жазуу, салыштыруу, тегеректөө.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: сандарды разряддары боюнча топтошот.',
    },
    'kadimki': {
        'prefix': '5-klass-kadimki-bolchoktor-', 'grade': 5, 'subtopic': 'Кадимки бөлчөктөр',
        'sabak': 'Барабар бөлчөктөр, кыскартуу, салыштыруу, тилке модели.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: барабар бөлчөктөрдү топтошот.',
    },
    'proporciya': {
        'prefix': '6-klass-proporciya-procent-', 'grade': 6, 'subtopic': 'Пропорция жана процент',
        'sabak': 'Түз пропорция, 10 % ыкмасы, сандын процентин табуу.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: процент жана чоңдукту дал келтиришет.',
    },
    'jonokoy': {
        'prefix': '6-klass-jonokoy-kobeytuuchuler-', 'grade': 6, 'subtopic': 'Жөнөкөй көбөйтүүчүлөр, ЭЧОБ жана ЭКОЭ',
        'sabak': 'Көбөйтүүчүлөр дарагы, ЭЧОБ жана ЭКОЭ.',
        'ish-barak': 'Жеңил, Орто, Оор тапшырмалар, жооп ачкычы менен.',
        'karta-sorttoo': 'Карталар: жөнөкөй жана курама сандар.',
    },
    'butun_kk': {
        'prefix': '5-klass-butun-sandar-koshuu-kemituu-', 'grade': 5, 'subtopic': 'Бүтүн сандарды кошуу жана кемитүү',
        'sabak': '26 слайд: «Нарындагы кыш» окуясы, жип менен сан огу, термометр.',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу оң, терс же нөл.',
    },
    'butun_kb': {
        'prefix': '5-klass-butun-sandar-kobeytuu-boluu-', 'grade': 5, 'subtopic': 'Бүтүн сандарды көбөйтүү жана бөлүү',
        'sabak': '26 слайд: «Суу сактагычтын күндөлүгү» окуясы, эки түстүү капкактар, белгилер эрежеси.',
        'ish-barak': '18 тапшырма жана 6 тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: жообу оң, терс же нөл.',
    },
    'bagyttalgan': {
        'prefix': '6-klass-bagyttalgan-sandar-amaldardyn-tartibi-', 'grade': 6, 'subtopic': 'Амалдардын тартиби',
        'sabak': '26 слайд: «Ала-Арчага жөө жүрүш» окуясы, «КаДа – БөКө – КоКе», (−3)² жана −3².',
        'ish-barak': '18 тапшырма жана тилке модели, жооп ачкычы менен.',
        'karta-sorttoo': '12 карта: туюнтманы жообу боюнча сорттошот.',
    },
}


def _pack_items(pack):
    prefix, grade, subtopic = pack['prefix'], pack['grade'], pack['subtopic']

    def one(section, title, note, level, suffix, label='PDF A4'):
        ext = '.pptx' if label == 'PPT' else '.pdf'
        name = prefix + suffix + pack.get('tail', '')
        return _item(section, grade, title, note, level, [(label, name + ext)],
                     IMAGE_DIR + name + '.webp', subtopic=subtopic)

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
         'files': [('PDF', prefix + 'klassta-koldonuu' + pack.get('tail', '') + '.pdf')], 'grade': grade},
        {'title': f'{grade}-класс · {subtopic}: мугалимдин картасы',
         'note': 'Типтүү каталар, чечүүчү суроо, чыгуу билети.',
         'files': [('PDF', prefix + 'mugalim-kartasy' + pack.get('tail', '') + '.pdf')], 'grade': grade},
    ]


def _group(key, title, crumb, pack_keys, slugs, badge=None):
    packs = [PACKS[k] for k in pack_keys]
    grades = sorted({p['grade'] for p in packs})
    # ``badge`` is only the label on the page. The pack's own grade still
    # names the files and the grade tabs.
    if badge is None:
        badge = f'{grades[0]}-класс' if len(grades) == 1 else None
    items = [i for p in packs for i in _pack_items(p)]
    teacher = [t for p in packs for t in _teacher(p)]
    return {'spec': _page(title, 'pack_' + key, crumb, badge, items, teacher=teacher), 'slugs': slugs,
            'packs': list(pack_keys)}


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
    ], badge='2–3 кл.'),
    _group('birdikter', 'Узундук, масса жана сыйымдуулук бирдиктерин алмаштыруу', 'Өлчөмдөр', ['birdikter'], [
        'systems-of-measurement-conversion-factors',
        'systems-of-measurement-mixed',
    ], badge='3–5 кл.'),
    _group('simmetriya', 'Симметрия жана фигураларды жылдыруу', 'Геометрия › Өзгөртүүлөр', ['simmetriya'], [
        'geometry-classifying-vocabulary-classifying-shapes-symmetry',
    ]),
    _group('ondu_orun', 'Ондук бөлчөктөр: орун маанилери, салыштыруу, тегеректөө', 'Сандар › Ондуктар', ['ondu_orun'], [
        'rounding-decimal-places',
    ], badge='4–5 кл.'),
    _group('perimetr', 'Периметр жана аянт', 'Геометрия › Периметр жана аянт', ['perimetr'], [
        'geometry-area-perimeter-quadrilaterals-rectangle-area',
        'geometry-area-perimeter-quadrilaterals-rectangle-perimeter',
        'geometry-area-perimeter-quadrilaterals-rectangle-area-perimeter',
        'geometry-area-perimeter-compound-rectilinear-area',
        'geometry-area-perimeter-compound-rectilinear-perimeter',
        'geometry-area-perimeter-compound-rectilinear-mixed',
    ], badge='3–4 кл.'),
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
    ], badge='5–6 кл.'),
    _group('bolchok_kb', 'Бөлчөктөрдү көбөйтүү жана бөлүү, аралаш сандар', 'Сандар › Бөлчөктөр › Эсептөөлөр',
           ['bolchok_kb'], [
        'unit-fractions-multiplying', 'unit-fractions-dividing', 'unit-fractions-multiplying-dividing',
        'unit-fractions-with-integers',
        'non-unit-fractions-multiplying', 'non-unit-fractions-dividing', 'non-unit-fractions-multiplying-dividing',
        'non-unit-fractions-with-cancelling', 'non-unit-fractions-with-integers',
    ], badge='5–6 кл.'),
    _group('akcha', 'Акча: сатып алуу, кайтарым, эң пайдалуу баа', 'Өлчөмдөр › Акча', ['akcha'], [
        'measures-money-purchasing-non-calculator',
    ], badge='3–4 кл.'),
    _group('ondu_kk', 'Ондук бөлчөктөрдү кошуу жана кемитүү', 'Сандар › Ондуктар › Эсептөөлөр', ['ondu_kk'], [
        'subtracting-1-digit', 'adding-subtracting-1-digit',
        'adding-1-2-digit', 'subtracting-1-2-digit', 'adding-subtracting-1-2-digit',
        'integers-adding-with-decimals', 'integers-subtracting-with-decimals',
        'integers-adding-subtracting-with-decimals',
        'adding-with-integers', 'subtracting-with-integers', 'adding-subtracting-with-integers',
    ], badge='4–5 кл.'),
    _group('ondu_kb', 'Ондук бөлчөктөрдү көбөйтүү жана бөлүү', 'Сандар › Ондуктар › Эсептөөлөр', ['ondu_kb'], [
        'multiplying-1-digit', 'dividing-1-digit', 'multiplying-dividing-1-digit', 'mixed-1-digit',
        'dividing-by-less-than-1', 'multiplying-1-2-digit', 'dividing-1-2-digit', 'multiplying-dividing-1-2-digit',
        'mixed-1-2-digit',
        'integers-multiplying-with-decimals', 'integers-dividing-with-decimals',
        'integers-multiplying-dividing-with-decimals', 'integers-dividing-divisor-less-than-1-with-decimals',
        'integers-mixed-with-decimals', 'multiplying-with-integers', 'dividing-with-integers',
        'multiplying-dividing-with-integers', 'mixed-with-integers', 'dividing-divisor-less-than-1-with-integers',
    ]),
    _group('bolchok_t', 'Бөлчөк түшүнүгү', 'Сандар › Бөлчөктөр', ['bolchok_t'], [], badge='2–3 кл.'),
    _group('kvadrat', 'Квадрат жана куб сандар, даража', 'Сандар › Даражалар', ['kvadrat'], [
        'indices-introduction', 'indices-square-numbers', 'indices-cube-numbers',
        'evaluating-roots-square', 'evaluating-roots-square-cube',
    ], badge='7-класс'),
    _group('k100', '100 ичинде кошуу жана кемитүү', 'Сандар › Бүтүн сандар', ['k100'], [
        'integers-adding-1-2-digit',
    ], badge='1–2 кл.'),
    _group('kemituu', 'Кемитүү: 10 жана 100 ичинде', 'Сандар › Бүтүн сандар', ['kemituu10', 'k100'], [
        'integers-subtracting-1-2-digit',
    ]),
    _group('mamycha', 'Мамыча менен кошуу жана кемитүү', 'Сандар › Бүтүн сандар', ['mamycha'], [
        'integers-adding-2-3-digit', 'integers-subtracting-2-3-digit', 'integers-adding-subtracting-2-3-digit',
    ], badge='2–3 кл.'),
    _group('kob_jadybal', 'Көбөйтүү жана бөлүү', 'Сандар › Бүтүн сандар', ['kob234', 'jadybal'], [
        'integers-multiplying-1-2-digit', 'integers-dividing-1-2-digit', 'integers-multiplying-dividing-1-2-digit',
    ]),
    _group('sandyn_bolugu', 'Сандын бөлүгү', 'Сандар › Бөлчөктөр', ['sandyn_bolugu'], [], badge='4-класс'),
    _group('million', 'Миллион ичиндеги сандар', 'Сандар › Бүтүн сандар', ['million'], [], badge='5-класс'),
    _group('tegerektoo', 'Тегеректөө жана болжолдоо', 'Сандар › Болжолдоо жана тегеректөө', ['tegerektoo', 'million'], [
        'rounding-whole-numbers',
    ]),
    _group('kadimki', 'Кадимки бөлчөктөр', 'Сандар › Бөлчөктөр › Барабар бөлчөктөр', ['kadimki'], [
        'equivalent-fractions-comparing-inequality', 'equivalent-fractions-comparing-ordering',
        'equivalent-fractions-simplifying',
    ], badge='3–4 кл.'),
    _group('proporciya', 'Пропорция жана процент', 'Сандар › Пропорция', ['proporciya'], [
        'percentages-noncalc-quantity-integer-decimal',
        'percentages-quantity-integer', 'percentages-noncalc-quantity-10s', 'percentages-noncalc-quantity-5s',
    ], badge='5-класс'),
    _group('jonokoy', 'Жөнөкөй көбөйтүүчүлөр, ЭЧОБ жана ЭКОЭ', 'Сандар › Бөлүүчүлөр жана эселиктер', ['jonokoy'], [
        'hcf-lcm-listing-mixed', 'hcf-prime-factorisation', 'lcm-prime-factorisation', 'hcf-listing', 'lcm-listing',
    ], badge='7-класс'),
    _group('bolunuu', 'Бөлүнүү белгилери', 'Сандар › Бөлүүчүлөр жана эселиктер', ['bolunuu'], [], badge='4-класс'),
    _group('bolunuu_jonokoy', 'Бөлүүчүлөр, эселиктер жана жөнөкөй сандар', 'Сандар › Бөлүүчүлөр жана эселиктер',
           ['bolunuu', 'jonokoy'], [], badge='4–6 кл.'),
    _group('butun_kk', 'Бүтүн сандарды кошуу жана кемитүү', 'Сандар › Багытталган сандар', ['butun_kk'], [
        'adding-directed', 'subtracting-directed', 'adding-subtracting-directed',
    ], badge='7-класс'),
    _group('butun_kb', 'Бүтүн сандарды көбөйтүү жана бөлүү', 'Сандар › Багытталган сандар', ['butun_kb'], [
        'multiplying-dividing-directed',
    ], badge='7-класс'),
    _group('bagyttalgan', 'Багытталган сандар: амалдардын тартиби', 'Сандар › Багытталган сандар',
           ['bagyttalgan'], ['with-bidmas-directed', 'complex-directed'], badge='7-класс'),
    _group('directed_mixed', 'Багытталган сандар менен аралаш эсептөөлөр', 'Сандар › Багытталган сандар',
           ['butun_kk', 'butun_kb'], ['mixed-directed'], badge='7-класс'),
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
    _group('maalymat_chogultuu', 'Маалымат чогултуу, жыштык таблицасы жана пиктограмма', 'Дата', ['maalymat3', 'maalymat'], [
        'data-collecting-introduction',
        'data-collecting-vocabulary',
        'data-frequency-tables-ungrouped-data-creating-reading',
        'data-representing-pictograms',
    ]),
    _group('maalymat', 'Маалымат, диаграмма жана орто маани', 'Дата', ['maalymat'], [
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
    _group('kolom', 'Тик бурчтуу параллелепипеддин көлөмү жана бет аянты', 'Геометрия › Көлөм жана бет аянты', ['kolom'], [
        'geometry-volume-surface-area-introduction-to-volume',
        'geometry-volume-surface-area-vocabulary',
        'geometry-volume-surface-area-nets',
        'geometry-volume-surface-area-cuboid-volume',
        'geometry-volume-surface-area-cuboid-surface-area',
        'geometry-volume-surface-area-cuboid-mixed-foundation',
        'geometry-volume-surface-area-cuboid-mixed-higher',
    ]),
    _group('ylldamdyk', 'Ылдамдык, убакыт жана аралык', 'Сандар › Өлчөмдөр › Татаал өлчөмдөр', ['ylldamdyk'], [
        'compound-speed-distance-time',
        'speed-distance-time-two-stage-journeys',
        'speed-distance-time-relative-speeds',
    ]),
    _group('koordinattar', 'Координаталык тегиздик', 'Геометрия › Координаттар', ['koordinattar'], [
        'geometry-coordinates-reading',
        'geometry-coordinates-reading-plotting',
        'algebra-graphs-abstract-coordinates-reading',
        'algebra-graphs-abstract-coordinates-reading-plotting',
    ], badge='7-класс'),
    _group('masshtab', 'Масштаб', 'Сандар › Өлчөмдөр › Масштабдуу сүрөттөр', ['masshtab'], [
        'scale-drawings-lengths',
        'scale-drawings-estimation',
    ], badge='6–7 кл.'),
    _group('okshosh', 'Окшош мүчөлөр жана кашааны ачуу', 'Алгебра › Өзгөртүп түзүү', ['okshosh'], [
        'algebra-manipulation-expand-single-without-coefficients',
        'algebra-manipulation-expand-single-with-coefficients',
        'algebra-manipulation-expand-single-multiple',
        'algebra-manipulation-expand-single-mixed',
        'algebra-manipulation-expressions-adding-brackets',
        'algebra-manipulation-notation-adding-brackets',
        'algebra-linear-brackets-without-coefficients',
        'algebra-linear-brackets-with-coefficients',
    ], badge='7-класс'),
    _group('aylana', 'Айлана жана тегерек', 'Геометрия › Аянт жана периметр › Тегеректер', ['aylana'], [
        'geometry-area-perimeter-circles-vocabulary',
        'geometry-area-perimeter-circles-circumference',
        'geometry-area-perimeter-circles-area',
        'geometry-area-perimeter-circles-area-circumference',
        'geometry-area-perimeter-circles-mixed',
        'geometry-area-perimeter-compound-with-circles-area',
        'geometry-area-perimeter-compound-with-circles-perimeter',
        'geometry-area-perimeter-compound-with-circles-mixed',
        'geometry-area-perimeter-mixed-polygons-circles',
    ]),
    _group('turmushtuk', 'Турмуштук эсептөөлөр: баа, рецепт, валюта', 'Пропорция › Турмуштук колдонуулар', ['turmushtuk'], [
        'real-life-best-buys-non-calculator',
        'real-life-best-buys-calculator',
        'real-life-prices-non-calculator',
        'real-life-prices-calculator',
        'real-life-recipes-non-calculator',
        'real-life-recipes-calculator',
        'real-life-exchange-rates-non-calculator',
        'real-life-exchange-rates-calculator',
        'real-life-mixed-non-calculator',
        'real-life-mixed-calculator',
        'purchasing-calculator',
        'measures-money-purchasing-calculator',
    ], badge='5–6 кл.'),
    _group('uch_burchtuk', 'Үч бурчтуктун, параллелограммдын жана трапециянын аянты', 'Геометрия › Аянт жана периметр', ['uch_burchtuk'], [
        'geometry-area-perimeter-triangles-area',
        'geometry-area-perimeter-quadrilaterals-parallelogram',
        'geometry-area-perimeter-quadrilaterals-trapezium',
        'geometry-area-perimeter-compound-polygonal-area',
        'geometry-area-perimeter-compound-polygonal-perimeter',
        'geometry-area-perimeter-mixed-polygons',
    ]),
    _group('payyz', 'Пайыз: чоңдуктун пайызы, арзандатуу жана кымбаттоо', 'Пропорция › Пайыздар', ['payyz'], [
        'percentages-expressing-quantity',
        'percentages-expressing-change',
        'percentages-noncalc-expressing-quantity',
        'percentages-noncalc-expressing-change',
        'percentages-quantity-decimal',
        'percentages-incdec-increase',
        'percentages-incdec-decrease',
        'percentages-incdec-mixed',
        'percentages-noncalc-incdec-increase',
        'percentages-noncalc-incdec-decrease',
        'percentages-noncalc-incdec-mixed',
        'expressing-quantity',
        'expressing-change',
    ], badge='5–6 кл.'),
    _group('venn', 'Көптүктөр жана Венн диаграммалары', 'Дата › Көрсөтүү', ['venn'], [
        'data-representing-venn-diagrams-creating-reading',
        'data-representing-venn-diagrams-sets-with-notation',
    ], badge='7–9 кл.'),
    _group('kop_kb', 'Көп орундуу сандарды көбөйтүү жана бөлүү', 'Сандар › Бүтүн сандар', ['kop_kb'], [
        'integers-multiplying-2-3-digit',
        'integers-dividing-2-3-digit',
        'integers-multiplying-dividing-2-3-digit',
    ], badge='3–4 кл.'),
    _group('m1000', '10, 100, 1000ге көбөйтүү жана бөлүү', 'Сандар › Эсептөөлөр', ['m1000', 'ondu_kb'], [
        'multiplying-dividing-10-100-1000',
        'integers-multiplying-dividing-10-100-1000',
    ], badge='4–5 кл.'),
    _group('tuz_teskeri', 'Түз жана тескери пропорциялуулук', 'Пропорция › Түз жана тескери пропорция', ['tuz_teskeri', 'proporciya'], [
        'direct-inverse-introduction',
        'direct-inverse-direct',
        'direct-inverse-inverse',
        'direct-inverse-mixed',
    ]),
    _group('bolchok_kk', 'Бөлчөктөрдү кошуу жана кемитүү', 'Сандар › Бөлчөктөр › Эсептөөлөр', ['bolchok_kk'], [
        'unit-fractions-adding',
        'unit-fractions-subtracting',
        'unit-fractions-adding-subtracting',
        'unit-fractions-mixed',
        'non-unit-fractions-adding',
        'non-unit-fractions-subtracting',
        'non-unit-fractions-adding-subtracting',
        'non-unit-fractions-mixed',
    ]),
    _group('tegerek_diagramma', 'Тегерек диаграммалар', 'Дата', ['tegerek_diagramma'], [
        'data-representing-pie-charts-reading',
        'data-representing-pie-charts-proportional-method',
        'data-representing-pie-charts-scaling-method',
        'geometry-area-perimeter-circles-comparative-pie-charts',
    ]),
    _group('geometriya3', 'Бурчтар, төрт бурчтуктар жана тегерек', 'Геометрия › Фигуралар', ['geometriya3'], [
        'geometry-classifying-vocabulary-vocabulary-angles',
        'geometry-classifying-vocabulary-vocabulary-circles',
        'geometry-classifying-vocabulary-vocabulary-sketching-diagrams',
        'geometry-classifying-vocabulary-classifying-shapes-quadrilaterals',
        'geometry-area-perimeter-quadrilaterals-vocabulary',
    ]),
    _group('maani_eseptoo', 'Туюнтманын маанисин эсептөө: терс сандар жана квадрат', 'Алгебра › Ордуна коюу', ['maani_eseptoo'], [
        'algebra-substitution-without-indices-negative',
        'algebra-substitution-symbols-negative',
        'algebra-substitution-with-indices-positive',
        'algebra-substitution-mixed',
    ]),
    _group('eki_tarap', 'Теңдемелер: функция машинасы жана белгисиз эки тарапта', 'Алгебра › Сызыктуу теңдемелер', ['eki_tarap'], [
        'algebra-linear-forming-function-machines',
        'algebra-manipulation-forming-function-machines',
        'algebra-forming-expr-function-machines',
        'algebra-linear-forming-functions-sequences',
        'algebra-linear-var1side-calc-3step',
        'algebra-linear-brackets-multiple',
        'algebra-linear-var-both-sides-without-brackets',
        'algebra-linear-var-both-sides-with-brackets',
        'algebra-linear-variable-both-sides',
    ]),
    _group('tamga_kb', 'Тамгалуу мүчөлөрдү көбөйтүү жана бөлүү', 'Алгебра › Өзгөртүп түзүү', ['tamga_kb'], [
        'algebra-manipulation-notation-multiplying-adding',
        'algebra-manipulation-notation-dividing',
        'algebra-manipulation-notation-multiplying-dividing',
        'algebra-manipulation-notation-mixed-arithmetic',
        'algebra-manipulation-expressions-multiplying',
        'algebra-manipulation-expressions-multiplying-adding',
        'algebra-manipulation-expressions-multiplying-dividing',
        'algebra-manipulation-expressions-mixed-arithmetic',
    ]),
    _group('katysh_1n', 'Катыш: 1 : n түрү, катыштарды бириктирүү жана өзгөрүү', 'Сандар › Катыш', ['katysh_1n'], [
        'ratio-expressing-1-to-n',
        'ratio-manipulation-1-to-n',
        'ratio-manipulation-combining',
        'ratio-manipulation-changing',
        'ratio-dividing-fpr-non-calculator',
        'ratio-dividing-fpr-calculator',
        'ratio-mixed-higher',
    ]),
    _group('anketa', 'Анкета, эки тараптуу таблица жана орточо маани', 'Дата', ['anketa'], [
        'data-collecting-questionnaires',
        'data-frequency-tables-two-way-tables-creating-reading',
        'data-frequency-tables-two-way-tables-with-bar-charts',
        'data-frequency-tables-ungrouped-data-calculating-averages',
        'data-analysing-mean-adjusting',
        'data-analysing-mean-reverse',
        'data-analysing-choosing-an-average',
    ]),
    # Pages that span two neighbouring packs (2026-10-31).
    _group('figuralar_2_3', 'Фигуралар, бурчтар жана терминдер', 'Геометрия › Классификациялоо жана терминология',
           ['figuralar', 'geometriya3'], []),
    _group('tekst_maseleler', 'Текст маселелер: тилке модели менен', 'Сандар › Бүтүн сандар › Турмуштук маселелер',
           ['mamycha', 'kop_kb'], ['integers-real-life-calculator', 'integers-real-life-non-calculator']),
    _group('ayant_tort', 'Төрт бурчтуктардын периметри жана аянты', 'Геометрия › Аянт жана периметр',
           ['perimetr', 'uch_burchtuk'], []),
    _group('katysh_all', 'Катыш: бөлүү, 1 : n түрү жана бириктирүү', 'Пропорция › Катыш', ['katysh', 'katysh_1n'], []),
]

# Repeated menu items that teach the same thing as a page above: they show
# the same pack (2026-10-31; duplicates per sayt-mockup/bardyk-temalar).
_MORE_SLUGS = {
    'fdp': [
        'decimals-to-both', 'decimals-to-fractions', 'decimals-to-percentages',
        'decimals-with-both', 'decimals-with-fractions', 'decimals-with-percentages',
        'fractions-equiv-to-decimals-calculator', 'fractions-equiv-to-percentages-calculator',
        'fractions-to-decimals-calculator', 'fractions-to-percentages-calculator',
        'percentages-expressing-converting-fractions',
    ],
    'fdpr': ['percentages-quantity-fpr', 'percentages-noncalc-quantity-fpr'],
    'kadimki': ['equivalent-fractions-with-calculations'],
    'k100': ['integers-mixed-1-2-digit'],
    'mamycha': ['integers-mixed-2-3-digit'],
    'akcha': ['purchasing-non-calculator'],
    'katysh': ['ratio-dividing-with-line-segments'],
    'eki_tarap': ['algebra-functions-evaluating-simple-machines', 'algebra-linear-mixed'],
    'algebra': ['algebra-linear-forming-shapes-angles-real-life'],
}
for _group_spec in GROUPS:
    _group_spec['slugs'] = list(_group_spec['slugs']) + _MORE_SLUGS.get(_group_spec['spec']['page_key'][len('pack_'):], [])

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
    (('number', 'fractions', 'fraction-of-a-quantity'), 'sandyn_bolugu'),
    (('number', 'integers', 'place-value-ordering'), 'million'),
    (('number', 'integers', 'integers-as-words'), 'million'),
    (('number', 'factors-multiples-primes', 'prime-numbers'), 'jonokoy'),
    (('number', 'factors-multiples-primes', 'prime-factorisation-index-form'), 'jonokoy'),
    (('number', 'factors-multiples-primes', 'multiples'), 'bolunuu'),
    (('number', 'factors-multiples-primes', 'factors'), 'bolunuu'),
    (('number', 'integers', 'divisibility-rules'), 'bolunuu'),
    (('number', 'factors-multiples-primes', 'prime-numbers-factors-multiples'), 'bolunuu_jonokoy'),
    (('number', 'measures', 'reading-scales'), 'olchomdor'),
    (('geometry', 'transformations', 'reflection'), 'simmetriya'),
    (('geometry', 'transformations', 'translation'), 'simmetriya'),
    (('geometry', 'transformations', 'line-symmetry'), 'simmetriya'),
    (('geometry', 'construction', 'nets'), 'kolom'),
    (('number', 'estimating-rounding', 'scale-drawings-estimation'), 'masshtab'),
    (('number', 'estimating-rounding', 'approximating-calculations'), 'tegerektoo'),
    (('number', 'fractions', 'mixed-fraction-questions'), 'bolchok_kk'),
    (('statistics', 'analysing', 'mixed'), 'maalymat'),
    (('statistics', 'representing', 'mixed'), 'maalymat'),
    # 2026-10-31: empty grade 1–6 pages that an existing pack teaches.
    (('algebra', 'equations-linear', 'variable-on-one-side-calculator'), 'algebra'),
    (('algebra', 'equations-linear', 'variable-on-one-side-non-calculator'), 'algebra'),
    (('algebra', 'equations-linear', 'with-functions'), 'eki_tarap'),
    (('algebra', 'introduction', 'forming-expressions'), 'algebra'),
    (('geometry', 'angles', 'angle-facts'), 'burchtar'),
    (('geometry', 'angles', 'drawing-measuring'), 'burchtar'),
    (('geometry', 'angles', 'mixed'), 'burchtar'),
    (('geometry', 'construction', 'angles'), 'burchtar'),
    (('geometry', 'construction', 'measuring-lines'), 'olchomdor'),
    (('geometry', 'construction', 'sketching-diagrams'), 'geometriya3'),
    (('geometry', 'area-perimeter', 'circles'), 'aylana'),
    (('geometry', 'area-perimeter', 'compound-rectilinear'), 'perimetr'),
    (('geometry', 'area-perimeter', 'quadrilaterals'), 'ayant_tort'),
    (('geometry', 'area-perimeter', 'mixed'), 'ayant_tort'),
    (('geometry', 'area-perimeter', 'triangles'), 'uch_burchtuk'),
    (('geometry', 'classifying-vocabulary', 'classifying-shapes'), 'figuralar_2_3'),
    (('geometry', 'classifying-vocabulary', 'vocabulary'), 'figuralar_2_3'),
    (('geometry', 'coordinates'), 'koordinattar'),
    (('geometry', 'transformations', 'mixed'), 'simmetriya'),
    (('number', 'directed-numbers', 'ordering'), 'butun_kk'),
    (('probability', 'two-way-tables'), 'anketa'),
    (('probability', 'venn-diagrams'), 'venn'),
    (('proportion', 'percentages-calculator', 'mixed'), 'payyz'),
    (('proportion', 'ratio', 'mixed'), 'katysh_all'),
    (('proportion', 'real-life-applications', 'mixed'), 'turmushtuk'),
    (('proportion', 'real-life-applications', 'prices'), 'turmushtuk'),
    (('statistics', 'analysing', 'mean'), 'anketa'),
    (('statistics', 'collecting'), 'maalymat_chogultuu'),
    (('statistics', 'frequency-tables', 'two-way-tables'), 'anketa'),
    (('statistics', 'frequency-tables', 'ungrouped-data'), 'maalymat_chogultuu'),
    (('statistics', 'representing', 'venn-diagrams'), 'venn'),
]}

NEW_FILES = [
    pack['prefix'] + suffix.replace('.', pack.get('tail', '') + '.')
    for pack in PACKS.values() for suffix in SUFFIXES
]


# Subpages that share one pack but not one 12-year grade. The group's
# badge stays for every other page in that pack.
SPLIT_BADGES = {
    'time-calculations': '3–4 кл.',
    'time-converting': '3–4 кл.',
    'time-timetables': '3–4 кл.',
    ('geometry', 'transformations', 'reflection'): '7–9 кл.',
    ('geometry', 'transformations', 'translation'): '7–9 кл.',
    'geometry-volume-surface-area-cuboid-surface-area': '7-класс',
    'geometry-volume-surface-area-cuboid-mixed-foundation': '5–7 кл.',
    'geometry-volume-surface-area-cuboid-mixed-higher': '5–7 кл.',
    'compound-speed-distance-time': '6–7 кл.',
    'speed-distance-time-relative-speeds': '7–8 кл.',
    'speed-distance-time-two-stage-journeys': '7–8 кл.',
    'geometry-area-perimeter-quadrilaterals-parallelogram': '7-класс',
    'geometry-area-perimeter-quadrilaterals-trapezium': '7-класс',
    'geometry-area-perimeter-compound-polygonal-area': '5–7 кл.',
    'geometry-area-perimeter-compound-polygonal-perimeter': '5–7 кл.',
    'geometry-area-perimeter-mixed-polygons': '5–7 кл.',
    'dividing-by-less-than-1': '6–7 кл.',
    'dividing-divisor-less-than-1-with-integers': '6–7 кл.',
    'integers-dividing-divisor-less-than-1-with-decimals': '6–7 кл.',
    'data-analysing-median': '7-класс',
    'data-analysing-mode-range-mode': '7-класс',
    'data-analysing-mode-range-range': '7-класс',
    'data-analysing-comparing-using-mmmr': '7-класс',
    ('statistics', 'analysing', 'mixed'): '6–7 кл.',
    'algebra-linear-var1side-calc-1step': '7-класс',
    'algebra-linear-var1side-calc-2step': '7-класс',
    'algebra-linear-var1side-noncalc-1step': '7-класс',
    'algebra-linear-var1side-noncalc-2step': '7-класс',
    'direct-inverse-direct': '7-класс',
    'direct-inverse-inverse': '8-класс',
    'direct-inverse-introduction': '7–8 кл.',
    'direct-inverse-mixed': '7–8 кл.',
    ('algebra', 'equations-linear', 'variable-on-one-side-calculator'): '6–7 кл.',
    ('algebra', 'equations-linear', 'variable-on-one-side-non-calculator'): '6–7 кл.',
    ('geometry', 'angles', 'angle-facts'): '5–7 кл.',
    ('geometry', 'angles', 'mixed'): '5–7 кл.',
    ('geometry', 'area-perimeter', 'mixed'): '5–7 кл.',
    ('geometry', 'transformations', 'mixed'): '4–9 кл.',
}


def page_for(slug, page_title):
    """The group page for a placeholder slug (or a PATH_PAGES key), with the
    page's own title in the menu path above the heading, or None if no pack
    fits it yet."""
    spec = PATH_PAGES.get(slug) if isinstance(slug, tuple) else SLUG_PAGES.get(slug)
    if spec is None:
        return None
    spec = copy.copy(spec)
    spec['crumb'] = f"{spec['crumb']} › {page_title}"
    override = SPLIT_BADGES.get(slug)
    if override:
        spec['grade_badge'] = override
    from apps.resources.data.spiral import strands_for
    spec['strands'] = strands_for(spec['page_key'])
    return spec
