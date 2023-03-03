#!/usr/bin/env pypy3

import sys

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines, {'.': 0, 'L': 1, '#': 2})
    return g

def part1(grid):
    while 1:
        g = grid.copy()
        changed = False
        for pos in grid:
            v = grid.get(pos)
            if v == 1 and all(grid.get(_) != 2 for _ in grid.neighbors8(pos)):
                g.set(pos, 2)
                changed = True
            elif v == 2 and sum(1 if grid.get(_) == 2 else 0 for _ in grid.neighbors8(pos)) >= 4:
                g.set(pos, 1)
                changed = True

        grid = g

        if not changed:
            break

    cnt = sum(1 if grid.get(_) == 2 else 0 for _ in grid)
    print(cnt)

def scan8(grid, pos):
    for dir in ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'):
        p2 = pos
        while 1:
            p2 = grid.step(p2, dir)
            if p2 is None:
                break
            if grid.get(p2):
                yield p2
                break

def part2(grid):
    while 1:
        g = grid.copy()
        changed = False
        for pos in grid:
            v = grid.get(pos)
            if v == 1 and all(grid.get(_) != 2 for _ in scan8(grid, pos)):
                g.set(pos, 2)
                changed = True
            elif v == 2 and sum(1 if grid.get(_) == 2 else 0 for _ in scan8(grid, pos)) >= 5:
                g.set(pos, 1)
                changed = True

        grid = g

        if not changed:
            break

    cnt = sum(1 if grid.get(_) == 2 else 0 for _ in grid)
    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
