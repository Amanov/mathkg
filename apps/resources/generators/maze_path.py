"""Seeded correct routes for «Туурабы? Лабиринт» worksheets.

Each maze keeps a single orthogonal route from the start edge to the finish
edge. Correct cells are exactly that route: two of them touch only when they
are the next step, so a neighbour cannot open a shortcut. The shape is chosen
from the maze name, so the same file rebuilds the same route and two mazes
do not share a shape.

Statements already on the sheet are only moved. True statements stay true and
false ones stay the plausible errors they were. Nothing here rewrites a
number, so the Kyrgyz thousands space and decimal comma travel with the text.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass

# The route that was copied onto almost every 5×5 answer key.
CANONICAL_5X5 = frozenset({
    (0, 0), (0, 1),
    (1, 1),
    (2, 0), (2, 1),
    (3, 0), (3, 2), (3, 3), (3, 4),
    (4, 0), (4, 1), (4, 2), (4, 4),
})
# 1-klass addition sheet, before this rebuild.
CANONICAL_KOSHUU = frozenset({
    (0, 0), (0, 2), (0, 3), (0, 4),
    (1, 0), (1, 1), (1, 2), (1, 4),
    (2, 3), (2, 4),
    (3, 3),
    (4, 3), (4, 4),
})
# Statistics lesson maze, 6 rows × 4 columns.
CANONICAL_STATISTICS = frozenset({
    (0, 1),
    (1, 1), (1, 2), (1, 3),
    (2, 3),
    (3, 1), (3, 2), (3, 3),
    (4, 0), (4, 1),
    (5, 0),
})

SHARED_AVOID = frozenset({CANONICAL_5X5, CANONICAL_KOSHUU, CANONICAL_STATISTICS})

_STEPS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def seed_int(key: str) -> int:
    digest = hashlib.sha256(key.encode('utf-8')).digest()
    return int.from_bytes(digest[:8], 'big')


def neighbors(row: int, col: int, rows: int, cols: int):
    for dr, dc in _STEPS:
        rr, cc = row + dr, col + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            yield rr, cc


def edge_sides(row: int, col: int, rows: int, cols: int, allowed: tuple[str, ...]) -> tuple[str, ...]:
    """Sides of this cell that open onto a margin wide enough for a label."""
    found = []
    if col == 0 and 'left' in allowed:
        found.append('left')
    if col == cols - 1 and 'right' in allowed:
        found.append('right')
    if row == 0 and 'top' in allowed:
        found.append('top')
    if row == rows - 1 and 'bottom' in allowed:
        found.append('bottom')
    return tuple(found)


def allowed_label_sides(left: float, right: float, top: float, bottom: float) -> tuple[str, ...]:
    """Margins that can hold «БАШТА» / «МААРА» without covering a cell or the instruction."""
    sides = []
    if left >= 56:
        sides.append('left')
    if right >= 56:
        sides.append('right')
    # A deep top band is the instruction, not an empty margin.
    if 26 <= top <= 72:
        sides.append('top')
    if 26 <= bottom <= 50:
        sides.append('bottom')
    if len(sides) >= 2:
        return tuple(sides)
    ranked = sorted(
        (('left', left), ('right', right), ('top', top), ('bottom', bottom)),
        key=lambda item: item[1],
        reverse=True,
    )
    return tuple(name for name, _gap in ranked[:2])


def _induced_extension(path: list[tuple[int, int]], row: int, col: int) -> bool:
    """The new cell may touch only the cell it is stepped from."""
    previous = len(path) - 1
    for index, (pr, pc) in enumerate(path):
        if abs(pr - row) + abs(pc - col) == 1 and index != previous:
            return False
    return True


@dataclass(frozen=True)
class MazePath:
    rows: int
    cols: int
    cells: tuple[tuple[int, int], ...]
    start_side: str
    finish_side: str

    @property
    def mask(self) -> frozenset[tuple[int, int]]:
        return frozenset(self.cells)

    @property
    def start(self) -> tuple[int, int]:
        return self.cells[0]

    @property
    def finish(self) -> tuple[int, int]:
        return self.cells[-1]

    def pattern(self) -> str:
        marks = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        for row, col in self.cells:
            marks[row][col] = 'G'
        return '\n'.join(''.join(line) for line in marks)


def _choose_sides(path, rows, cols, allowed, rng: random.Random):
    start_opts = list(edge_sides(*path[0], rows, cols, allowed))
    finish_opts = list(edge_sides(*path[-1], rows, cols, allowed))
    rng.shuffle(start_opts)
    rng.shuffle(finish_opts)

    def crowded(side, start, finish):
        if side in ('left', 'right'):
            return abs(start[0] - finish[0]) < 2
        return abs(start[1] - finish[1]) < 2

    # Prefer a route that enters on one side and leaves on the other.
    ordered = []
    for start_side in start_opts:
        for finish_side in finish_opts:
            same = start_side == finish_side
            blocked = same and crowded(start_side, path[0], path[-1])
            ordered.append((blocked, same, start_side, finish_side))
    ordered.sort(key=lambda item: (item[0], item[1]))
    for blocked, _same, start_side, finish_side in ordered:
        if blocked:
            continue
        return start_side, finish_side
    return None


def _random_path(rng, rows, cols, length, allowed, budget: int = 25000):
    starts = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if edge_sides(row, col, rows, cols, allowed)
    ]
    rng.shuffle(starts)
    remaining = budget

    def search(start):
        nonlocal remaining
        path = [start]
        used = {start}

        def walk():
            nonlocal remaining
            remaining -= 1
            if remaining <= 0:
                return None
            if len(path) == length:
                if path[-1] == path[0]:
                    return None
                if not edge_sides(*path[-1], rows, cols, allowed):
                    return None
                sides = _choose_sides(path, rows, cols, allowed, rng)
                if sides is None:
                    return None
                return path[:], sides
            row, col = path[-1]
            options = list(neighbors(row, col, rows, cols))
            rng.shuffle(options)
            for nxt_row, nxt_col in options:
                if (nxt_row, nxt_col) in used:
                    continue
                if not _induced_extension(path, nxt_row, nxt_col):
                    continue
                path.append((nxt_row, nxt_col))
                used.add((nxt_row, nxt_col))
                found = walk()
                if found is not None:
                    return found
                used.remove((nxt_row, nxt_col))
                path.pop()
                if remaining <= 0:
                    return None
            return None

        return walk()

    for start in starts:
        found = search(start)
        if found is not None:
            cells, (start_side, finish_side) = found
            return MazePath(rows, cols, tuple(cells), start_side, finish_side)
    return None


def find_path(key, rows, cols, length, avoid, allowed=('left', 'right'), attempts: int = 80):
    """Return a reproducible route for ``key`` whose cells are not in ``avoid``."""
    base = seed_int(key)
    for attempt in range(attempts):
        rng = random.Random(base + attempt * 1_000_003)
        path = _random_path(rng, rows, cols, length, allowed)
        if path is None:
            continue
        if path.mask in avoid:
            continue
        if not is_single_route(path.mask, rows, cols):
            continue
        return path
    raise RuntimeError(f'no unique route for {key} ({rows}×{cols}, {length} cells)')


def is_single_route(mask: frozenset, rows: int, cols: int) -> bool:
    """True when the green cells are one induced path and nothing else."""
    cells = list(mask)
    if len(cells) < 2:
        return False
    green = set(cells)
    degree = {}
    for row, col in cells:
        degree[(row, col)] = sum(1 for nb in neighbors(row, col, rows, cols) if nb in green)
    if any(value not in (1, 2) for value in degree.values()):
        return False
    if sum(1 for value in degree.values() if value == 1) != 2:
        return False
    if sum(degree.values()) != 2 * (len(cells) - 1):
        return False
    start = next(cell for cell, value in degree.items() if value == 1)
    seen = {start}
    queue = [start]
    while queue:
        row, col = queue.pop()
        for nxt in neighbors(row, col, rows, cols):
            if nxt in green and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen) == len(cells)


def endpoints(mask: frozenset, rows: int, cols: int) -> tuple[tuple[int, int], tuple[int, int]]:
    green = set(mask)
    ends = []
    for row, col in mask:
        degree = sum(1 for nb in neighbors(row, col, rows, cols) if nb in green)
        if degree == 1:
            ends.append((row, col))
    if len(ends) != 2:
        raise ValueError('green cells are not a single path')
    return tuple(sorted(ends))


@dataclass(frozen=True)
class Placement:
    path: MazePath
    # New grid slot -> slot the statement is copied from.
    mapping: tuple[tuple[tuple[int, int], tuple[int, int]], ...]

    def as_dict(self) -> dict[tuple[int, int], tuple[int, int]]:
        return dict(self.mapping)


def placement_for(key, rows, cols, true_cells, avoid, allowed=('left', 'right')) -> Placement:
    """Move the existing true cells onto a new route. False cells fill the rest."""
    if len(true_cells) < 2:
        raise ValueError(f'{key} has no route to vary')
    path = find_path(key, rows, cols, len(true_cells), avoid, allowed)
    rng = random.Random(seed_int(key + ':cells'))
    trues = list(true_cells)
    falses = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if (row, col) not in set(true_cells)
    ]
    rng.shuffle(trues)
    rng.shuffle(falses)
    spare = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if (row, col) not in path.mask
    ]
    if len(trues) != len(path.cells) or len(falses) != len(spare):
        raise ValueError(f'{key} cell counts do not match the route')
    pairs = list(zip(path.cells, trues)) + list(zip(spare, falses))
    return Placement(path, tuple(pairs))


def assign_routes(specs) -> dict[str, Placement]:
    """One route per maze key.

    Each spec is ``(key, rows, cols, true cells, allowed sides)``.
    """
    avoid = set(SHARED_AVOID)
    placed = {}
    for key, rows, cols, true_cells, allowed in sorted(specs, key=lambda item: item[0]):
        placement = placement_for(key, rows, cols, list(true_cells), avoid, allowed)
        avoid.add(placement.path.mask)
        placed[key] = placement
    masks = [item.path.mask for item in placed.values()]
    if len(masks) != len(set(masks)):
        raise RuntimeError('two mazes received the same route')
    return placed


def format_kyrgyz_number(value: float | int) -> str:
    """Thousands grouped with a space, fraction with a comma."""
    if isinstance(value, float) and not value.is_integer():
        text = f'{value:.4f}'.rstrip('0').rstrip('.')
        whole, frac = text.split('.')
        sign = ''
        if whole.startswith('-'):
            sign, whole = '-', whole[1:]
        grouped = f'{int(whole):,}'.replace(',', ' ') if whole else '0'
        return f'{sign}{grouped},{frac}'
    number = int(value)
    sign = '-' if number < 0 else ''
    grouped = f'{abs(number):,}'.replace(',', ' ')
    return sign + grouped
