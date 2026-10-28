"""Kyrgyz wording fixes inside existing PowerPoint text runs.

The package is still rewritten by ``deck_text.rewrite_pptx``. This module
only decides the new characters. A match that crosses runs is rebuilt on
those runs; pictures, charts and the other runs stay as they were.

Thousands commas are removed before decimal points are turned into
commas, so ``51,052.91`` becomes ``51 052,91`` and a real decimal such
as ``0,768`` is left alone.
"""

from __future__ import annotations

import ast
import contextvars
import json
import re
from pathlib import Path

# Narrow no-break space. A thousands group should not break across a line.
NBSP = '\u202f'

_PROVEN = contextvars.ContextVar('kyrgyz_thousands', default=frozenset())

# Full instruction sentences, longest first at apply time. The new text is
# what a teacher would write, and it is not longer than the old sentence
# by more than a few characters (the text box stays the same).
SENTENCE_REWRITES = {
    'Окуучуларга  тарсиа курактын туура болгондон кийин гана, клей менен жабыштырууну сунуштоо керек':
        'Окуучулар куракты туура чогулткандан кийин гана клей менен чапташсын.',
    'Бул ресурс математикалык ыкманын жандуу демонстрацияларын камсыз кылат.':
        'Бул ресурс ыкманы жандуу көрсөтөт.',
    'Бул ресурс математикалык ыкманын жандуу    демонстрацияларын камсыз кылат.':
        'Бул ресурс ыкманы жандуу көрсөтөт.',
    'Мугалим үчүн жооп баракчасы жана таратма материалдар камтылган.':
        'Мугалим үчүн жооп барагы жана таратма материалдар бар.',
    "Кайсы команда туура жооп бергенине жараша 'X' же 'O' баскычын басыңыз/тийип коюңуз.":
        'Туура жооп берген командага жараша «X» же «O» баскычын басыңыз.',
    'Окуучулар суроо тордон тогуз жоопту тандап, аларды дептериндеги 3х3 квадратка туш келди жайгаштырышы керек.':
        'Окуучулар тордон тогуз жоопту тандап, дептердеги 3х3 чакмакка каалагандай коюшат.',
    'Музыканы баштоо үчүн каалаган жерди чыкылдатыңыз, андан кийин суроону көрсөтүү үчүн "Өттү" чыкылдатыңыз, анан жоопту көрсөтүү үчүн кайра басыңыз.':
        'Музыка үчүн каалаган жерди басыңыз. Суроо үчүн «Өттү» дегенди, жооп үчүн дагы бир жолу басыңыз.',
    'Ошол команда үчүн квадратты талап кылуу үчүн жооп кутучасынын тиешелүү көлөкө тарабын чыкылдатыңыз/тийиңиз.':
        'Ошол команданын квадратын ээлөө үчүн жооп кутучасынын боёлгон бөлүгүн басыңыз.',
    'Тиешелүү суроого өтүү үчүн алты бурчтук тамганы басыңыз/тийиңиз.':
        'Суроого өтүү үчүн алты бурчтуктагы тамганы басыңыз.',
    'Алар үчүн алты бурчтук талап кылуу үчүн команданын түсүн тандаңыз.':
        'Алты бурчтукту ээлөө үчүн команданын түсүн тандаңыз.',
    'Жеңүүчү деп эң жогорку баалуулукка ээ болгон студент/топ/ тарап эсептелет.':
        'Эң чоң мааниге ээ окуучу же топ жеңет.',
    'Суроону тандоо үчүн ак кутучаны басыңыз/тийиңиз. Тиешелүү суроого өтүү үчүн номерди басыңыз.':
        'Суроону тандоо үчүн ак кутучаны басыңыз. Ошол суроого өтүү үчүн номерди басыңыз.',
    'Бул конкурстук иш-чарада бир окуучу , 2 же андан көп студенттен турган команданын кабарчысы болуп саналат.':
        'Бул жарышта бир окуучу, 2 же андан көп окуучудан турган команданын кабарчысы болот.',
    'Упайлар системасы менен студенттер тиешелүү суроолорго аракет кыла алышат.':
        'Упайына жараша окуучулар суроо тандап жооп бере алышат.',
    'Тиешелүү суроого өтүү үчүн тордун квадратын басыңыз/тийиңиз.':
        'Суроого өтүү үчүн тордогу чакмакты басыңыз.',
    'Студенттер өз жоопторун эки - экиден же мугалимге  көрсөтүп текшере алышы керек.':
        'Окуучулар жообун жупташып же мугалимге көрсөтүп текшерет.',
    'Студенттер мини-тактада же дептер аркылуу жооп бере алышат':
        'Окуучулар мини-тактага же дептерге жооп жаза алышат',
    'Студенттер упай топтоп, бомбаны ачса, жарымынан (же кааласаңыз, бардыгынан!) айрылышат.':
        'Окуучулар упай топтойт. Бомбаны ачса, жарымынан (же баарынан) айрылат.',
    'Карталардын ар кандай өлчөмдөрү камтылган.':
        'Карталардын ар кандай өлчөмү бар.',
    'Окуучуларга багыттар берилиши мүмкүн (мугалим же башка студенттер тарабынан) жана жоопту биринчи көрсөткөн окуучу өз командасына упай алат.':
        'Мугалим же башка окуучулар тапшырма бериши мүмкүн. Жоопту биринчи көрсөткөн окуучу өз командасына упай алат.',
    'Студенттер "Старттан" "Аягына" чейинки жолду табышы керек,':
        'Окуучулар «Старттан» «Аягына» чейинки жолду табат,',
    'Студенттер дубалдагы боштуктан гана өтө алышат.':
        'Окуучулар дубалдагы бош жерден гана өтөт.',
    'Студенттер үчүн "Өзүң жаса конугуусу" камтылган.':
        'Окуучулар үчүн «Өзүң жаса» бөлүмү бар.',
    'Студенттер кайчылаш суроолорду жана жооптордун каталарын текшерип, анан аларды оңдоосу керек.':
        'Окуучулар суроо менен жооптогу каталарды текшерип, оңдошот.',
    'Студенттерге канча каталарды табышы керек экенин айтуу зарыл эмес.':
        'Окуучуларга канча ката табарын айтуу шарт эмес.',
    'Бул карталар ар түрдүү атаандаштык жана биргелешкен оюндарда колдонулушу мүмкүн.':
        'Бул карталар жарышта да, бирге ойногондо да колдонулат.',
    'Студенттердин топтору (2+) карталардын бир топтомун колдонушат жана эң жакшы эки картаны айлантышат. Бул карталар бөлүшкөн терминди биринчи аныктаган оюнчу бир картаны сактайт. Жаңы карта бул картаны алмаштырат жана кайрадан студенттер дал келген терминди табышы керек. Аягында эң көп карта бар студент жеңет! (Эгер карталардын бири дайыма сакталып турса, оюн жеңилирээк болот.)':
        'Окуучулар (2+) бир топтом карта менен ойношот. Эки картаны ачышат. Орток терминди биринчи тапкан окуучу бир картаны алат. Анын ордуна жаңы карта коюлат, анан дал келген терминди кайра издешет. Эң көп картасы бар окуучу жеңет. (Бир карта дайыма кала берсе, оюн жеңилирээк.)',
    'Студенттердин топтору (2+) баштапкы картаны коюп, калганын ортосуна бөлүштүрүшөт. Студенттер баштапкы картага дал келүү үчүн жогорку картасын гана карашат. Дал келүүнү билдиргенден кийин студент өзүнүн картасын старттык картага кое алат. Эми бардык оюнчулар жогорку картасын бул жаңы картага дал келтириши керек. Бардык карталарынан кутулуу менен утуп алган студенттер бардык карталар ойнолмоюнча башка оюнчуларга жардам бере алышат.':
        'Окуучулар (2+) бир картаны ортого коюп, калганын бөлүшөт. Ар ким үстүнкү картасын гана карап, ортодогу картага дал келтирет. Дал келсе, өз картасын үстүнө коёт. Эми баары жаңы картага дал келтирет. Картасы түгөнгөн окуучу калгандарга жардам берет, карта бүткөнчө.',
    'Жеке адамдар/студенттердин топтору карталарды домино ташы катары колдоно алышат, анткени ар бир карта башка каалаган карта менен байланыштырылышы мүмкүн.':
        'Окуучулар же топтор картаны домино ташындай колдонот: ар бир карта башка каалаган карта менен уланат.',
    'Студенттерге сапка коюлганда ар бир жуп карталардын ортосунда кандай терминдер бөлүшүлгөнүн белгилөө маанилүү.':
        'Окуучулар катар койгондо, эки картанын ортосундагы орток терминди белгилеши керек.',
    'Карталардын бир нече + жарым-жартылай комплекттери викторина-викторина-соода карталары катары колдонулушу мүмкүн. Студенттер өз картасын башка студенттер менен салыштырып, дал келген терминди таба алышат. Студенттер андан кийин карталарды алмаштырып, экинчи студентти таба алышат. Атаандаштыкта, студенттер убакыттын чегинде жетишилген матчтардын жана алмашуулардын санын жаза алышат..':
        'Картанын толук же жарым топтомун «суроо–суроо–алмаш» оюнуна колдонсо болот. Окуучу өз картасын башкасыныкы менен салыштырып, дал келген терминди табат. Анан карта алмашып, башка окуучуну табат. Жарышта убакыт ичинде канча жолу дал келгенин жана алмашканын жазышат.',
    'Эгерде студенттер туура эмес болсо, алар суроону өткөрүп жибериши мүмкүн же 1 упай берилип же андан башка мүмкүнчүлүк берилет ':
        'Туура чыкпаса, окуучу суроону өткөрүп жибериши мүмкүн, же 1 упай, же дагы бир мүмкүнчүлүк алат. ',
    'Студенттер тордон тогуз жоопту тандап, аларды китебиндеги 3х3 квадратка туш келди жайгаштырышы керек.':
        'Окуучулар тордон тогуз жоопту тандап, китептеги 3х3 чакмакка каалагандай коюшат.',
    'Убакыттын өтүшүнө жараша, студенттер сызык, X же "толук үй" (бардыгы) менен жеңе алышат.':
        'Убакытка жараша окуучулар сызык, X же бүт тор («бардыгы») менен жеңе алат.',
    'Бул студенттерди тестирлөө үчүн тез Powerpoint оюну.':
        'Окуучуну тез текшерүүчү кыска Powerpoint оюну.',
    'Кийинки суроону берүү үчүн "Кийинки Оюнчу " баскычын чыкылдатыңыз.':
        'Кийинки суроо үчүн «Кийинки Оюнчу» баскычын басыңыз.',
    'Команданын унаасын чыкылдатып, аны бир орун алдыга жылдырыңыз. Жеңүүчү анимация бар':
        'Команданын унаасын басып, бир орун алдыга жылдырыңыз. Жеңгенде анимация чыгат.',
    'Жооп үчүн "Жооп" кутучасын чыкылдатып, оюн тактасына кайра кайтыңыз.':
        'Жооп үчүн «Жооп» кутучасын басып, оюн тактасына кайтыңыз.',
}

