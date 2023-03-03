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

def run(grid, times):
    for i in range(times):
        g = grid.copy()

        for pt in grid:
            cnts = defaultdict(int)
            for npt in grid.neighbors8(pt):
                c = grid.getc(npt)
                cnts[c] += 1

            c = grid.getc(pt)
            if c == '.' and cnts['|'] >= 3:
                g.setc(pt, '|')
            elif c == '|' and cnts['#'] >= 3:
                g.setc(pt, '#')
            elif c == '#' and not (cnts['#'] >= 1 and cnts['|'] >= 1):
                g.setc(pt, '.')

        grid = g
        yield grid

def part1(grid):
    for i, g in enumerate(run(grid, 10)):
        if DEBUG:
            print()
            print(i+1)
            g.print()

    cnts = defaultdict(int)
    for pt in g:
        c = g.getc(pt)
        cnts[c] += 1

    print(cnts['#'] * cnts['|'])

def part2(grid):
    N = 1_000_000_000

    # pattern starts repeating every 28 iterations eventually
    seen = {}
    for i, g in enumerate(run(grid, 1000)):
        i += 1
        h = g.hash()
        if h in seen:
            period = i - seen[h]
            debug(h, seen[h], i, period)

            # when we're on the same pattern as would show up in iteration 1B,
            # break and compute resources...
            if (N - i) % period == 0:
                break

        seen[h] = i

    cnts = defaultdict(int)
    for pt in g:
        c = g.getc(pt)
        cnts[c] += 1

    print(cnts['#'] * cnts['|'])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
