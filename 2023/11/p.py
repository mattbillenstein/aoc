#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return SparseGrid(lines)

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def part1(grid, N=2):
    # expand
    ngrid = grid.copy()

    sx, sy = ngrid.size

    for y in range(sy-1, -1, -1):
        row = [pt for pt, _ in ngrid.sparse_iter() if pt[1] == y and ngrid.getc(pt) == '#']
        if not row:
            pts = [pt for pt, _ in ngrid.sparse_iter() if pt[1] > y and ngrid.getc(pt) == '#']
            pts.sort(key=lambda pt: (pt[1], pt[0]), reverse=True)
            for pt in pts:
                npt = (pt[0], pt[1] + (N-1))
                ngrid.setc(npt, '#')
                ngrid.setc(pt, '.')
                    
    sx, sy = ngrid.size

    for x in range(sx-1, -1, -1):
        col = [pt for pt, _ in ngrid.sparse_iter() if pt[0] == x and ngrid.getc(pt) == '#']
        if not col:
            pts = [pt for pt, _ in ngrid.sparse_iter() if pt[0] > x and ngrid.getc(pt) == '#']
            pts.sort(reverse=True)
            for pt in pts:
                npt = (pt[0] + (N-1), pt[1])
                ngrid.setc(npt, '#')
                ngrid.setc(pt, '.')

    pts = [pt for pt, _ in ngrid.sparse_iter() if ngrid.getc(pt) == '#']

    tot = 0
    for a, b in itertools.combinations(pts, 2):
        tot += manhattan(a, b)
    print(tot)

    if DEBUG:
        grid.print()
        print()
        ngrid.print()

def part2(data):
    part1(data, 1000000)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data.copy())
    if '2' in sys.argv:
        part2(data.copy())

if __name__ == '__main__':
    main()
