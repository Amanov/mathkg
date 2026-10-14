# Tarsia puzzle generator

Builds the genuine Tarsia mechanic: a big equilateral triangle subdivided
into an n-row grid of n² small triangles. Every **internal edge** (shared
by two small triangles) carries one matching pair - a question on one
triangle's side of the edge, its answer on the other triangle's side -
each oriented so it reads upright with that edge as the triangle's local
"bottom". Printed/exported, cut apart, and reassembled by matching edges.

This was derived by unpacking a real reference `.pptx`/`.pdf` Tarsia
puzzle, extracting its embedded grid image, and confirming pixel-for-pixel
that this module's rendered geometry and per-edge text rotation reproduce
the same structure. It is not a guess at the convention.

## When to use this

Any time you need a cut-and-match triangle jigsaw for a math (or other)
topic page - new content only. **Never reuse another publisher's actual
problem numbers** (see Content rules below); use this to generate your
own verified pairs and render them with the real geometry.

## Quick start

```python
import sys
sys.path.insert(0, '/home/user/mathkg/.claude/skills/tarsia-puzzle/scripts')
from build_tarsia_deck import build_tarsia_activity
from geom import edge_count

n = 4                      # grid size: n=3 -> 9 pairs, n=4 -> 18, n=5 -> 30
print(edge_count(n))       # exact number of (question, answer) pairs required

pairs = [
    ("0.3 + 0.4", "0.7"),
    ("0.8 - 0.5", "0.3"),
    # ... exactly edge_count(n) pairs total
]

out = build_tarsia_activity(
    n=n,
    pairs=pairs,
    title="Ондуктарды кошуу — Тарсия",
    usage_lines=[
        "Үч бурчтуктарды кесип, жооптору дал келгендерин жанаштырыңыз.",
        "Жуп же кичине топ менен иштесе болот.",
    ],
    out_dir="/path/to/output",
    base_name="OnduktarduKoshuuTarsia",
    closing_email="mathematicskgz@gmail.com",   # or None
)
# out == {'pptx': ..., 'pdf': ..., 'png': ...}
```

`build_tarsia_activity` needs `TARSIA_PPTXGENJS` set to a `pptxgenjs`
module path (or pass it via the environment before calling), since the
PPTX assembly shells out to Node + pptxgenjs, same as the rest of this
project's slide generation:

```bash
export TARSIA_PPTXGENJS=/path/to/node_modules/pptxgenjs
```

Output: a 3-slide PPTX (title/instructions, full-bleed puzzle image,
closing slide - no branding added beyond what you pass in), a vector PDF
of the puzzle alone (crisp at any print size), and the raw PNG.

## Content rules (copyright + correctness)

- **Never copy another source's exact numbers.** If you're working from a
  reference deck (as with the GoTeachMaths-derived files), use its
  *subject and difficulty* as a guide and write entirely new values.
- **Verify every pair programmatically before rendering** - use
  `fractions.Fraction` for fraction arithmetic, `decimal.Decimal` for
  decimals (never raw `float`, which introduces rounding error). A wrong
  pair ships a broken puzzle (no valid match exists).
- **No duplicate answers** within one puzzle, or two different questions
  could legitimately match the same triangle, breaking the "exactly one
  valid match" property. Check for collisions before rendering (dedupe,
  or require it isn't in `used_answers` as you generate).
- Strip any branding/watermarks/links if you're using a real file only as
  a *structural* reference - this skill's own output carries none.

## Picking grid size `n`

| n | triangles (n²) | internal edges (pairs needed) |
|---|---|---|
| 3 | 9  | 9  |
| 4 | 16 | 18 |
| 5 | 25 | 30 |
| 6 | 36 | 45 |

Matches the real decks' "Standard" (bigger, more problems) vs. "Small"
(fewer, quicker) pattern - e.g. generate once at n=4 for Standard and
again at n=3 with a subset of pairs for Small.

## Tuned rendering defaults

`tarsia.render_tarsia()` defaults (`s=1.8`, `fontsize=9`,
`inset_frac=0.11`) were tuned empirically to avoid text collisions where
3 pairs converge on one small triangle (an interior triangle can border
up to 3 neighbors, so it can carry up to 3 separate texts). If you change
`fontsize` or go to a larger `n` (smaller triangles per pair), re-check
for overlap - render once, read the PNG back, and look at the busiest
interior triangles before shipping.

## Files

- `scripts/geom.py` - triangular grid math: vertices of every small
  triangle, midpoint + angle of every internal edge, for a given `n`.
- `scripts/tarsia.py` - `render_tarsia(n, pairs, ...)`: draws the grid and
  places/rotates each pair's two texts correctly (matplotlib, outputs PNG
  + vector PDF).
- `scripts/build_tarsia_deck.py` - `build_tarsia_activity(...)`: wraps
  `render_tarsia` plus a 3-slide PPTX (title/instructions, puzzle image,
  closing) via Node + pptxgenjs.

## External references (unreachable from this sandbox)

The request for this tool also pointed at tarsia.ai, tarsiamaker.co.uk,
classtools.net/tarsia, mrchapmanmaths.com/tools/tarsia-generator, and a
YouTube tutorial (watch?v=K-YOXYAeDMM), to fold their conventions in.
None could be fetched - this sandbox's network policy blocks outbound
requests to hosts outside its allowlist (confirmed via repeated
`WebFetch` attempts, all `ENOTFOUND`; see the project's `CLAUDE.md` for
the same restriction noted against other reference sites). If you're
picking this up with network access, worth checking those sites for:
multi-size/difficulty export options, a "dummy edge" border convention,
and whether they support shapes beyond triangles (some Tarsia-style
tools also do rectangles/hexagons) - none of that is implemented here.
What *is* implemented was reverse-engineered directly from the real
uploaded `.pptx`/`.pdf` files instead (see above), which is why the
geometry is exact rather than approximate.

## Known limits

- This does not implement the "dummy edge" border convention some
  commercial generators use (a border edge with a value that matches
  nothing, just to vary the outline). Every internal edge here is a real,
  solvable pair; the outer boundary of the big triangle has no text.
- Designed for short text (fraction/decimal expressions, single
  operations). A long question string in a small/crowded `n=5+` grid may
  still need a bigger `s` or smaller `fontsize` - check the render.
