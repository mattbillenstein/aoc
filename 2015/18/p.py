#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines)

def part1(grid, part=1):
    for i in range(100):
        g = grid.copy()

        for pt in grid:
            cnt = sum(grid.get(npt) for npt in grid.neighbors8(pt))
            if g.get(pt):
                if not 2 <= cnt <= 3:
                    g.set(pt, 0)
            else:
                if cnt == 3:
                    g.set(pt, 1)

        if part == 2:
            g.set((0, 0), 1)
            g.set((0, 99), 1)
            g.set((99, 0), 1)
            g.set((99, 99), 1)

        grid = g

        if DEBUG:
            print()
            grid.print()

    print(sum(grid.get(_) for _ in grid))

def part2(data):
    part1(data, 2)

def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
