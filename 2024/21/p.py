#!/usr/bin/env pypy3

import sys
from functools import lru_cache

from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return (lines,)

def make_paths(cpt, npt, g):
    # only take L paths if they don't pass through the # in the grid
    if cpt == npt:
        return ['A']

    nx, ny = (abs(npt[0] - cpt[0]), abs(npt[1] - cpt[1]))
    cx = '>' if npt[0] > cpt[0] else '<'
    cy = 'v' if npt[1] > cpt[1] else '^'

    paths = set([cx * nx + cy * ny, cy * ny + cx * nx])
    for path in list(paths):
        pt = cpt
        for dir in path:
            pt = g.step(pt, dir)
            if g.getc(pt) == '#':
                paths.remove(path)
                break

    return [_ + 'A' for _ in paths]

def part(codes):
    # use small grids to generate paths
    dg = Grid(['#^A', '<v>'])
    ng = Grid(['789', '456', '123', '#0A'])

    # generate paths between points on each grid
    paths = {}
    for g in (dg, ng):
        for pt1, c1 in g.iterc():
            if c1 != '#':
                for pt2, c2 in g.iterc():
                    if c2 != '#':
                        paths[(c1, c2)] = make_paths(pt1, pt2, g)

    @lru_cache(maxsize=None)
    def countem(code, times, prev='A'):
        if times == 0:
            return len(code)

        tot = 0
        for c in code:
            mn = sys.maxsize
            for path in paths[(prev, c)]:
                x = countem(path, times-1)
                if x < mn:
                    mn = x
            tot += mn
            prev = c

        return tot

    tot1 = tot2 = 0
    for code in codes:
        num = int(code.lstrip('A0').rstrip('A'))
        n1 = countem(code, 3)
        n2 = countem(code, 26)
        tot1 += num * n1
        tot2 += num * n2

    if '1' in sys.argv:
        print(tot1)
    if '2' in sys.argv:
        print(tot2)

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
