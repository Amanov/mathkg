"""Tarsia triangular-grid geometry (server-side mirror of
static/js/tarsia-builder.js and tools/tarsia/geom.py - keep all three in
sync if the convention ever changes).

An n-row Tarsia puzzle is a big equilateral triangle subdivided into n^2
small triangles. Every internal edge (shared by two small triangles)
carries one question/answer pair, each oriented to read upright with that
edge as its own triangle's local "bottom".
"""
import math

SQRT3 = math.sqrt(3)


def row_up_apex_x(r, i, s):
    return -r * s / 2 + i * s - s / 2


def triangle_vertices(n, s=1.0):
    h = s * SQRT3 / 2
    tris = {}
    for r in range(1, n + 1):
        top = (r - 1) * h
        bot = r * h
        for i in range(1, r + 1):
            ax = row_up_apex_x(r, i, s)
            tris[(r, 'U', i)] = [(ax, top), (ax - s / 2, bot), (ax + s / 2, bot)]
        for j in range(1, r):
            ax_j = row_up_apex_x(r, j, s)
            ax_j1 = row_up_apex_x(r, j + 1, s)
            tris[(r, 'D', j)] = [(ax_j, top), (ax_j1, top), (ax_j + s / 2, bot)]
    return tris


def internal_edges(n, s=1.0):
    tris = triangle_vertices(n, s)
    edges = []
    for r in range(1, n + 1):
        for i in range(1, r):
            a = tris[(r, 'U', i)]
            mx = (a[0][0] + a[2][0]) / 2
            my = (a[0][1] + a[2][1]) / 2
            angle = math.degrees(math.atan2(a[2][1] - a[0][1], a[2][0] - a[0][0]))
            edges.append(((r, 'U', i), (r, 'D', i), (mx, my), angle))
        for i in range(1, r):
            a = tris[(r, 'D', i)]
            mx = (a[1][0] + a[2][0]) / 2
            my = (a[1][1] + a[2][1]) / 2
            angle = math.degrees(math.atan2(a[2][1] - a[1][1], a[2][0] - a[1][0]))
            edges.append(((r, 'D', i), (r, 'U', i + 1), (mx, my), angle))
    for r in range(1, n):
        for i in range(1, r + 1):
            a = tris[(r, 'U', i)]
            j = i
            if (r + 1, 'D', j) in tris:
                mx = (a[1][0] + a[2][0]) / 2
                my = (a[1][1] + a[2][1]) / 2
                edges.append(((r, 'U', i), (r + 1, 'D', j), (mx, my), 0.0))
    return edges


def triangle_centroid(verts):
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    return sum(xs) / 3, sum(ys) / 3


def edge_count(n):
    return len(internal_edges(n))


def text_rotation(edge_mid, this_tri_verts, edge_vec_angle):
    """Rotation (deg, normalized to -90..90) for text belonging to
    this_tri_verts, attached to the edge at edge_mid. Picks whichever of
    (angle, angle+180) has its 'up' direction pointing toward this
    triangle's own centroid."""
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
