#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from hexgrid import HexSparseGrid

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    directions = []
    for line in lines:
        L = []
        directions.append(L)

        i = 0
        while i < len(line):
            j = i+1
            if line[i] in ('n', 's'):
                j += 1
            L.append(line[i:j].upper())
            i = j

    return directions

def part1(directions):
    g = HexSparseGrid([], {'.': 0, '#': 1, 'O': 100})

    for L in directions:
        pt = (0, 0)
        for step in L:
            pt = g.step(pt, step)

        if g.get(pt):
            g.set(pt, 0)
        else:
            g.set(pt, 1)

    cnt = 0
    for pt in g:
        if g.get(pt):
            cnt += 1
    print(cnt)

#    g.set((0, 0), 100)
    g.print()

    return g

def part2(directions):
    g = part1(directions)

    for i in range(100):
        flip = []
        for y in g.ys:
            for x in g.xs(y):
                pt = (x, y)

                cnt = sum(1 for _ in g.neighbors6(pt) if g.get(_))

                if g.get(pt):
                    # black, flip white if 0 or > 2 black
                    if cnt == 0 or cnt > 2:
                        flip.append(pt)
                else:
                    # white, flip black if exactly 2 black
                    if cnt == 2:
                        flip.append(pt)

        for pt in flip:
            if g.get(pt):
                g.set(pt, 0)
            else:
                g.set(pt, 1)

    cnt = 0
    for pt in g:
        if g.get(pt):
            cnt += 1
    print(i+1, cnt)

    g.print()

def main():
    data = parse_input()
    part2(data)

if __name__ == '__main__':
    main()
