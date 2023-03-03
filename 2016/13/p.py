#!/usr/bin/env pypy3

import sys

from graph import bfs
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return int(lines[0])

def part(data):
    g = Grid(['.' * 100] * 100, {'.': 0, '#': 1, 'O': 2})

    for x in g.xs:
        for y in g.ys:
            q = x*x + 3*x + 2*x*y + y + y*y + data
            r = 1
            cnt = 0
            while r <= q:
                if r & q:
                    cnt += 1
                r *= 2

            g.set((x, y), cnt % 2)

    def neighbors(pt):
        for npt in g.neighbors4(pt):
            if g.get(npt) == 0:
                yield npt

    if DEBUG:
        g.print()

    dist = bfs((1, 1), neighbors, (31, 39))
    print(dist)

    s = set()
    for pt in g:
        if g.get(pt) == 0:
            s.add(pt)

    found = bfs((1, 1), neighbors, s)
    print(sum(1 for pt, dist in found if dist <= 50))

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
