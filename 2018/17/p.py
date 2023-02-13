#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import SparseGrid

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = SparseGrid([], {'.': 0, '#': 1, '|': 2, '~': 3, '+': 4})
    for line in lines:
        for c in '=,.':
            line = line.replace(c, ' ')
        L = line.split()

        if L[0] == 'x':
            x0 = x1 = int(L[1])
            y0 = int(L[3])
            y1 = int(L[4])
        elif L[0] == 'y':
            y0 = y1 = int(L[1])
            x0 = int(L[3])
            x1 = int(L[4])

        if 1 or x0 < 570 and y0 < 150:
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    g.setc((x, y), '#')

    return g

def drop(pt, grid, maxy):
    while 1:
        npt = grid.step(pt, 'v')
        if npt[1] > maxy:
            return None

        c = grid.getc(npt)
        if c not in '.|':
            break

        grid.setc(npt, '|')

        pt = npt

    return pt

def fill(startpt, grid, srcs):
    # check we're on something...
    assert grid.get(grid.step(startpt, 'v'), 0)

    scan = {}

    for dir in '<>':
        pt = startpt
        while 1:
            npt = grid.step(pt, dir)
            c = grid.getc(npt)
            if c == '#':
                scan[dir] = ('wall', pt)
                break

            elif c in '.|':
                if grid.getc(grid.step(npt, 'v')) in '.|':
                    scan[dir] = ('drop', npt)
                    break
                pt = npt

    L, R = scan['<'], scan['>']
    c = '|'
    if L[0] == R[0] == 'wall':
        c = '~'

    y = L[1][1]
    for x in range(L[1][0], R[1][0]+1):
        pt = (x, y)
        grid.setc(pt, c)
        if c == '~' and pt in srcs:
            srcs.remove(pt)

    for tup in (L, R):
        if tup[0] == 'drop':
            srcs.add(tup[1])
        
def part1(grid):
    faucet = (500, 0)
    grid.setc(faucet, '+')

    maxy = max(_[1] for _ in grid)

    srcs = set([faucet])

    while 1:
        g = grid.copy()

        if DEBUG:
            print()
            grid.print()

        for pt in list(srcs):
            if pt not in srcs:
                continue

            pt = drop(pt, grid, maxy)
            if pt is None:
                continue

            fill(pt, grid, srcs)

        if g.g == grid.g:
            break

    if 1 or DEBUG:
        print()
        grid.print()

    cnt = 0
    for pt in grid:
        if pt[1] > maxy:
            continue

        c = grid.getc(pt)
        if c in '~|':
            cnt += 1

    print(cnt)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
