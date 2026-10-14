"""Tarsia triangular-grid geometry.

An n-row Tarsia puzzle is a big equilateral triangle subdivided into n^2
small triangles (n up-triangles + (n-1) down-triangles per row, for rows
1..n). Internal edges (shared by two small triangles) each carry one
question (on one triangle, oriented to that edge) and its matching answer
(on the other triangle, oriented to the same edge). This module computes
the vertices of every small triangle and the midpoint+angle of every
internal edge, so text can be placed and rotated correctly.

Reverse-engineered directly from real Tarsia puzzle source files (pixel
geometry verified to match exactly) - see SKILL.md.
"""
import math

SQRT3 = math.sqrt(3)


def row_up_apex_x(r, i, s):
    """x of the apex (top vertex) of up-triangle i (1-indexed) in row r (1-indexed)."""
    return -r * s / 2 + i * s - s / 2


def triangle_vertices(n, s=1.0):
    """Return dict: (r, 'U'|'D', i) -> [(x,y), (x,y), (x,y)] for every small
    triangle in an n-row grid, apex of the whole figure at (0,0), y increasing
    downward."""
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
    """Return list of (key_a, key_b, midpoint, angle_degrees) for every
    internal edge (shared by exactly two small triangles). angle_degrees is
    the edge's own orientation (0 = horizontal), suitable for rotating text
    to run parallel to the edge."""
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
    """Number of (question, answer) pairs an n-row grid needs."""
    return len(internal_edges(n))
