"""Explanation lesson: from a bar model to x.

One fixed deck for the «Тилкеден x ке» page. Colours, stripe, Golos Text
and the footer match the house lesson slides. Maths runs are italic.
"""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

SLIDE_W = 12191695
SLIDE_H = 6858000
FONT = 'Golos Text'

NAVY = RGBColor(0x1D, 0x35, 0x57)
BLUE = RGBColor(0x24, 0x41, 0x8C)
GREEN = RGBColor(0x00, 0x7A, 0x5A)
ORANGE = RGBColor(0xA8, 0x44, 0x00)
MUTED = RGBColor(0x4A, 0x5A, 0x70)
FOOT = RGBColor(0x8D, 0x99, 0xAA)
PALE = RGBColor(0xF3, 0xF5, 0xFB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1F, 0x24, 0x30)

FOOTER = 'MathKG · Математика кыргызча'
CRUMB = 'Алгебра · Киришүү'
TOPIC = 'Тилкеден x ке'
NEXT_URL = 'https://www.mathkg.com/algebra-intro-definitions/'
EMAIL = 'mathematicskgz@gmail.com'


def build_lesson():
    prs = Presentation()
    prs.slide_width = Emu(SLIDE_W)
    prs.slide_height = Emu(SLIDE_H)
    prs.core_properties.title = TOPIC
    blank = prs.slide_layouts[6]
    slides = [
        _title,
        _recap,
        _engage,
        _explore,
        _bar_model,
        _worked,
        _levels,
        _practice_easy,
        _practice_mid,
        _practice_hard,
        _check,
        _next_lesson,
        _feedback,
    ]
    for build in slides:
        slide = prs.slides.add_slide(blank)
        _blank(slide)
        build(slide)
    return prs


