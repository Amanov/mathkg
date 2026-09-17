"""Single source of truth for the 11-cell question grid geometry, shared
by both the PDF template (as CSS percentages) and the PPTX builder (as
EMU rectangles), so the two output formats never drift apart.

Layout (4 weighted columns x 4 equal rows):
    q1 q1 q2 q3
    q4 q4 q5 q6
    q7 q7 q8 q11
    q9 q9 q10 q11
"""

COL_WEIGHTS = [1.1, 1.1, 1.0, 1.0]
ROW_COUNT = 4

# number -> (col_start, col_span, row_start, row_span), 0-indexed
CELL_SPANS = {
    1: (0, 2, 0, 1), 2: (2, 1, 0, 1), 3: (3, 1, 0, 1),
    4: (0, 2, 1, 1), 5: (2, 1, 1, 1), 6: (3, 1, 1, 1),
    7: (0, 2, 2, 1), 8: (2, 1, 2, 1), 11: (3, 1, 2, 2),
    9: (0, 2, 3, 1), 10: (2, 1, 3, 1),
}


def _col_edges_pct():
    total = sum(COL_WEIGHTS)
    edges = [0.0]
    for w in COL_WEIGHTS:
        edges.append(edges[-1] + 100.0 * w / total)
    return edges


def cell_rect_pct(number):
    """Returns (left%, top%, width%, height%) for a question number."""
    col_start, col_span, row_start, row_span = CELL_SPANS[number]
    col_edges = _col_edges_pct()
    row_h = 100.0 / ROW_COUNT
    left = col_edges[col_start]
    width = col_edges[col_start + col_span] - left
    top = row_start * row_h
    height = row_span * row_h
    return left, top, width, height
