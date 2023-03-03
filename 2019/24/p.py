#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines)

def part1(grid):
    states = set()

    while 1:
        if DEBUG:
            print()
            grid.print()

        state = []

        add = []
        remove = []
        for pt in grid:
            cnt = sum(grid.get(_) for _ in grid.neighbors4(pt))
            v = grid.get(pt)
            if v:
                state.append(pt)

            if v and cnt != 1:
                remove.append(pt)
            if not v and 1 <= cnt <= 2:
                add.append(pt)

        state = tuple(state)
        if state in states:
            break

        states.add(state)

        for pt in add:
            grid.set(pt, 1)
        for pt in remove:
            grid.set(pt, 0)

    if DEBUG:
        print()
        grid.print()

    x = 1
    tot = 0
    for pt in grid:
        if grid.get(pt):
            tot += x
        x *= 2

    print(tot)

def part2(grid):
    CENTER = (2, 2)

    empty = grid.copy()
    empty.clear()

    grids = defaultdict(lambda: empty.copy())
    grids[0] = grid

    def neighbors(pt, level):
        grid = grids[level]
        L = [(_, level) for _ in grid.neighbors4(pt)]
        if (CENTER, level) in L:
            L.remove((CENTER, level))
            if pt[0] < CENTER[0]:
                # left, include level+1 first column
                for y in range(5):
                    L.append(((0, y), level+1))
            elif pt[0] > CENTER[0]:
                # right, include level+1 last column
                for y in range(5):
                    L.append(((4, y), level+1))
            elif pt[1] < CENTER[1]:
                # top, include level+1 first row
                for x in range(5):
                    L.append(((x, 0), level+1))
            elif pt[1] > CENTER[1]:
                # bottom, include level+1 last row
                for x in range(5):
                    L.append(((x, 4), level+1))

        # edges, include adjacent cell in level-1
        if pt[0] == 0:
            L.append(((1, 2), level-1))
        if pt[0] == 4:
            L.append(((3, 2), level-1))
        if pt[1] == 0:
            L.append(((2, 1), level-1))
        if pt[1] == 4:
            L.append(((2, 3), level-1))

        return L

    for i in range(200):
        minlvl = min(grids)
        maxlvl = max(grids)

        add = []
        remove = []
        for level in range(minlvl-1, maxlvl+1+1):
            grid = grids[level]
            for pt in grid:
                if pt == CENTER:
                    continue

                cnt = sum(grids[_[1]].get(_[0]) for _ in neighbors(pt, level))
                v = grid.get(pt)

                if v and cnt != 1:
                    remove.append((pt, level))
                if not v and 1 <= cnt <= 2:
                    add.append((pt, level))

        for pt, level in add:
            grids[level].set(pt, 1)
        for pt, level in remove:
            grids[level].set(pt, 0)

    tot = 0
    for level in sorted(grids):
        grid = grids[level]
        cnt = sum(grid.get(_) for _ in grid)
        if not cnt:
            continue

        tot += cnt

        if DEBUG:
            print(level)
            grid.print()
            print()

    print(tot)

def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