def _blank(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.fill.background()
    _quiet(shape)


def _quiet(shape):
    shape.shadow.inherit = False


def _box(slide, x, y, w, h, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.adjustments[0] = 0.08
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1.25)
    _quiet(shape)
    return shape


def _rect(slide, x, y, w, h, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    _quiet(shape)
    return shape


def _text(slide, x, y, w, h, content, size=20, bold=False, color=INK,
          align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """content is a string or a list of (text, italic) pairs."""
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.paragraphs[0].alignment = align
    box.text_frame.paragraphs[0].space_after = Pt(0)
    try:
        tf._txBody.bodyPr.set('anchor', {MSO_ANCHOR.TOP: 't', MSO_ANCHOR.MIDDLE: 'ctr', MSO_ANCHOR.BOTTOM: 'b'}[anchor])
    except Exception:
        pass
    if isinstance(content, str):
        content = [(content, False)]
    paragraph = tf.paragraphs[0]
    paragraph.alignment = align
    paragraph.clear()
    for text, italic in content:
        run = paragraph.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.name = FONT
        run.font.color.rgb = color
    return box


def _lines(slide, x, y, w, h, lines, size=22, color=INK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for index, line in enumerate(lines):
        paragraph = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        paragraph.alignment = align
        paragraph.space_after = Pt(8)
        if isinstance(line, str):
            line = [(line, False)]
        for text, italic in line:
            run = paragraph.add_run()
            run.text = text
            run.font.size = Pt(size)
            run.font.bold = False
            run.font.italic = italic
            run.font.name = FONT
            run.font.color.rgb = color
    return box


def _chrome(slide, title):
    _rect(slide, 365760, 228600, 11460175, 640080, WHITE)
    stripe_y, stripe_h, stripe_w = 369417, 358444, 70408
    for dx, color in ((557784, GREEN), (691560, ORANGE), (825337, BLUE)):
        _rect(slide, dx, stripe_y, stripe_w, stripe_h, color)
    _text(slide, 1087130, 300000, 5200000, 500000, title, size=28, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    _text(slide, 6400000, 300000, 5200000, 500000, CRUMB, size=16, color=MUTED, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    _text(slide, 365760, 6492240, 6876105, 274320, FOOTER, size=12, color=FOOT, anchor=MSO_ANCHOR.MIDDLE)
    _text(slide, 6095847, 6492240, 5600000, 274320, TOPIC, size=12, color=FOOT, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def _eq(text):
    return [(text, True)]


def _title(slide):
    _chrome(slide, 'Сабак')
    _text(slide, 700000, 1200000, 10800000, 900000, TOPIC, size=48, bold=True, color=NAVY)
    _text(slide, 700000, 2100000, 10800000, 500000, 'Түшүндүрмө сабак', size=26, color=GREEN)
    _box(slide, 700000, 2900000, 10700000, 3200000, PALE)
    _text(slide, 980000, 3100000, 10000000, 400000, 'Мугалим үчүн', size=18, bold=True, color=BLUE)
    _lines(slide, 980000, 3600000, 10000000, 2200000, [
        '•  Окуучу тилкедеги «?» ордуна x жазат.',
        '•  Адегенде тилке, анан теңдеме. Экөө бир эле санды берет.',
        '•  Жеңилден оорго чейин машыгып, анан текшерет.',
        '•  Кийинки сабак — Аныктамалар.',
    ], size=22, color=NAVY)


def _recap(slide):
    _chrome(slide, 'Кайталоо')
    _lines(slide, 700000, 1200000, 10800000, 1800000, [
        'Тилке — тик бурчтук.',
        'Узун тилке бүтүндү көрсөтөт. Кыска тилкелер анын бөлүктөрү.',
        '«?» — азырынча билбеген сан.',
    ], size=24, color=NAVY)
    _bar_row(slide, 900000, 3400000, [
        (3200000, GREEN, '5'),
        (4200000, ORANGE, '?'),
    ], 700000)
    _text(slide, 700000, 4500000, 10800000, 500000, _eq('5 + ? = 12'), size=32, color=NAVY, align=PP_ALIGN.CENTER)
    _text(slide, 700000, 5200000, 10800000, 500000, 'Бүтүн 12. Бир бөлүгү белгилүү, экинчиси жок.', size=20, color=MUTED, align=PP_ALIGN.CENTER)


def _engage(slide):
    _chrome(slide, 'Кызыктыруу')
    _box(slide, 700000, 1300000, 10700000, 4600000, PALE)
    _lines(slide, 1000000, 1600000, 10100000, 3600000, [
        'Айгеримдин 3 бирдей кутусу бар.',
        'Ар бир кутуда бирдей санда алма.',
        'Үстөлдө дагы 5 алма турат.',
        'Баары 26 алма.',
        '',
        'Бир кутуда канча алма?',
    ], size=28, color=NAVY)


def _explore(slide):
    _chrome(slide, 'Изилдөө')
    _text(slide, 700000, 1150000, 10800000, 400000, 'Бир маселе. Эки жол.', size=24, color=NAVY)
    _box(slide, 600000, 1750000, 5300000, 4300000, PALE)
    _box(slide, 6200000, 1750000, 5300000, 4300000, PALE)
    _text(slide, 800000, 1950000, 4900000, 400000, 'Арифметика', size=22, bold=True, color=GREEN)
    _text(slide, 6400000, 1950000, 4900000, 400000, 'Теңдеме', size=22, bold=True, color=ORANGE)
    _lines(slide, 800000, 2600000, 4900000, 2800000, [
        _eq('26 − 5 = 21'),
        _eq('21 : 3 = 7'),
        'Бир кутуда 7 алма.',
    ], size=26, color=NAVY)
    _lines(slide, 6400000, 2600000, 4900000, 2800000, [
        _eq('3x + 5 = 26'),
        'x — бир куту.',
        'Жооп дагы 7.',
    ], size=26, color=NAVY)


def _bar_model(slide):
    _chrome(slide, 'Тилке модели')
    _text(slide, 700000, 1100000, 10800000, 400000, 'Үч бирдей куту жана дагы 5 алма. Бүтүнү 26.', size=22, color=NAVY)
    _bar_row(slide, 900000, 1900000, [
        (2400000, GREEN, 'x'),
        (2400000, GREEN, 'x'),
        (2400000, GREEN, 'x'),
        (1800000, ORANGE, '5'),
    ], 780000)
    _text(slide, 900000, 2850000, 9600000, 300000, 'бөлүктөр', size=14, color=MUTED, align=PP_ALIGN.CENTER)
    _bar_row(slide, 900000, 3400000, [
        (9000000, BLUE, '26'),
    ], 780000)
    _text(slide, 900000, 4300000, 9600000, 300000, 'бүтүн', size=14, color=MUTED, align=PP_ALIGN.CENTER)
    _text(slide, 700000, 5000000, 10800000, 500000, _eq('3x + 5 = 26'), size=36, color=NAVY, align=PP_ALIGN.CENTER)


def _worked(slide):
    _chrome(slide, 'Чыгарылган мисал')
    _lines(slide, 900000, 1300000, 7000000, 4600000, [
        _eq('3x + 5 = 26'),
        _eq('3x = 26 − 5'),
        _eq('3x = 21'),
        _eq('x = 21 : 3'),
        _eq('x = 7'),
    ], size=32, color=NAVY)
    _box(slide, 8000000, 1800000, 3400000, 3600000, PALE)
    _lines(slide, 8200000, 2400000, 3000000, 2000000, [
        'Бир кутуда',
        '7 алма.',
    ], size=28, color=GREEN, align=PP_ALIGN.CENTER)


def _levels(slide):
    _chrome(slide, 'Деңгээлдер')
    cards = [
        (700000, GREEN, 'Жеңил', 'Бир амал', _eq('x + 4 = 9')),
        (4500000, ORANGE, 'Орто', 'Эки амал, ондук', _eq('2x + 1,5 = 7,5')),
        (8300000, BLUE, 'Оор', 'Чоң сан', _eq('2x + 1 500 = 70 000')),
    ]
    for x, color, name, note, equation in cards:
        _box(slide, x, 1600000, 3200000, 4000000, PALE)
        _rect(slide, x, 1600000, 3200000, 180000, color)
        _text(slide, x + 160000, 2000000, 2880000, 500000, name, size=28, bold=True, color=color)
        _text(slide, x + 160000, 2600000, 2880000, 400000, note, size=18, color=MUTED)
        _text(slide, x + 160000, 3400000, 2880000, 1400000, equation, size=22, color=NAVY)


def _practice_easy(slide):
    _practice(slide, 'Машыгуу · Жеңил', GREEN, [
        (_eq('1.   x + 4 = 9'), 'x = 5'),
        (_eq('2.   x − 3 = 6'), 'x = 9'),
        (_eq('3.   2x = 10'), 'x = 5'),
    ])


def _practice_mid(slide):
    _practice(slide, 'Машыгуу · Орто', ORANGE, [
        (_eq('1.   2x + 1,5 = 7,5'), 'x = 3'),
        (_eq('2.   3x − 0,5 = 5,5'), 'x = 2'),
        (_eq('3.   x + 2,5 = 6'), 'x = 3,5'),
    ])


def _practice_hard(slide):
    _practice(slide, 'Машыгуу · Оор', BLUE, [
        (_eq('1.   2x + 1 500 = 70 000'), 'x = 34 250'),
        (_eq('2.   x + 12 000 = 70 000'), 'x = 58 000'),
        (_eq('3.   4x = 70 000'), 'x = 17 500'),
    ])


def _practice(slide, title, color, rows):
    _chrome(slide, title)
    _rect(slide, 700000, 1150000, 280000, 280000, color)
    y = 1600000
    for equation, answer in rows:
        _text(slide, 800000, y, 7000000, 500000, equation, size=28, color=NAVY)
        _text(slide, 8000000, y, 3400000, 500000, answer, size=28, bold=True, color=GREEN)
        y += 1200000
    _text(slide, 700000, 5600000, 10800000, 400000, 'Жоопту дептерге жаз, анан оң жагы менен текшер.', size=18, color=MUTED)


def _check(slide):
    _chrome(slide, 'Текшерүү')
    _text(slide, 700000, 1150000, 10800000, 400000, 'Үч мүнөт. Кагазга жаз.', size=22, color=NAVY)
    _lines(slide, 700000, 1700000, 10800000, 2500000, [
        '1.  Тилкеде 2x жана 4 бар. Бүтүнү 18. Теңдемени жаз.',
        '2.  3x + 5 = 26 болсо, x канча?',
        '3.  2x + 1 500 = 70 000 болсо, x канча?',
    ], size=24, color=NAVY)
    _box(slide, 700000, 4500000, 10700000, 1600000, PALE)
    _text(slide, 950000, 4650000, 10200000, 300000, 'Жооп', size=16, bold=True, color=GREEN)
    _text(
        slide, 950000, 5050000, 10200000, 800000,
        _eq('1.  2x + 4 = 18      2.  x = 7      3.  x = 34 250'),
        size=22, color=NAVY,
    )


def _next_lesson(slide):
    _chrome(slide, 'Кийинки сабак')
    _text(slide, 700000, 1500000, 10800000, 500000, 'Бул сабакта x тилкедеги белгисиз сан болду.', size=24, color=NAVY)
    _text(slide, 700000, 2200000, 10800000, 500000, 'Кийинки сабакта аныктамаларды карайбыз.', size=24, color=NAVY)
    _box(slide, 700000, 3200000, 10700000, 2200000, PALE)
    _text(slide, 950000, 3450000, 10000000, 400000, 'Кийинки тема', size=16, color=MUTED)
    link = _text(slide, 950000, 3900000, 10000000, 700000, 'Аныктамалар', size=36, bold=True, color=BLUE)
    run = link.text_frame.paragraphs[0].runs[0]
    run.hyperlink.address = NEXT_URL
    _text(slide, 950000, 4700000, 10000000, 400000, 'Алгебра · Киришүү', size=18, color=MUTED)


def _feedback(slide):
    _chrome(slide, 'Пикир')
    _box(slide, 700000, 1300000, 10700000, 4800000, PALE)
    _lines(slide, 1000000, 1550000, 6200000, 2200000, [
        'Суроолор барбы?',
        'Пикирлер?',
        'Сунуштар?',
    ], size=32, color=NAVY)
    _text(slide, 1000000, 3900000, 6200000, 400000, '…же ката таптыңызбы?', size=22, color=ORANGE)
    _text(slide, 1000000, 4400000, 6200000, 400000, 'Кат жөнөтүңүз:', size=20, color=MUTED)
    _box(slide, 1000000, 5000000, 5600000, 700000, WHITE, line=BLUE)
    _text(slide, 1000000, 5100000, 5600000, 500000, EMAIL, size=22, bold=True, color=BLUE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _mini_bars(slide, 7800000, 1900000)


def _bar_row(slide, x, y, parts, height):
    gap = 120000
    cursor = x
    for width, color, label in parts:
        _rect(slide, cursor, y, width, height, color)
        _text(
            slide, cursor, y, width, height, label,
            size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        )
        cursor += width + gap


def _mini_bars(slide, x, y):
    _text(slide, x, y, 3200000, 300000, 'Тилке', size=14, color=MUTED, align=PP_ALIGN.CENTER)
    width = 900000
    gap = 80000
    top = y + 400000
    for index in range(3):
        _rect(slide, x + index * (width + gap), top, width, 420000, GREEN)
        _text(slide, x + index * (width + gap), top, width, 420000, 'x', size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _rect(slide, x, top + 560000, 3 * width + 2 * gap, 360000, ORANGE)
    _text(slide, x, top + 560000, 3 * width + 2 * gap, 360000, '5', size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _rect(slide, x, top + 1100000, 3 * width + 2 * gap, 420000, BLUE)
    _text(slide, x, top + 1100000, 3 * width + 2 * gap, 420000, '26', size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