# Longer phrases first. These are the approved safe pairs, not whole notes.
_PHRASES = (
    ('көбөйтүүбүз керек', 'көбөйтөбүз'),
    ('бөлүшүбүз керек', 'бөлөбүз'),
    ('Ар кандай пикир ыраазычылык', 'Ар кандай пикир үчүн ыраазычылык'),
    ('кайсы жана клей', 'кайчы жана клей'),
    ('өз дептерге', 'өз дептерине'),
    ('өз топторго', 'өз топторуна'),
    ('бул тен чыгуу', 'бул тең чыгуу'),
    ('бул тен болсо', 'бул тең болсо'),
    ('Торт амал', 'Төрт амал'),
    ('торт амал', 'төрт амал'),
    ('Жейилген', 'Желген'),
    ('жейилген', 'желген'),
    ('Жейилди', 'Желди'),
    ('жейилди', 'желди'),
    ('даярдаоган', 'даярдалган'),
    ('салышатю', 'салышат.'),
    ('Баардык', 'Бардык'),
    ('баардык', 'бардык'),
    ('кемитүүдон', 'кемитүүдөн'),
    ('Көбурөөк', 'Көбүрөөк'),
    ('көбурөөк', 'көбүрөөк'),
    ('Кондум', 'Көндүм'),
    ('кондум', 'көндүм'),
    ('Устунку', 'Үстүнкү'),
    ('устунку', 'үстүнкү'),
    ('караныз', 'караңыз'),
    ('корсото', 'көрсөтө'),
    ('бөлчөгу', 'бөлчөгү'),
    ('дукөн', 'дүкөн'),
    ('коебуз', 'коёбуз'),
    ('чоңоет', 'чоңоёт'),
    ('ырахмат', 'рахмат'),
    ('иреттээлген', 'ирээттелген'),
    ('Иреттээлген', 'Ирээттелген'),
    ('Студенттик көрүнүш', 'Окуучунун көрүнүшү'),
    ('студенттик көрүнүш', 'окуучунун көрүнүшү'),
)

