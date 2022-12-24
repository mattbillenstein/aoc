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
def dfs(grids):
    global last
    start_time = time.time()

    for pt in grids[0]:
        v = grids[0].get(pt)
        if v == START:
            start = pt
        elif v == END:
            end = pt

#    print(start, end)

    max_steps = len(grids)
    best = (10000, [])
    stack = []
    stack.append((1, [start]))

    i = 0
    while stack:
        i += 1
        step, path = stack.pop()

        pt = path[-1]

        dist = abs(pt[0] - start[0]) + abs(pt[1] - start[1])
#        if len(path) > 15 and dist*4 < len(path):
#            # if steps are more than 2x the manhattan distance, abort this path
#            print('hi')
#            continue

        passes = defaultdict(int)
        for p in path:
            passes[p] += 1
        max_pass = max(passes.values())
        sum_pass = sum(_ for _ in passes.values() if _ != 1)
        if sum_pass > 50:
            continue
        if sum_pass//2 > len(passes):
            continue
        if max_pass > 5:
            continue

        if step >= max_steps:
            continue

        if step > len(grids)-1:
            print('End of grids')
            continue

        grid = grids[step]

        if 0 or time.time() - last > 10:
            print()

            # print the grid at the end of the last step, before considring the
            # next grid...
            g = grids[step-1]
            v = g.get(pt, EMPTY)
            assert v == EMPTY

            G = g.copy()
            G.set(pt, END)

            print(f'Step:{step-1} Point:{pt}') # Path:{path}')
            print(f'Best:{best[0]} Depth:{len(path)} Distance:{dist} Unique:{len(passes)} Max-passthroughs:{max_pass} Sum-passthroughs:{sum_pass} Paths:{i} Paths/s:{(i/(time.time() - start_time)):2f}')

            G.print()

            last = time.time()

        size = grid.size
        found = False
        for npt in grid.neighbors_manhattan(pt):
            if not (0 <= npt[0] < size[0] and 0 <= npt[1] < size[1]):
                continue
            
            v = grid.get(npt, EMPTY)

            if v == EMPTY:
                found = True
                stack.append((step+1, path + [npt]))
            elif v == END:
                if len(path)+1 < best[0]:
                    best = (len(path)+1, path + [npt])
                    print(f'Best: {best}')

        if not found:
            # wait if we can - we need to check we're not currently sitting on
            # an occupied spot...
            if grid.get(pt, EMPTY) == EMPTY:
                stack.append((step+1, path + [pt]))

    return best[1]

def part1(grid):
    size = grid.size
    depth = 2000 #(size[0] + size[1]) * 20
    print(depth)
    grids = generate_grids(grid, depth)

    if 0:
        for i, g in enumerate(grids):
            cnt = 0
            d = defaultdict(int)
            for pt in g:
                v = g.get(pt)
                for dir in (UP, DOWN, LEFT, RIGHT):
                    if v & dir:
                        d[dir] += 1
                        cnt += 1
            print(i, cnt, d)
            g.print()

    path = dfs(grids)
    print(path)
    print(len(path) - 1)  # exclude start as a step

    if 0:
        i = 0
        for pt, g in zip(path, grids):
            print()
            print(i, pt)
            g.print()
            assert g.get(pt, EMPTY) in (START, EMPTY, END), g.get(pt)
    #        g.set(pt, END)
            g.print()
            i += 1


def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
