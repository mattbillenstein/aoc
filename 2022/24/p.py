#!/usr/bin/env pypy3

import sys
import time
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
#    grid.print()

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

#        print()
#        print(step)
#        ngrid.print()

    return grids

last = time.time()
def dfs(grids, max_steps):
    global last

    for pt in grids[0]:
        v = grids[0].get(pt)
        if v == START:
            start = pt
        elif v == END:
            end = pt

#    print(start, end)

    best = (10000, None)
#    stack = [(1, [start])]
    stack = deque([(1, [start])])

    while stack:
#        step, path = stack.pop()
        step, path = stack.popleft()

        pt = path[-1]

        dist = abs(pt[0] - start[0]) + abs(pt[1] - start[1])
        if len(path) > 15 and dist*2 < len(path):
            # if steps are more than 2x the manhattan distance, abort this path
            continue

        if step >= max_steps:
            continue

        if step > len(grids)-1:
            print('End of grids')
            continue

        grid = grids[step]

        if 0 or time.time() - last > 10:
            print()
            g = grids[step-1]
            v = g.get(pt)
            g.set(pt, END)
            d = defaultdict(int)
            for p in path:
                d[p] += 1
            print(step-1, path)
            print(len(path), dist, len(d), max(d.values()))

            g.print()
#            print()
#            grid.print()
            if v in (EMPTY, None):
                g.remove(pt)
            else:
                g.set(pt, v)
            last = time.time()

        size = grid.size
        found = False
        for npt in grid.neighbors_manhattan(pt):
            if not (0 <= npt[0] < size[0] and 0 <= npt[1] < size[1]):
                continue
            
            v = grid.get(npt, EMPTY)

            if v == END:
                if len(path)+1 < best[0]:
                    best = (len(path)+1, path + [npt])
                    print(best)
                continue

            if v == EMPTY:
                found = True
                stack.append((step+1, path + [npt]))

        if not found:
            # wait
            stack.append((step+1, path + [path[-1]]))

    return best[1]

def part1(grid):
    size = grid.size
    depth = size[0] * size[1] * 2
    grids = generate_grids(grid, depth)

    path = dfs(grids, depth)
    print(path)
    print(len(path) - 1)  # exclude start as a step

    i = 0
    for pt, g in zip(path, grids):
#        print()
#        print(i, pt)
        assert g.get(pt, EMPTY) in (START, EMPTY, END), g.get(pt)
#        g.set(pt, END)
#        g.print()
        i += 1


def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