# «Маселени чыгар», not «чеч». «Чечет» (decides), «чечим» and «чечүүчү суроо»
# stay: those are decisions, not solving a problem.
_SOLVE = (
    (re.compile(r'([Мм])аселе чечүү(?!ч)'), lambda m: ('М' if m.group(1) == 'М' else 'м') + 'аселе чыгаруу'),
    (re.compile(r'([Мм])аселе чечилди'), lambda m: ('М' if m.group(1) == 'М' else 'м') + 'аселе чыгарылды'),
    (re.compile(r'([Тт])еңдемелерди чечүү(?!ч)'), lambda m: ('Т' if m.group(1) == 'Т' else 'т') + 'еңдемелерди чыгаруу'),
    (re.compile(r'([Тт])еңдеме чечүү(?!ч)'), lambda m: ('Т' if m.group(1) == 'Т' else 'т') + 'еңдеме чыгаруу'),
    (re.compile(r'аркылуу чечүү(?!ч)'), 'аркылуу чыгаруу'),
    (re.compile(r'тартып чечүү(?!ч)'), 'тартып чыгаруу'),
    (re.compile(r'түзүп чечүү(?!ч)'), 'түзүп чыгаруу'),
    (re.compile(r'ойлонуп чеч(?![А-Яа-яӨөҮүҢң])'), 'ойлонуп чыгар'),
    (re.compile(r'([Чч])ечиңиз'), lambda m: ('Ч' if m.group(1) == 'Ч' else 'ч') + 'ыгарыңыз'),
    (re.compile(r'(?<=[, ])чеч(?=, текшер)'), 'чыгар'),
)

