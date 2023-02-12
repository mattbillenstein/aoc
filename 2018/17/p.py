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

        if x0 < 550 and y0 < 50:
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    g.setc((x, y), '#')

    return g

def drop(pt, grid, maxy):
    if pt[1] > maxy:
        return None

    npt = grid.step(pt, 'v')
    c = grid.getc(npt)
    if c == '.':
        grid.setc(npt, '|')
        return npt

    return pt

def fill(startpt, grid):
    drops = []

    filled = []

    for dir in '<>':
        pt = startpt
        while 1:
            if grid.getc(grid.step(pt, 'v')) == '.':
                drops.append(pt)
                break

            npt = grid.step(pt, dir)
            c = grid.getc(npt)
            if c in '.|':
                grid.setc(npt, '|')
                filled.append(npt)
                pt = npt
            elif c == '#':
                break
            elif c == '~':
                break

    if not drops:
        for pt in filled + [startpt]:
            grid.setc(pt, '~')

    return drops

def part1(grid):
    faucet = (500, 0)
    grid.setc(faucet, '+')

    grid.print()

    maxy = max(_[1] for _ in grid)

    drops = []
    ndrops = [faucet]

    while 1:
        for pt in ndrops:
            while 1:
                npt = drop(pt, grid, maxy)
                if npt is None or npt == pt:
                    break

                drops.append(npt)
                pt = npt

        while drops:
            ndrops = fill(drops[-1], grid)

            print()
            print(ndrops)
            print(drops)
            grid.print()

            if ndrops:
                break

            drops.pop()

        if all(_[1] > maxy for _ in ndrops):
            break

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
