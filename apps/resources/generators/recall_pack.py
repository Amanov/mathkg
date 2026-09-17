"""Generates parameterized "recall / retrieval practice" worksheet packs.

Structural format (grid of short mixed-topic questions, each worth a small
number of marks, with a matching answer-key page) is a generic, widely used
worksheet layout, not tied to any particular publisher. All question
scenarios, numbers and Kyrgyz wording here are authored fresh for this
project - nothing is translated from a third-party source - which is also
what makes a single pack regenerable into many number-varied variants
(1A, 1B, 1C, ...) via the `seed` argument.

Kyrgyz-specific care taken throughout:
- Case/possessive suffixes are always attached to a real Kyrgyz noun
  (сом, мм, маани, сызык...), never glued directly onto a bare digit, since
  suffix vowel-harmony on a raw numeral is genuinely ambiguous in writing.
- Decimals use a comma (Kyrgyz/European convention), never a dot.
- Word problems keep the verb at the end of the clause (SOV) instead of
  the buried-at-the-end-of-a-translated-sentence feel of a literal
  English->Kyrgyz translation.
"""
import random

NAMES = [
    "Айгерим", "Нурбек", "Айжан", "Бекзат", "Салтанат",
    "Азамат", "Гүлнара", "Мирлан", "Асель", "Данияр",
    "Элмира", "Тынчтык",
]

FOOD_ITEMS = ["самса", "пирожок", "бургер", "манты"]
DRINK_ITEMS = ["чай", "компот", "сок", "лимонад"]
PIECE_ITEMS = ["печенье", "мандарин", "конфет", "кант"]

COMBO_FOODS = ["самса", "лагман", "плов", "манты", "куурдак"]
COMBO_DRINKS = ["чай", "компот", "сок", "айран"]

SERIES_TITLE = "ЭСТЕ САКТОО БАРАКЧАСЫ"
SUBJECT_LINE = "Аралаш кайталоо - 5-6-класс"


def fmt_num(x):
    """Kyrgyz-style number formatting: comma decimal separator, no
    trailing .0 for whole numbers."""
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer()):
        return str(int(x))
    text = f"{x:.2f}".rstrip("0").rstrip(".")
    return text.replace(".", ",")


def _q1_money(rng):
    name = rng.choice(NAMES)
    item_a = rng.choice(FOOD_ITEMS)
    item_b = rng.choice(DRINK_ITEMS)
    item_c = rng.choice(PIECE_ITEMS)
    price_a = rng.randrange(30, 71, 5)
    price_b = rng.randrange(10, 31, 5)
    price_c = rng.randrange(5, 16, 5)
    qty_c = rng.choice([2, 3])
    total = price_a + price_b + qty_c * price_c
    paid = rng.choice([200, 500, 1000])
    while paid <= total:
        paid = paid * 2
    change = paid - total

    prompt = (
        f"{name} дүкөндөн {price_a} сомго {item_a}, {price_b} сомго {item_b} "
        f"жана {price_c} сомдон {qty_c} {item_c} сатып алды. Ал кассага {paid} сом берди. "
        f"Канча сом кайтарым берилиши керек?"
    )
    return {
        "topic": "Акча эсеби",
        "marks": 2,
        "prompt": prompt,
        "answer": f"{change} сом",
    }


def _q2_multiply(rng):
    a = rng.randint(12, 89)
    b = rng.randint(12, 89)
    return {
        "topic": "Көбөйтүү",
        "marks": 3,
        "prompt": f"{a} × {b} эсепте.",
        "answer": fmt_num(a * b),
    }


def _q3_divide(rng):
    b = rng.randint(11, 25)
    q = rng.randint(11, 40)
    a = b * q
    return {
        "topic": "Бөлүү",
        "marks": 2,
        "prompt": f"{a} ÷ {b} эсепте.",
        "answer": fmt_num(q),
    }


def _q4_combinations(rng):
    foods = rng.sample(COMBO_FOODS, 3)
    drinks = rng.sample(COMBO_DRINKS, 2)
    price = rng.randrange(80, 161, 10)
    combos = [f"{f} + {d}" for f in foods for d in drinks]
    prompt = (
        f"Мектептин ашканасында {price} сомго 1 тамак жана 1 суусундук тандаса болот.<br>"
        f"Тамактар: {', '.join(foods)}.<br>"
        f"Суусундуктар: {', '.join(drinks)}.<br>"
        f"Тамак менен суусундуктун болушу мүмкүн болгон бардык айкалыштарын жазгыла."
    )
    return {
        "topic": "Айкалыштар",
        "marks": 2,
        "prompt": prompt,
        "answer": "; ".join(combos),
    }


def _q5_percent(rng):
    tenths = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    decimal = tenths / 10
    percent = rng.choice([15, 24, 35, 46, 62, 78, 84, 95])
    prompt = (
        f"а) {fmt_num(decimal)} санын пайызга айландыр.<br>"
        f"б) {percent}% санын ондук бөлчөккө айландыр."
    )
    answer = f"а) {int(decimal * 100)}%   б) {fmt_num(percent / 100)}"
    return {
        "topic": "Пайыз жана ондук бөлчөк",
        "marks": 2,
        "prompt": prompt,
        "answer": answer,
    }