# Multiple-choice labels follow the Kyrgyz alphabet, not Latin A B C D.
_OPTION_LETTER = {
    'A': 'А', 'B': 'Б', 'C': 'В', 'D': 'Г',
    'E': 'Д', 'F': 'Е', 'G': 'Ж', 'H': 'З',
}
# A choice label is "A) 4" or a line that is only "A)". Not "(H)", "3C)" or "Points A & B)".
_OPTION_RE = re.compile(
    "(?:^|(?<=[\\n\\r])|(?<=>)|(?<=\")|(?<=\'))([A-H])\\)(?=\\s|$|<)"
    "|(?<=\\s)([A-H])\\)(?=\\s)"
)
_BARE_THOUSANDS = re.compile(r'(?<!\d)(\d{5,})(?!\d)')

_STUDENT = (
    ('студенттерге', 'окуучуларга'),
    ('студенттерди', 'окуучуларды'),
    ('студенттердин', 'окуучулардын'),
    ('студенттерден', 'окуучулардан'),
    ('студенттерде', 'окуучуларда'),
    ('студенттер', 'окуучулар'),
    ('студенттен', 'окуучудан'),
    ('студенттин', 'окуучунун'),
    ('студентти', 'окуучуну'),
    ('студентке', 'окуучуга'),
    ('студентте', 'окуучуда'),
    ('студент', 'окуучу'),
)

_LATIN_TO_CYR = {
    'A': 'А', 'a': 'а', 'B': 'В', 'C': 'С', 'c': 'с', 'E': 'Е', 'e': 'е',
    'H': 'Н', 'K': 'К', 'M': 'М', 'O': 'О', 'o': 'о', 'P': 'Р', 'p': 'р',
    'T': 'Т', 'X': 'Х', 'x': 'х', 'Y': 'У', 'y': 'у', 'd': 'д', 'D': 'Д',
}

_CYR = re.compile(r'[А-Яа-яӨөҮүҢңЁё]')
_WORD = re.compile(r'[A-Za-zА-Яа-яӨөҮүҢңЁё]+')
_IRET = re.compile(r'(?<![А-Яа-яӨөҮүҢңA-Za-z])([Ии])рет')
_UCHUN = re.compile(r'(?<![А-Яа-яӨөҮүҢң])([Уу])чун(?![А-Яа-яӨөҮүҢң])')
_SPACE_COMMA = re.compile(r'(?<=[А-Яа-яӨөҮүҢңA-Za-z»")»])[ \t]+,')
_THOUSANDS = re.compile(r'(?<!\d)(\d{1,3}(?:,\d{3})+)(\.\d+)?(?!\d)')
_DECIMAL = re.compile(r'(?<!\d)(\d+)\.(\d+)(?!\d)')
_SECTION_RANGE = re.compile(r'(?<!\d)\d{1,2}\.\d{1,2}[–—-]\d{1,2}\.\d{1,2}(?!\d)')
_A_P = re.compile(r'<a:p(?:\s[^>]*)?>(.*?)</a:p>', re.DOTALL)
_A_T = re.compile(r'<a:t(?:\s[^>]*)?>(.*?)</a:t>', re.DOTALL)

