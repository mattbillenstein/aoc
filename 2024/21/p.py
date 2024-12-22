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

    dx = npt[0] - cpt[0]
    dy = npt[1] - cpt[1]
    cx = '>' if dx > 0 else '<'
    cy = 'v' if dy > 0 else '^'
    dx = abs(dx)
    dy = abs(dy)

    paths = []
    for path in set([cx * dx + cy * dy, cy * dy + cx * dx]):
        valid = True
        pt = cpt
        for dir in path:
            pt = g.step(pt, dir)
            if g.getc(pt) == '#':
                valid = False
                break
        if valid:
            paths.append(path + 'A')

    return paths

def part(codes):
    # use small grids to generate paths
    dg = Grid(['#^A', '<v>'])
    ng = Grid(['789', '456', '123', '#0A'])

    # for each pair of points on each grid, generate the shortest path we can
    # take between them...
    paths = {}
    for g in (dg, ng):
        for pt1 in g:
            c1 = g.getc(pt1)
            if c1 == '#':
                continue
            for pt2 in g:
                c2 = g.getc(pt2)
                if c2 == '#':
                    continue
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
