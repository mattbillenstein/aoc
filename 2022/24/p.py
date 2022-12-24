#!/usr/bin/env pypy3

import sys
from collections import defaultdict, deque
from pprint import pprint

from grid import SparseGrid

EMPTY = 0
UP = 2
DOWN = 4
LEFT = 8
RIGHT = 16
WALL = 32
START = 64
END = 128

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    chars = {
        '#': WALL,
        '^': UP,
        'v': DOWN,
        '<': LEFT,
        '>': RIGHT,
        '.': EMPTY,
        'S': START,
        'E': END,
    }

    grid = SparseGrid(lines, chars=chars)
    grid.set((1, 0), START)
    size = grid.size
    grid.set((size[0]-1-1, size[1]-1), END)

    return grid

def generate_grids(grid, steps):
    size = grid.size

    grids = [grid.copy()]

    for step in range(1, steps):
        grid = grids[-1]

        ngrid = grid.copy()
        for k, v in grid.g.items():
            if v not in (WALL, START, END):
                del ngrid.g[k]
        grids.append(ngrid)

        for pt, v in grid.g.items():
            if v not in (WALL, EMPTY):
                for dir in (UP, DOWN, LEFT, RIGHT):
                    if v & dir:
                        ndir = grid.values[v & dir]
                        npt = grid.step(pt, ndir)
                        if grid.get(npt) == WALL:
                            # wrap
                            x, y = npt
                            if ndir == '^':
                                npt = (x, size[1]-1-1)
                            elif ndir == 'v':
                                npt = (x, 1)
                            elif ndir == '<':
                                npt = (size[0]-1-1, y)
                            elif ndir == '>':
                                npt = (1, y)

                        ngrid.g.setdefault(npt, 0)
                        ngrid.g[npt] |= v & dir

    return grids

def bfs(grids, v1=START, v2=END):
    for pt in grids[0]:
        v = grids[0].get(pt)
        if v == v1:
            start = pt
        elif v == v2:
            end = pt

    seen = set([(start, 1)])
    queue = deque([(start, 1)])
    while queue:
        vertex, step = queue.popleft()

        grid = grids[step]

        if vertex == end:
            return step - 1  # don't count the first step...

        size = grid.size

        x, y = vertex
        for npt in [(x+1, y), (x, y+1), (x, y-1), (x-1, y)]:
            if (npt, step+1) in seen:
                continue

            if not (0 <= npt[0] < size[0] and 0 <= npt[1] < size[1]):
                continue

            v = grid.get(npt, EMPTY)
            if v == EMPTY or npt == end:
                seen.add((npt, step+1))
                queue.append((npt, step+1))

        # wait if we can - we need to check we're not currently sitting on an
        # occupied spot...
        if grid.get(vertex, EMPTY) == EMPTY:
            seen.add((vertex, step+1))
            queue.append((vertex, step+1))

def part1(grid):
    size = grid.size
    depth = (size[0] + size[1]) * 3   # ?
    grids = generate_grids(grid, depth)
    steps = bfs(grids)
    print(steps)

def part2(grid):
    size = grid.size
    depth = (size[0] + size[1]) * 10   # ?
    grids = generate_grids(grid, depth)

    steps = bfs(grids)

    print(steps)

    for i in range(steps, steps+10):
        x = bfs(grids[i:], END, START)
        if x:
            ds = (i-steps) + x
            steps += ds
            print(ds, steps)
            break

    for i in range(steps, steps+10):
        x = bfs(grids[i:])
        if x:
            ds = (i-steps) + x
            steps += ds
            print(ds, steps)
            break

def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