_MANIFEST = Path(__file__).resolve().parent / 'data' / 'deck_kyrgyz_manifest.json'
_PROSE_MANIFEST = Path(__file__).resolve().parent / 'data' / 'kyrgyz_prose_manifest.json'

# Letters that are not Kyrgyz. A rewrite must not introduce them.
_FOREIGN = re.compile(r'[әғқұһіӘҒҚҰҺІğşıİöüçĞŞ]')


def _redistribute(texts, updated):
    """Write the edited paragraph back without moving unchanged runs."""
    import difflib

    joined = ''.join(texts)
    if joined == updated:
        return list(texts)
    out = list(texts)
    matcher = difflib.SequenceMatcher(a=joined, b=updated, autojunk=False)
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        if tag == 'equal':
            continue
        out, _n = _splice(out, i1, i2, updated[j1:j2])
    if ''.join(out) != updated:
        return [updated, *['' for _ in texts[1:]]]
    return out


def _splice(texts, start, end, new):
    out = list(texts)
    spans = []
    pos = 0
    for index, text in enumerate(out):
        spans.append((pos, pos + len(text), index))
        pos += len(text)
    overlapping = [index for begin, finish, index in spans if finish > start and begin < end]
    if not overlapping:
        return out, 0
    first = overlapping[0]
    last = overlapping[-1]
    begin = spans[first][0]
    last_begin = spans[last][0]
    prefix = out[first][: start - begin]
    suffix = out[last][end - last_begin :]
    if first == last:
        out[first] = prefix + new + suffix
    else:
        out[first] = prefix + new
        for index in overlapping[1:-1]:
            out[index] = ''
        out[last] = suffix
    return out, 1


def _replace_all(texts, old, new):
    found = 0
    while True:
        joined = ''.join(texts)
        start = joined.find(old)
        if start < 0:
            return texts, found
        texts, n = _splice(texts, start, start + len(old), new)
        found += n


def _cap_like(source, target):
    if source[:1].isupper():
        return target[:1].upper() + target[1:]
    return target


def _latin_token(token):
    if not _CYR.search(token) or not re.search(r'[A-Za-z]', token):
        return token
    return ''.join(_LATIN_TO_CYR.get(char, char) for char in token)


def _obvious_thousands(token):
    """English grouping that cannot be a Kyrgyz decimal."""
    if '.' in token:
        return True
    groups = token.split(',')
    if len(groups) >= 3:
        return True
    if len(groups) == 2 and groups[1] == '000' and groups[0].isdigit() and int(groups[0]) >= 10:
        return True
    return False


def _thousands_value(token):
    head, dot, frac = token.partition('.')
    digits = head.replace(',', '')
    if not digits.isdigit():
        return None
    if dot:
        return float(f'{digits}.{frac}')
    return float(digits)


def _decimal_value(token):
    if token.count(',') != 1 or '.' in token:
        return None
    head, frac = token.split(',')
    if not head.isdigit() or not frac.isdigit():
        return None
    return float(f'{head}.{frac}')


def _sanitize(side, *, thousands):
    text = side
    for src, dst in (('×', '*'), ('÷', '/'), ('–', '-'), ('−', '-'), ('—', '-')):
        text = text.replace(src, dst)
    # ``47,713 + 7%`` in these loans means the amount plus 7 percent of it.
    text = re.sub(
        r'(\d+(?:[ ,]\d{3})*(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)%',
        r'(\1*(1+\2/100))',
        text,
    )
    text = re.sub(r'[^\d.,+\-*/() \u00a0]', ' ', text)
    text = text.replace(NBSP, '').replace('\u00a0', '').replace(' ', '')
    if not text:
        return None
    if thousands:
        text = re.sub(r'(?<=\d),(?=\d{3}(?:\D|$))', '', text)
        text = text.replace(',', '.')
    else:
        text = text.replace(',', '.')
    if not re.fullmatch(r'[\d.+\-*/()]+', text):
        return None
    return text


def _eval_math(text):
    if text is None:
        return None
    try:
        tree = ast.parse(text, mode='eval')
    except SyntaxError:
        return None
    allowed = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd,
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            return None
    try:
        value = eval(compile(tree, '<n>', 'eval'), {'__builtins__': {}}, {})
    except (ZeroDivisionError, OverflowError, ValueError):
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _equation_proves(token, paragraph):
    target = _thousands_value(token)
    as_decimal = _decimal_value(token)
    if target is None:
        return False
    for side in re.split(r'[=≈]', paragraph):
        if token in side and not re.search(r'[+×÷*/\-–−]', side):
            continue
        value = _eval_math(_sanitize(side, thousands=True))
        if value is None or abs(value - target) > 1.5:
            continue
        if as_decimal is not None:
            other = _eval_math(_sanitize(side, thousands=False))
            if other is not None and abs(other - as_decimal) <= 0.05:
                continue
        return True
    return False


