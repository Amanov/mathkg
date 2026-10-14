"""Renders a Tarsia triangle jigsaw as inline SVG for the print/PDF path
(WeasyPrint). Mirrors static/js/tarsia-builder.js's renderSVG() exactly so
the PDF matches what the teacher saw in the live preview - see
tarsia_geom.py for the shared geometry.
"""
import html

from .tarsia_geom import (
    SQRT3,
    internal_edges,
    text_rotation,
    triangle_centroid,
    triangle_vertices,
)

INK = '#1F2A44'
_SCALE = 100


def build_tarsia_svg(n, pairs, s=1.8, font_size=9, inset_frac=0.11,
                      stroke_width=2, margin=0.2, px_size=760):
    tris = triangle_vertices(n, s)
    edges = internal_edges(n, s)
    width = n * s + 2 * margin
    height = n * s * SQRT3 / 2 + 2 * margin

    def tx(x):
        return (x + width / 2) * _SCALE

    def ty(y):
        return (y + margin) * _SCALE

    parts = [
        f'<svg viewBox="0 0 {width * _SCALE:.1f} {height * _SCALE:.1f}" '
        f'width="{px_size}" height="{px_size * height / width:.0f}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">'
    ]

    for verts in tris.values():
        d = (
            f'M {tx(verts[0][0]):.1f} {ty(verts[0][1]):.1f} '
            f'L {tx(verts[1][0]):.1f} {ty(verts[1][1]):.1f} '
            f'L {tx(verts[2][0]):.1f} {ty(verts[2][1]):.1f} Z'
        )
        parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{stroke_width}" stroke-linejoin="round"/>')

    inset = inset_frac * s
    for (ka, kb, mid, angle), pair in zip(edges, pairs):
        q, a = (pair + ['', ''])[:2] if isinstance(pair, list) else pair
        for key, text in ((ka, q), (kb, a)):
            if not text:
                continue
            verts = tris[key]
            rot = text_rotation(mid, verts, angle)
            cx, cy = triangle_centroid(verts)
            mx, my = mid
            dx, dy = cx - mx, cy - my
            dist = (dx ** 2 + dy ** 2) ** 0.5 or 1
            ux, uy = dx / dist, dy / dist
            px, py = tx(mx + ux * inset), ty(my + uy * inset)
            safe = html.escape(str(text))
            parts.append(
                f'<text x="{px:.1f}" y="{py:.1f}" transform="rotate({rot:.1f} {px:.1f} {py:.1f})" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-size="{font_size * _SCALE * 0.012:.1f}" fill="{INK}">{safe}</text>'
            )

    parts.append('</svg>')
    return ''.join(parts)