def _q6_ordering_error(rng):
    n = 7
    start = rng.randint(20, 40)
    values = [start]
    for _ in range(n - 1):
        values.append(values[-1] + rng.randint(2, 6))
    i, j = rng.sample(range(2, n - 2), 2) if n > 5 else (1, n - 2)
    i, j = sorted((i, j))
    if j - i < 2:
        j = min(i + 2, n - 1)
    values[i], values[j] = values[j], values[i]
    seq_text = ", ".join(str(v) for v in values)
    swapped_vals = sorted([values[j], values[i]])
    prompt = (
        f"Мугалим {n} окуучунун упайын өсүү тартибинде "
        f"жайгаштырды:<br><strong>{seq_text}</strong><br>"
        f"Тартипти бузган эки санды тапкыла."
    )
    return {
        "topic": "Ой жүгүртүү (статистика)",
        "marks": 2,
        "prompt": prompt,
        "answer": " жана ".join(str(v) for v in swapped_vals),
    }


def _q7_bounds(rng):
    length = rng.randint(40, 95)
    prompt = (
        f"Жиптин узундугу эң жакын сантиметрге чейин тегеректелгенде {length} см чыкты.<br>"
        f"а) Анын болушу мүмкүн болгон эң аз узундугун жазгыла.<br>"
        f"б) Анын болушу мүмкүн болгон эң чоң узундугун жазгыла."
    )
    answer = f"а) {fmt_num(length - 0.5)} см   б) {fmt_num(length + 0.5)} см"
    return {
        "topic": "Тегеректөө чектери",
        "marks": 2,
        "prompt": prompt,
        "answer": answer,
    }


def _q8_units(rng):
    mm = rng.choice([15, 25, 45, 65, 85, 95])
    m = rng.choice([2, 3, 4, 5, 6, 7])
    prompt = (
        f"а) {mm} мм-ди сантиметрге айландыр.<br>"
        f"б) {m} м-ди сантиметрге айландыр."
    )
    answer = f"а) {fmt_num(mm / 10)} см   б) {m * 100} см"
    return {
        "topic": "Бирдик которуу",
        "marks": 2,
        "prompt": prompt,
        "answer": answer,
    }


def _q9_powers(rng):
    n, m = rng.sample(range(2, 99), 2)
    prompt = f"а) {n}⁰ маанисин жаз.<br>б) {m}⁰ маанисин жаз."
    return {
        "topic": "Даражалар",
        "marks": 2,
        "prompt": prompt,
        "answer": "а) 1   б) 1",
    }


def _q10_sequence(rng):
    a = rng.randint(2, 9)
    d = rng.randint(2, 6)
    terms = [a + k * d for k in range(5)]
    next_two = [a + 5 * d, a + 6 * d]
    prompt = (
        "Ырааттуулуктун кийинки эки санын тап:<br>"
        f"<strong>{', '.join(str(t) for t in terms)}, ___, ___</strong>"
    )
    return {
        "topic": "Ырааттуулук",
        "marks": 2,
        "prompt": prompt,
        "answer": ", ".join(str(t) for t in next_two),
    }


def _q11_reflection(rng):
    mirror_x = rng.choice([-1, 0, 1])
    side = rng.choice([-1, 1])
    base_x = mirror_x + side * rng.randint(2, 3)
    dx = side * rng.randint(1, 2)
    points = [
        (base_x, rng.randint(-3, 0)),
        (base_x + dx, rng.randint(1, 3)),
        (base_x + 2 * dx, rng.randint(-3, 0)),
    ]
    reflected = [(2 * mirror_x - x, y) for x, y in points]
    prompt = (
        f"A үч бурчтугун x = {mirror_x} сызыгына карата чагылдыр.<br>"
        f"Жаңы сүрөттү тартып, аны A' деп белгиле."
    )
    return {
        "topic": "Чагылдыруу (геометрия)",
        "marks": 2,
        "prompt": prompt,
        "answer": "Сүрөттү карагыла (жооп баракчасы)",
        "svg_points": points,
        "svg_reflected": reflected,
        "svg_mirror_x": mirror_x,
    }


_BUILDERS = [
    _q1_money, _q2_multiply, _q3_divide, _q4_combinations, _q5_percent,
    _q6_ordering_error, _q7_bounds, _q8_units, _q9_powers, _q10_sequence,
    _q11_reflection,
]

_CIRCLED_DIGITS = "①②③④⑤⑥⑦⑧⑨⑩⑪"


def generate_pack(seed=None, pack_code="1-А"):
    """Builds one full recall pack: 11 questions, each with fresh randomly
    parameterized numbers/names/scenarios (never the same worksheet twice
    unless the same seed is reused), ready to render to PDF or PPTX."""
    rng = random.Random(seed)
    questions = []
    for i, builder in enumerate(_BUILDERS):
        q = builder(rng)
        q["number"] = i + 1
        q["circled"] = _CIRCLED_DIGITS[i]
        questions.append(q)

    total_marks = sum(q["marks"] for q in questions)
    return {
        "series_title": SERIES_TITLE,
        "subject_line": SUBJECT_LINE,
        "pack_code": pack_code,
        "total_marks": total_marks,
        "questions": questions,
    }