def _base(token):
    return token.split('.', 1)[0]


def collect_proven(paragraphs):
    """Comma-groups in this deck that are thousands, not decimals."""
    proven = set()
    pending = []
    for paragraph in paragraphs:
        for match in _THOUSANDS.finditer(paragraph):
            token = match.group(0)
            if token.startswith('0,'):
                continue
            if (
                _obvious_thousands(token)
                or _money_thousands(token, paragraph)
                or _feeds_obvious_result(token, paragraph)
                or _scaled_thousands(token, paragraph)
                or _equation_proves(token, paragraph)
            ):
                proven.add(_base(token))
            else:
                pending.append((token, paragraph))
    scaled_file = any(_scaled_paragraph(paragraph) for paragraph in paragraphs)
    money_file = any(
        base.split(',')[0].isdigit() and int(base.split(',')[0]) >= 10
        for base in proven
    )
    if scaled_file or money_file:
        for token, paragraph in pending:
            base = _base(token)
            if base in proven or token.startswith('0,') or _DECIMAL_LESSON.search(paragraph):
                continue
            if not _bare_number(paragraph, token):
                continue
            head = token.split(',')[0]
            if scaled_file or (head.isdigit() and int(head) >= 10):
                proven.add(base)
    # A result of two already-proven operands is a thousands number too.
    changed = True
    while changed:
        changed = False
        for token, paragraph in pending:
            base = _base(token)
            if base in proven or token.startswith('0,'):
                continue
            if _result_of_proven(token, paragraph, proven):
                proven.add(base)
                changed = True
    return frozenset(proven)


def _result_of_proven(token, paragraph, proven):
    """A comma-number is thousands when the other groups in the sum already are."""
    others = {_base(match.group(0)) for match in _THOUSANDS.finditer(paragraph)}
    others.discard(_base(token))
    if not others or not others <= proven:
        return False
    target = _thousands_value(token)
    for side in re.split(r'[=≈]', paragraph):
        side_bases = {_base(match.group(0)) for match in _THOUSANDS.finditer(side)}
        if _base(token) in side_bases and not re.search(r'[+×÷*/\-–−]', side):
            continue
        value = _eval_math(_sanitize(side, thousands=True))
        if value is not None and target is not None and abs(value - target) <= 1.5:
            return True
    return False


_MONEY_WORD = re.compile(r'сом|насыя|депозит|төлө')
_DECIMAL_LESSON = re.compile(r'жүздөн|разряд|бөлчөк|ортосунда|өсүү тартиби|ондон бир')


def _money_thousands(token, paragraph):
    """A grouped number next to a money word is a thousands amount."""
    if not re.fullmatch(r'\d{1,3}(?:,\d{3})+', token) or token.startswith('0,'):
        return False
    if _DECIMAL_LESSON.search(paragraph) or not _MONEY_WORD.search(paragraph):
        return False
    return True


def _scaled_paragraph(paragraph):
    return bool(re.search(r'[×÷]\s*(?:10|100|1000)(?!\d)', paragraph))


def _bare_number(paragraph, token):
    return re.fullmatch(rf'\s*=?\s*{re.escape(token)}\s*', paragraph) is not None


