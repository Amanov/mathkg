"""Topic strands across grades (2026-10-31).

The site's menu repeats one idea in several places (fractions in grade 3,
5 and 6; data in grade 3 and 6, ...). Singapore teaches such an idea as a
spiral: each grade comes back to it one step deeper. Every pack page shows
the strand it belongs to, so a teacher sees the grade before and after and
what changes at each step, and can follow the links.

Each step names a group from pack_pages.GROUPS and says, for the teacher,
what is new at that step compared with the one before.
"""

from apps.resources.data.pack_pages import GROUPS, PATH_PAGES

STRANDS = [
    ('Кошуу жана кемитүү', [
        ('kemituu', 'Ташчалар жана он чакмак менен, сан курамы'),
        ('k100', 'Ондуктар жана бирдиктер, сан огунда секирүү'),
        ('mamycha', 'Мамыча менен жазуу, разряддан өтүү'),
        ('ondu_kk', 'Ондук үтүрлөрдү бирин биринин астына жазуу'),
        ('bolchok_kk', 'Бөлүмдөрү ар башка: жалпы бөлүм табуу'),
        ('butun_kk', 'Терс сандар: сан огунда эки тарапка'),
    ]),
    ('Көбөйтүү жана бөлүү', [
        ('kob_jadybal', 'Барабар топтор, массив жана жадыбал'),
        ('kop_kb', 'Көп орундуу сандар мамыча менен'),
        ('m1000', 'Разряддар солго же оңго жылат'),
        ('ondu_kb', 'Ондук үтүрдүн орду кантип өзгөрөт'),
        ('butun_kb', 'Белгилердин эрежеси: (−) × (−) = (+)'),
        ('bolchok_kb', 'Бөлчөккө бөлүү: тескери санга көбөйтүү'),
    ]),
    ('Сандар жана алардын касиеттери', [
        ('million', 'Разряд таблицасы миллионго чейин'),
        ('tegerektoo', 'Тегеректеп, жоопту алдын ала болжолдоо'),
        ('ondu_orun', 'Разряддар үтүрдөн кийин да уланат'),
        ('bolunuu', 'Бөлбөй туруп эле бөлүнөрүн билүү'),
        ('jonokoy', 'Жөнөкөй көбөйтүүчүлөр дарагы, ЭЧОБ жана ЭКОЭ'),
        ('kvadrat', 'Чарчы жана куб сандар, даража жазуусу'),
    ]),
    ('Бөлчөктөр', [
        ('bolchok_t', 'Бүтүндүн барабар бөлүктөрү, бүктөлгөн кагаз'),
        ('sandyn_bolugu', 'Тилке модели менен сандын бөлүгү'),
        ('kadimki', 'Барабар бөлчөктөр, кыскартуу жана салыштыруу'),
        ('bolchok_kk', 'Бөлүмдөрү ар башка: жалпы бөлүм табуу'),
        ('bolchok_kb', 'Бөлчөккө бөлүү: тескери санга көбөйтүү'),
        ('fdp', 'Бир сан үч жазылышта: бөлчөк, ондук, пайыз'),
    ]),
    ('Катыш, пропорция жана пайыз', [
        ('fdp', 'Пайыз: 100дүн бөлүгү'),
        ('payyz', 'Чоңдуктун пайызы, арзандатуу жана кымбаттоо'),
        ('katysh', 'Эки чоңдукту салыштыруу, тилке модели'),
        ('katysh_1n', '1 : n түрү, катыштарды бириктирүү'),
        ('proporciya', 'Барабар эки катыш: пропорция'),
        ('tuz_teskeri', 'Бири өскөндө экинчиси өсөбү же азаябы'),
        ('masshtab', 'Картадагы аралыктан чыныгы аралыкка'),
        ('turmushtuk', 'Баа, рецепт жана валюта'),
    ]),
    ('Өлчөмдөр', [
        ('ubakyt', 'Саат окуу, күн, ай жана календарь'),
        ('olchomdor', 'Сызгыч, тараза жана өлчөөчү идиш менен'),
        ('birdikter', 'Бирдиктерди алмаштыруу: см, м, км; г, кг'),
        ('akcha', 'Сатып алуу, кайтарым жана эң пайдалуу баа'),
        ('ylldamdyk', 'Ылдамдык = аралык ÷ убакыт'),
    ]),
    ('Фигуралар жана геометрия', [
        ('figuralar', 'Фигураларды таануу: жак, чоку, кыр'),
        ('geometriya3', 'Бурчтардын жана төрт бурчтуктардын түрлөрү'),
        ('simmetriya', 'Симметрия огу, чагылдыруу жана жылдыруу'),
        ('burchtar', 'Транспортир: бурчту градус менен өлчөө'),
        ('koordinattar', 'Чекиттин орду эки сан менен'),
    ]),
    ('Периметр, аянт жана көлөм', [
        ('perimetr', 'Чек ара узундугу жана бетти чарчылар менен жабуу'),
        ('uch_burchtuk', 'Тик бурчтуктан үч бурчтукка жана параллелограммга'),
        ('kolom', 'Кубиктер менен көлөм жана бет аянт'),
        ('aylana', 'Айлананын узундугу жана тегерек аянты, π'),
    ]),
    ('Маалымат жана диаграммалар', [
        ('maalymat_chogultuu', 'Чогултуу, жыштык таблица, пиктограмма'),
        ('venn', 'Көптүктөр жана Венн диаграммасы'),
        ('maalymat', 'Мамычалуу диаграмма жана орто маани'),
        ('tegerek_diagramma', 'Бүтүндүн бөлүктөрү тегерек диаграммада'),
        ('anketa', 'Өз анкетасы жана эки тараптуу таблица'),
    ]),
    ('Алгебра', [
        ('algebra', 'Тамга сандын ордунда: туюнтма жана теңдеме'),
        ('maani_eseptoo', 'Тамганын ордуна сан коюп эсептөө'),
        ('okshosh', 'Окшош мүчөлөрдү топтоо, кашааны ачуу'),
        ('tamga_kb', 'Тамгалуу мүчөлөрдү көбөйтүү жана бөлүү'),
        ('eki_tarap', 'Белгисиз теңдеменин эки тарабында'),
    ]),
    ('Оң жана терс сандар', [
        ('butun_kk', 'Сан огунда эки тарапка жүрүү'),
        ('butun_kb', 'Белгилердин эрежеси: (−) × (−) = (+)'),
        ('bagyttalgan', 'Терс сандар менен амалдардын тартиби'),
    ]),
]

