"""Renders the coordinate-grid reflection diagram for the geometry recall
question as inline SVG, so the worksheet needs no external image asset and
no extra dependency (matplotlib etc.) - just plain string formatting."""

_RANGE = 5
_CELL = 26
_MARGIN = 22
_SIZE = _MARGIN * 2 + _CELL * _RANGE * 2


def _to_px(x, y):
    return (_MARGIN + (x + _RANGE) * _CELL, _MARGIN + (_RANGE - y) * _CELL)


def _polygon_points(points):
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in (_to_px(x, y) for x, y in points))


def build_reflection_svg(points, reflected, mirror_x, show_answer, px_size=190):
    # WeasyPrint's SVG support does not reliably compute an "auto"/percentage
    # height for inline SVG the way a browser does, so both dimensions are
    # given as fixed pixels here - an unconstrained size caused the diagram
    # to overflow its grid cell and spill a blank page onto the PDF.
    lines = []
    lines.append(
        f'<svg viewBox="0 0 {_SIZE} {_SIZE}" width="{px_size}" height="{px_size}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">'
    )
    # grid lines
    for i in range(-_RANGE, _RANGE + 1):
        x0, y0 = _to_px(i, -_RANGE)
        x1, y1 = _to_px(i, _RANGE)
        stroke = "#94a3b8" if i != 0 else "#334155"
        width = 1 if i != 0 else 1.6
        lines.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{stroke}" stroke-width="{width}"/>')
        x0, y0 = _to_px(-_RANGE, i)
        x1, y1 = _to_px(_RANGE, i)
        stroke = "#94a3b8" if i != 0 else "#334155"
        width = 1 if i != 0 else 1.6
        lines.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{stroke}" stroke-width="{width}"/>')

    # mirror line x = mirror_x
    mx0, my0 = _to_px(mirror_x, -_RANGE)
    mx1, my1 = _to_px(mirror_x, _RANGE)
    lines.append(
        f'<line x1="{mx0:.1f}" y1="{my0:.1f}" x2="{mx1:.1f}" y2="{my1:.1f}" '
        f'stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>'
    )
    lx, ly = _to_px(mirror_x, _RANGE)
    lines.append(f'<text x="{lx + 4:.1f}" y="{ly - 4:.1f}" font-size="12" fill="#dc2626">x = {mirror_x}</text>')

    # shape A
    lines.append(f'<polygon points="{_polygon_points(points)}" fill="rgba(15,60,88,0.25)" stroke="#0f3c58" stroke-width="2"/>')
    cx = sum(p[0] for p in points) / 3
    cy = sum(p[1] for p in points) / 3
    lax, lay = _to_px(cx, cy)
    lines.append(f'<text x="{lax:.1f}" y="{lay:.1f}" font-size="14" font-weight="bold" fill="#0f3c58">A</text>')

    if show_answer:
        lines.append(f'<polygon points="{_polygon_points(reflected)}" fill="rgba(13,110,253,0.2)" stroke="#0d6efd" stroke-width="2" stroke-dasharray="4,3"/>')
        rcx = sum(p[0] for p in reflected) / 3
        rcy = sum(p[1] for p in reflected) / 3
        rax, ray = _to_px(rcx, rcy)
        lines.append(f'<text x="{rax:.1f}" y="{ray:.1f}" font-size="14" font-weight="bold" fill="#0d6efd">A\'</text>')

    lines.append('</svg>')
    return "".join(lines)