def _scaled_thousands(token, paragraph):
    if token.startswith('0,') or _DECIMAL_LESSON.search(paragraph):
        return False
    if not re.fullmatch(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?', token):
        return False
    return _scaled_paragraph(paragraph)


def _feeds_obvious_result(token, paragraph):
    """An operand is thousands when the result is already English-grouped."""
    for match in _THOUSANDS.finditer(paragraph):
        other = match.group(0)
        if other == token or not _obvious_thousands(other):
            continue
        result = _thousands_value(other)
        for side in re.split(r'[=≈]', paragraph):
            if token not in side:
                continue
            value = _eval_math(_sanitize(side, thousands=True))
            if value is not None and result is not None and abs(value - result) <= 1.5:
                return True
    return False


def _is_thousands(token, paragraph):
    if token.startswith('0,'):
        return False
    if _base(token) in _PROVEN.get():
        return True
    if (
        _obvious_thousands(token)
        or _money_thousands(token, paragraph)
        or _scaled_thousands(token, paragraph)
        or _feeds_obvious_result(token, paragraph)
    ):
        return True
    return _equation_proves(token, paragraph)


def _group_digits(digits):
    parts = []
    rest = digits
    while rest:
        parts.append(rest[-3:])
        rest = rest[:-3]
    return NBSP.join(reversed(parts))


def _skip_bare_thousands(text, match):
    window = text[max(0, match.start() - 16) : match.end() + 12].lower()
    return any(mark in window for mark in ('http', 'www.', '.pptx', '.pdf', '.png', '.svg', '.html'))


def _skip_decimal(text, match):
    start, end = match.start(), match.end()
    window = text[max(0, start - 24) : end + 16]
    if any(mark in window for mark in ('http', 'www.', '@', 'mailto:')):
        return True
    if start > 0 and text[start - 1] in 'vV§':
        return True
    if end < len(text) and text[end] == '.':
        return True
    if start > 0 and text[start - 1] == '.':
        return True
    around = text[max(0, start - 8) : end + 8]
    if _SECTION_RANGE.search(around):
        return True
    # ``2011-стандарт 3.2`` is a curriculum clause, not a decimal.
    before = text[max(0, start - 16) : start].lower()
    if before.rstrip().endswith('стандарт'):
        return True
    whole, frac = match.group(1), match.group(2)
    if (
        len(frac) == 2
        and whole.isdigit()
        and int(whole) <= 23
        and int(frac) <= 59
        and re.search(r'саат|мүнөт|таң|кеч', window)
        and not re.search(r'[$£€сом]', window)
    ):
        return True
    return False


def _apply_joined(text, counts, *, numbers=True):
    """Fixes that are easier to see once runs have been joined."""
    original = text
    for old, new in sorted(SENTENCE_REWRITES.items(), key=lambda item: len(item[0]), reverse=True):
        if old in text:
            hits = text.count(old)
            text = text.replace(old, new)
            counts['rewrite'] += hits
    for old, new in _PHRASES:
        if old in text:
            hits = text.count(old)
            text = text.replace(old, new)
            counts['safe'] += hits
    for pattern, repl in _SOLVE:
        updated, hits = pattern.subn(repl, text)
        text = updated
        counts['solve'] = counts.get('solve', 0) + hits

    updated, hits = _UCHUN.subn(lambda m: ('Ү' if m.group(1) == 'У' else 'ү') + 'чүн', text)
    text = updated
    counts['safe'] += hits

    def iret(match):
        return ('И' if match.group(1) == 'И' else 'и') + 'рээт'

    updated, hits = _IRET.subn(iret, text)
    text = updated
    counts['iret'] += hits

    for old, new in _STUDENT:
        pattern = re.compile(
            rf'(?<![А-Яа-яӨөҮүҢң])({old[0].upper()}{old[1:]}|{old})(?![А-Яа-яӨөҮүҢң])'
        )

        def student(match, replacement=new):
            return _cap_like(match.group(0), replacement)

        updated, hits = pattern.subn(student, text)
        text = updated
        counts['student'] += hits

    def option_letter(match):
        letter = match.group(1) or match.group(2)
        return _OPTION_LETTER[letter] + ')'

    updated, hits = _OPTION_RE.subn(option_letter, text)
    text = updated
    counts['option'] = counts.get('option', 0) + hits

    def latin(match):
        return _latin_token(match.group(0))

    updated, hits = _WORD.subn(latin, text)
    # subn counts every word. Count only tokens that changed.
    if updated != text:
        counts['latin'] += sum(
            1 for old, new in zip(_WORD.findall(text), _WORD.findall(updated)) if old != new
        )
        text = updated

    if numbers:
        def thousands(match):
            token = match.group(0)
            if not _is_thousands(token, text):
                return token
            counts['thousands'] += 1
            return token.replace(',', NBSP)

        text = _THOUSANDS.sub(thousands, text)

        def bare_thousands(match):
            if _skip_bare_thousands(text, match):
                return match.group(0)
            counts['thousands'] += 1
            return _group_digits(match.group(1))

        text = _BARE_THOUSANDS.sub(bare_thousands, text)

        def decimal(match):
            if _skip_decimal(text, match):
                return match.group(0)
            return match.group(1) + ',' + match.group(2)

        updated = _DECIMAL.sub(decimal, text)
        decimal_hits = 0
        for match in _DECIMAL.finditer(text):
            if _skip_decimal(text, match):
                continue
            decimal_hits += 1
        text = updated
        counts['decimal'] += decimal_hits

    updated, hits = _SPACE_COMMA.subn(',', text)
    text = updated
    counts['safe'] += hits
    if text != original and _FOREIGN.search(text) and not _FOREIGN.search(original):
        raise ValueError('rewrite introduced a non-Kyrgyz letter')
    return text


def apply_kyrgyz_page(text):
    """Page copy only: solve-verbs, option letters, студент, ирээт.

    The slide rewriter also fixes typos and decimals. Page source keeps
    code, CSS and English abbreviations alone.
    """
    counts = empty_counts()
    original = text
    for pattern, repl in _SOLVE:
        text, hits = pattern.subn(repl, text)
        counts['solve'] += hits
    for old, new in (
        ('Студенттик көрүнүш', 'Окуучунун көрүнүшү'),
        ('студенттик көрүнүш', 'окуучунун көрүнүшү'),
    ):
        hits = text.count(old)
        if hits:
            text = text.replace(old, new)
            counts['student'] += hits
    for old, new in _STUDENT:
        pattern = re.compile(
            rf'(?<![А-Яа-яӨөҮүҢң])({old[0].upper()}{old[1:]}|{old})(?![А-Яа-яӨөҮүҢң])'
        )

        def student(match, replacement=new):
            return _cap_like(match.group(0), replacement)

        text, hits = pattern.subn(student, text)
        counts['student'] += hits

    def iret(match):
        return ('И' if match.group(1) == 'И' else 'и') + 'рээт'

    text, hits = _IRET.subn(iret, text)
    counts['iret'] += hits

    def option_letter(match):
        letter = match.group(1) or match.group(2)
        return _OPTION_LETTER[letter] + ')'

    text, hits = _OPTION_RE.subn(option_letter, text)
    counts['option'] += hits
    if text != original and _FOREIGN.search(text) and not _FOREIGN.search(original):
        raise ValueError('rewrite introduced a non-Kyrgyz letter')
    counts['total'] = sum(value for key, value in counts.items() if key != 'total')
    return text, counts


def apply_kyrgyz_wording(text):
    """Teacher-facing sentences. Digits in code, URLs and CSS are left alone."""
    counts = empty_counts()
    updated = _apply_joined(text, counts, numbers=False)
    counts['total'] = sum(value for key, value in counts.items() if key != 'total')
    return updated, counts


def apply_kyrgyz_runs(texts):
    """Return new run strings and per-group counts.

    The joined paragraph is edited, then the new characters are written
    back onto the runs that held the old ones. A match split across runs
    keeps its tail on the last run.
    """
    counts = {
        'safe': 0, 'thousands': 0, 'iret': 0, 'student': 0,
        'rewrite': 0, 'decimal': 0, 'latin': 0, 'solve': 0, 'option': 0,
    }
    joined = ''.join(texts)
    updated = _apply_joined(joined, counts)
    total = sum(counts.values())
    counts['total'] = total
    if updated == joined:
        return list(texts), counts
    if len(texts) == 1:
        return [updated], counts
    return _redistribute(texts, updated), counts


def paragraph_texts(xml):
    import html
    found = []
    for para in _A_P.finditer(xml):
        runs = [html.unescape(item) for item in _A_T.findall(para.group(1))]
        if runs:
            found.append(''.join(runs))
    return found


def empty_counts():
    return {
        'safe': 0, 'thousands': 0, 'iret': 0, 'student': 0,
        'rewrite': 0, 'decimal': 0, 'latin': 0, 'solve': 0, 'option': 0, 'total': 0,
    }


def load_manifest():
    return json.loads(_MANIFEST.read_text(encoding='utf-8'))


def refresh_prose_media(media_root):
    """Rewrite volume decks whose bytes are still the pre-prose hash."""
    from apps.resources.deck_text import refresh_one

    manifest = json.loads(_PROSE_MANIFEST.read_text(encoding='utf-8'))
    totals = {'updated': 0, 'already': 0, 'missing': 0, 'foreign': 0, 'rejected': 0}
    root = Path(media_root)
    for relative, entry in manifest.items():
        outcome = refresh_one(root / relative, entry)
        totals[outcome] += 1
    print('kyrgyz prose: ' + ' '.join(f'{name}={count}' for name, count in totals.items()))
    return totals


def refresh_kyrgyz_media(media_root):
    from apps.resources.deck_text import refresh_one

    manifest = load_manifest()
    totals = {'updated': 0, 'already': 0, 'missing': 0, 'foreign': 0, 'rejected': 0}
    root = Path(media_root)
    for relative, entry in manifest.items():
        outcome = refresh_one(root / relative, entry)
        totals[outcome] += 1
    print('kyrgyz text: ' + ' '.join(f'{name}={count}' for name, count in totals.items()))
    return totals
