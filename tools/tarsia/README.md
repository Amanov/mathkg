# Tarsia puzzle generator

A big equilateral triangle split into an n-row grid of n² small triangles. Every internal edge (shared by two small triangles) carries one question/answer pair. Each string is rotated so it reads upright with that edge as its own triangle's bottom. Printed, cut apart, and reassembled by matching edges.

The geometry was checked against a real reference puzzle's embedded grid, not guessed. Three copies of that math must stay the same: `tools/tarsia/geom.py`, `apps/resources/generators/tarsia_geom.py`, and `static/js/tarsia-builder.js`.

## Site builder (what teachers use)

`/tarsia-builder/` renders `templates/resources/tarsia_builder.html`. The preview is client-side SVG (`static/js/tarsia-builder.js`). Draft pairs are stored in `localStorage` under keys prefixed `tarsiaBuilderPairs:`.

Export is `POST /tarsia-builder/export/?format=pdf` or `format=pptx` (`apps/resources/views/tarsia_builder.py`). JSON body:

| Field | Constraint |
|---|---|
| `shape` | `"triangle"` (default) or `"loop"` |
| `n` | Triangle only. Integer 3..6 |
| `count` | Loop only. Integer 4..24. This is the number of cards and of pairs |
| `pairs` | List of `[question, answer]`. Length must be `edge_count(n)` for a triangle, or `count` for a loop. Each side is stripped and cut to 60 characters. Empty sides are rejected. Answers must be unique |
| `title` | Optional, stripped, cut to 120 characters. Default `"Тарсия"` |
| `usageLines` | Optional list. Up to 6 non-empty lines, each cut to 200 characters |

A bad body returns 400 with a Kyrgyz sentence. An unknown `format` returns 400. An unexpected render error is logged and returns 500.

Triangle export shuffles which pair lands on which edge before drawing, so the sheet is not already solved. Loop export builds a random cyclic order (`build_loop_order`) and does not use that shuffle: cutting the cards apart is what scrambles the activity.

PDF is the SVG rendered by WeasyPrint (`tarsia_svg.py` or `loop_cards.py`) inside `templates/interactive/tarsia_print.html`. PPTX is native shapes from `python-pptx` (`tarsia_pptx.py`, `loop_cards.py`): a title/instructions slide, the puzzle or cards, and a closing slide whose email is `mathematicskgz@gmail.com`. The download name is the ASCII letters and digits of the title, or `Tarsia`, plus `_Tarsia.pptx` / `_Tarsia.pdf`.

Server entry points:

```python
from apps.resources.generators.tarsia_geom import edge_count
from apps.resources.generators.tarsia_pptx import build_tarsia_pptx
from apps.resources.generators.tarsia_svg import build_tarsia_svg
from apps.resources.generators.loop_cards import build_loop_cards_pptx, build_loop_cards_svg, build_loop_order

n = 4
print(edge_count(n))  # 18
pairs = [
    ("0.3 + 0.4", "0.7"),
    ("0.8 - 0.5", "0.3"),
    # ... 16 more pairs; 18 total, every answer unique
]

buf = build_tarsia_pptx(
    n, pairs, "Ондуктарды кошуу — Тарсия",
    ["Үч бурчтуктарды кесип, жооптору дал келгендерин жанаштырыңыз."],
)
svg = build_tarsia_svg(n, pairs)  # defaults: s=1.8, font_size=9, inset_frac=0.11
```

`build_tarsia_pptx` returns a `BytesIO`. It does not check pair count; pass `edge_count(n)` pairs. The view is what enforces the limits above.

Menu row: `python manage.py add_tarsia_builder_menu_link` creates or updates the "Тарсия куруучу" item pointing at `tarsia_builder`. Safe to re-run.

## Offline generator

`tools/tarsia/` is the original matplotlib + pptxgenjs batch tool. The site builder does not call it. Matplotlib is not in `requirements.txt`. PPTX assembly needs Node and `TARSIA_PPTXGENJS` set to a `pptxgenjs` module path.

```python
import sys
sys.path.insert(0, "tools/tarsia")
from build_tarsia_deck import build_tarsia_activity
from geom import edge_count

n = 4
print(edge_count(n))  # 18
pairs = [
    ("0.3 + 0.4", "0.7"),
    ("0.8 - 0.5", "0.3"),
    # ... 16 more pairs; 18 total, every answer unique
]

out = build_tarsia_activity(
    n=n,
    pairs=pairs,
    title="Ондуктарды кошуу — Тарсия",
    usage_lines=["Үч бурчтуктарды кесип, жооптору дал келгендерин жанаштырыңыз."],
    out_dir="/path/to/output",
    base_name="OnduktarduKoshuuTarsia",
    closing_email="mathematicskgz@gmail.com",  # or None
)
# out == {"pptx": ..., "pdf": ..., "png": ...}
```

Wrong pair count raises `ValueError`. Output is a 3-slide PPTX (title, full-bleed puzzle image, closing), a vector PDF of the puzzle, and `{base_name}_puzzle.png`. `render_tarsia` defaults are `s=1.8`, `fontsize=9`, `inset_frac=0.11`. Those were tuned so three texts can share one interior triangle. A larger `n` or a longer string needs a visual check of the busiest interior triangles.

This tool does not shuffle pairs and does not reject duplicate answers. Do that before calling it.

## Loop cards

Second shape on the builder, implemented in `apps/resources/generators/loop_cards.py`. Pieces are rectangles. For a permutation `order` of the pairs, card `k` shows `answer[order[k]]` on the left and `question[order[(k+1) % N]]` on the right. Solving the right-hand question leads to the card whose left side is that answer, once around the loop and back to the start.

## Content rules

- Write new numbers. A reference deck is a guide for subject and difficulty only.
- Check every pair before rendering. Use `fractions.Fraction` or `decimal.Decimal`. A wrong pair has no valid match.
- Keep answers unique inside one puzzle. Two questions with the same answer both match the same edge.

## Grid size

Internal edges = `3n(n-1)/2`, which is what `edge_count` returns.

| n | Triangles (n²) | Pairs |
|---|---|---|
| 3 | 9 | 9 |
| 4 | 16 | 18 |
| 5 | 25 | 30 |
| 6 | 36 | 45 |

The builder stops at n=6. The offline `edge_count` accepts larger n; text collision gets worse as the triangles shrink.

## Files

- `tools/tarsia/geom.py` — original grid math.
- `tools/tarsia/tarsia.py` — matplotlib PNG + PDF.
- `tools/tarsia/build_tarsia_deck.py` — PNG/PDF plus a pptxgenjs deck.
- `apps/resources/generators/tarsia_geom.py` — server copy of the grid math.
- `apps/resources/generators/tarsia_svg.py` — SVG for the PDF path. Defaults match the matplotlib renderer (`s=1.8`, `font_size=9`, `inset_frac=0.11`).
- `apps/resources/generators/tarsia_pptx.py` — editable triangle shapes, not a placed PNG.
- `apps/resources/generators/loop_cards.py` — loop-card SVG and PPTX.
- `static/js/tarsia-builder.js` — live preview. Same vertex and edge construction as `tarsia_geom.py`.

## Known limits

- Outer edges carry no text. There is no "dummy edge" border value.
- The site builder rejects a side longer than 60 characters. The offline renderer will draw a longer string and may overlap.
- Loop cards are on the site builder only. `tools/tarsia/` builds triangles.
