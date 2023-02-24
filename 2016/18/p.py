#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part1(row, rows=40):
    g = Grid([row] + ['.' * len(row)] * (rows - 1), {'.': 0, '^': 1})

    for y in g.ys:
        if y == 0:
            continue

        for x in g.xs:
            l = c = r = 0
            if x > 0:
                l = g.get((x-1, y-1))
            c = g.get((x, y-1))
            if x < g.size[0]-1:
                r = g.get((x+1, y-1))

            if (l, c, r) in [(1, 1, 0), (0, 1, 1), (1, 0, 0), (0, 0, 1)]:
                g.set((x, y), 1)

    if DEBUG:
        print()
        g.print()

    print(sum(1 for _ in g if not g.get(_)))

def part2(row):
    part1(row, 400_000)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
