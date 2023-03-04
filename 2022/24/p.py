#!/usr/bin/env pypy3

import sys
from collections import deque

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

def next_grid(grid):
    ngrid = grid.copy()
    for k, v in grid.g.items():
        if v not in (WALL, START, END):
            del ngrid.g[k]

    size = grid.size
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

    return ngrid

def get_grid(grids, i):
    j = len(grids) - 1
    while j < i:
        grids.append(next_grid(grids[j]))
        j += 1
    return grids[i]

def bfs(grids, v1=START, v2=END):
    grid = grids[0]
    for pt in grid:
        v = grid.get(pt)
        if v == v1:
            start = pt
        elif v == v2:
            end = pt

    seen = set([(start, 0)])
    queue = deque([(start, 0)])
    while queue:
        vertex, step = queue.popleft()

        grid = get_grid(grids, step)

        if vertex == end:
            return step

        size = grid.size

        for npt in grid.neighbors4(vertex):
            if (npt, step+1) in seen:
                continue

            if not (0 <= npt[0] < size[0] and 0 <= npt[1] < size[1]):
                continue

            v = grid.get(npt)
            if v == EMPTY or npt == end:
                seen.add((npt, step+1))
                queue.append((npt, step+1))

        # wait if we can - we need to check we're not currently sitting on an
        # occupied spot...
        if grid.get(vertex) == EMPTY:
            seen.add((vertex, step+1))
            queue.append((vertex, step+1))

def run(grid):
    grids = [next_grid(grid)]
    steps = bfs(grids)
    print(steps)

    for i in range(steps, steps+10):
        get_grid(grids, i)
        x = bfs(grids[i:], END, START)
        if x:
            ds = (i-steps) + x
            steps += ds
#            print(ds, steps)
            break

    for i in range(steps, steps+10):
        get_grid(grids, i)
        x = bfs(grids[i:])
        if x:
            ds = (i-steps) + x
            steps += ds
#            print(ds, steps)
            break

    print(steps)

def main():
    grid = parse_input()
    run(grid.copy())

if __name__ == '__main__':
    main()
