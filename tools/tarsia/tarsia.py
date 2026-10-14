"""Render a Tarsia triangle jigsaw to PNG (for slide embedding) and a
vector PDF (for print), from a list of (question, answer) pairs - one
pair per internal edge of an n-row triangular grid. See geom.py for the
grid math and SKILL.md for the full write-up of the convention.
"""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from geom import triangle_vertices, internal_edges, triangle_centroid, edge_count


def _text_rotation(edge_mid, this_tri_verts, edge_vec_angle):
    """Rotation (deg, normalized to -90..90 for legibility) for text that
    belongs to `this_tri_verts`, sitting near the edge at edge_mid. Picks
    whichever of (angle, angle+180) has its 'up' direction pointing toward
    this triangle's own centroid, i.e. the edge reads as this triangle's
    local 'bottom'."""
    cx, cy = triangle_centroid(this_tri_verts)
    mx, my = edge_mid
    rot = edge_vec_angle
    for cand in (edge_vec_angle, edge_vec_angle + 180):
        rad = math.radians(cand + 90)
        up = (math.cos(rad), math.sin(rad))
        d = (cx - mx, cy - my)
        if up[0] * d[0] + up[1] * d[1] > 0:
            rot = cand
            break
    return ((rot + 90) % 180) - 90


def render_tarsia(n, pairs, out_png=None, out_pdf=None, s=1.8, dpi=220,
                   ink='#1F2A44', line_w=2.0, fontsize=9, margin=0.2,
                   inset_frac=0.11):
    """pairs: list of (question_str, answer_str), length must equal
    geom.edge_count(n). Writes out_png and/or out_pdf (pass None to skip
    either)."""
    need = edge_count(n)
    if len(pairs) != need:
        raise ValueError(f'n={n} grid needs exactly {need} (question, answer) pairs, got {len(pairs)}')

    tris = triangle_vertices(n, s)
    edges = internal_edges(n, s)

    fig_w = (n * s + 2 * margin) * 1.6
    fig_h = (n * s * math.sqrt(3) / 2 + 2 * margin) * 1.6
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    for verts in tris.values():
        xs = [v[0] for v in verts] + [verts[0][0]]
        ys = [v[1] for v in verts] + [verts[0][1]]
        ax.plot(xs, ys, color=ink, linewidth=line_w, solid_capstyle='round')

    inset = inset_frac * s
    for (ka, kb, mid, angle), (q, a) in zip(edges, pairs):
        for key, text in ((ka, q), (kb, a)):
            verts = tris[key]
            rot = _text_rotation(mid, verts, angle)
            cx, cy = triangle_centroid(verts)
            mx, my = mid
            dx, dy = cx - mx, cy - my
            dist = math.hypot(dx, dy)
            ux, uy = (dx / dist, dy / dist) if dist else (0, 0)
            tx, ty = mx + ux * inset, my + uy * inset
            ax.text(tx, ty, text, rotation=rot, ha='center', va='center',
                     fontsize=fontsize, color=ink, family='DejaVu Sans')

    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')
    fig.tight_layout(pad=0.1)
    if out_png:
        fig.savefig(out_png, dpi=dpi, bbox_inches='tight', pad_inches=0.08, facecolor='white')
    if out_pdf:
        fig.savefig(out_pdf, bbox_inches='tight', pad_inches=0.08, facecolor='white')
    plt.close(fig)
