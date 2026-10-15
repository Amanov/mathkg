"""'Loop cards' (chain/domino-style matching activity) - a second shape for
the Tarsia builder, much simpler geometrically than the triangle jigsaw
since pieces are plain rectangles with no rotation.

Given N (question, answer) pairs, picks a random cyclic order and builds N
cards where card k shows:
  left  = the ANSWER to a pair that is NOT its own right-hand question
  right = a QUESTION

Specifically, for a random permutation `order` of 0..N-1:
  card k = { left: answer[order[k]], right: question[order[(k+1) % N]] }

A student solves the right-hand question, finds the card whose left side
shows that answer, and moves to it - working through every card exactly
once and returning to the start. This is the standard "loop cards" /
"round robin" review format (distinct from Tarsia's edge-matching, and
needs no shuffling step before cutting - unlike the triangle jigsaw,
cutting a loop-card sheet apart and handing cards to different students
already scrambles the activity, since nothing here depends on two pieces
having been printed adjacently).
"""
import io
import random

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Pt

INK = '#1F2A44'
MUTED = '#5B6472'
AMBER = '#F2A33F'
WHITE = '#FFFFFF'


def build_loop_order(n_pairs, rng=None):
    rng = rng or random
    order = list(range(n_pairs))
    rng.shuffle(order)
    return order


def _cards_from_order(pairs, order):
    n = len(pairs)
    cards = []
    for k in range(n):
        left = pairs[order[k]][1]
        right = pairs[order[(k + 1) % n]][0]
        cards.append((left, right))
    return cards


def build_loop_cards_svg(pairs, order=None, cols=3, card_w=260, card_h=90, gap=14, px_pad=16):
    order = order if order is not None else build_loop_order(len(pairs))
    cards = _cards_from_order(pairs, order)
    n = len(cards)
    rows = (n + cols - 1) // cols
    width = cols * card_w + (cols - 1) * gap + 2 * px_pad
    height = rows * card_h + (rows - 1) * gap + 2 * px_pad

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">'
    ]
    for i, (left, right) in enumerate(cards):
        col = i % cols
        row = i // cols
        x = px_pad + col * (card_w + gap)
        y = px_pad + row * (card_h + gap)
        mid = x + card_w * 0.38
        parts.append(f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="8" fill="none" stroke="{INK}" stroke-width="2"/>')
        parts.append(f'<line x1="{mid}" y1="{y}" x2="{mid}" y2="{y + card_h}" stroke="{INK}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x + (mid - x) / 2}" y="{y + 20}" text-anchor="middle" font-size="10" fill="{MUTED}">Жообу</text>')
        parts.append(_wrapped_text(x + (mid - x) / 2, y + card_h / 2 + 8, str(left), 15, (mid - x - 10), bold=True, anchor='middle'))
        parts.append(f'<text x="{mid + (x + card_w - mid) / 2}" y="{y + 20}" text-anchor="middle" font-size="10" fill="{MUTED}">Суроосу</text>')
        parts.append(_wrapped_text(mid + (x + card_w - mid) / 2, y + card_h / 2 + 8, str(right), 13, (x + card_w - mid - 10), anchor='middle'))
    parts.append('</svg>')
    return ''.join(parts)


def _wrapped_text(cx, cy, text, font_size, max_w, bold=False, anchor='middle'):
    # Single-line, best-effort: shrink font for long strings rather than
    # implement full text wrapping in raw SVG.
    approx_char_w = font_size * 0.58
    max_chars = max(4, int(max_w / approx_char_w))
    if len(text) > max_chars:
        font_size = max(9, int(font_size * max_chars / len(text)))
    weight = 'bold' if bold else 'normal'
    safe = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'<text x="{cx}" y="{cy}" text-anchor="{anchor}" font-size="{font_size}" font-weight="{weight}" fill="{INK}">{safe}</text>'


def build_loop_cards_pptx(pairs, title, usage_lines, order=None,
                           closing_lines=('Суроолор барбы?', 'Сунуштар?'),
                           closing_email=None):
    order = order if order is not None else build_loop_order(len(pairs))
    cards = _cards_from_order(pairs, order)

    SLIDE_W, SLIDE_H = Emu(12192000), Emu(6858000)
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    ink = RGBColor(0x1F, 0x2A, 0x44)
    muted = RGBColor(0x5B, 0x64, 0x72)
    white = RGBColor(0xFF, 0xFF, 0xFF)

    s = prs.slides.add_slide(prs.slide_layouts[6])
    box = s.shapes.add_textbox(Emu(540000), Emu(450000), Emu(11100000), Emu(1000000))
    p = box.text_frame.paragraphs[0]
    p.text = title
    p.font.size, p.font.bold, p.font.color.rgb = Pt(28), True, ink
    box2 = s.shapes.add_textbox(Emu(540000), Emu(1620000), Emu(11100000), Emu(2000000))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    for i, line in enumerate(usage_lines):
        pp = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        pp.text = line
        pp.font.size, pp.font.color.rgb = Pt(15), muted

    per_slide = 8
    cols = 4
    card_w, card_h = Emu(2700000), Emu(1200000)
    gap = Emu(180000)
    left0, top0 = Emu(540000), Emu(650000)

    for start in range(0, len(cards), per_slide):
        chunk = cards[start:start + per_slide]
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        for i, (left_txt, right_txt) in enumerate(chunk):
            col, row = i % cols, i // cols
            x = left0 + col * (card_w + gap)
            y = top0 + row * (card_h + gap)
            rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, card_w, card_h)
            rect.fill.background()
            rect.line.color.rgb = ink
            rect.line.width = Pt(1.5)
            rect.shadow.inherit = False
            half = Emu(int(card_w * 0.4))
            _loop_cell(slide, x, y, half, card_h, 'Жообу', left_txt, ink, muted, bold=True)
            _loop_cell(slide, Emu(x + half), y, Emu(card_w - half), card_h, 'Суроосу', right_txt, ink, muted, bold=False)

    closing = prs.slides.add_slide(prs.slide_layouts[6])
    closing.background.fill.solid()
    closing.background.fill.fore_color.rgb = ink
    cbox = closing.shapes.add_textbox(Emu(720000), Emu(1800000), Emu(10550000), Emu(1450000))
    for i, line in enumerate(closing_lines):
        pp = cbox.text_frame.paragraphs[0] if i == 0 else cbox.text_frame.add_paragraph()
        pp.text = line
        pp.font.size, pp.font.bold, pp.font.color.rgb = Pt(30), True, white
    if closing_email:
        ebox = closing.shapes.add_textbox(Emu(720000), Emu(3420000), Emu(10550000), Emu(540000))
        ep = ebox.text_frame.paragraphs[0]
        ep.text = closing_email
        ep.font.size, ep.font.color.rgb = Pt(14), RGBColor(0xC7, 0xD2, 0xE8)

    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf


def _loop_cell(slide, x, y, w, h, label, value, ink, muted, bold):
    label_box = slide.shapes.add_textbox(x, y, w, Emu(300000))
    label_box.text_frame.margin_top = 0
    lp = label_box.text_frame.paragraphs[0]
    lp.alignment = PP_ALIGN.CENTER
    lp.text = label
    lp.font.size, lp.font.color.rgb = Pt(10), muted

    val_box = slide.shapes.add_textbox(x, Emu(y + 300000), w, Emu(h - 300000))
    val_box.text_frame.word_wrap = True
    vp = val_box.text_frame.paragraphs[0]
    vp.alignment = PP_ALIGN.CENTER
    vp.text = str(value)
    vp.font.size, vp.font.bold, vp.font.color.rgb = Pt(14 if bold else 12), bold, ink