_SPECS = {group['spec']['page_key'][len('pack_'):]: group for group in GROUPS}
_PATHS = {}
for _path, _spec in PATH_PAGES.items():
    _PATHS.setdefault(_spec['page_key'][len('pack_'):], _path)


def grade_label(spec):
    """The grade a pack page is for, as the page shows it ('5-класс',
    '2–3 кл.')."""
    if spec.get('grade_badge'):
        return spec['grade_badge']
    grades = sorted({item['grade'] for section in spec['sections'] for item in section['items']})
    if len(grades) == 1:
        return f'{grades[0]}-класс'
    return f'{grades[0]}–{grades[-1]} кл.'


def _first_grade(label):
    return int(next(ch for ch in label if ch.isdigit()))


def group_url(key):
    """One page that shows this group: its first menu slug, else the
    first database page it fills."""
    group = _SPECS[key]
    if group['slugs']:
        return f"/{group['slugs'][0]}/"
    return '/resources/topic/' + '/'.join(_PATHS[key]) + '/'


def _strand(title, steps, current):
    rows = []
    for key, change in steps:
        label = grade_label(_SPECS[key]['spec'])
        rows.append({
            'key': key,
            'title': _SPECS[key]['spec']['title'],
            'grade': label,
            'grade_num': _first_grade(label),
            'change': change,
            'url': group_url(key),
            'current': key == current,
        })
    rows.sort(key=lambda row: row['grade_num'])
    return {'title': title, 'steps': rows}


def strands_for(page_key):
    """The strands a pack page (page_key 'pack_<group>') belongs to."""
    current = page_key[len('pack_'):] if page_key.startswith('pack_') else page_key
    own = [_strand(title, steps, current) for title, steps in STRANDS if any(k == current for k, _ in steps)]
    if own or current not in _SPECS:
        return own
    # A page that joins two packs (e.g. fdpr = fdp + katysh) sits in the
    # strands of the packs it carries.
    packs = set(_SPECS[current]['packs'])
    return [_strand(title, steps, current) for title, steps in STRANDS
            if any(packs & set(_SPECS[k]['packs']) for k, _ in steps)]
