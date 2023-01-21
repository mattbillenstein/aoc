#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid

DEBUG = '--debug' in sys.argv

EAST = 1
SOUTH = 2

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
#    lines = [int(_) for _ in lines]
    g = Grid(lines, {'.': 0, '>': EAST, 'v': SOUTH})
    return g

def part1(grid):
    grid.print()

    steps = 0
    while 1:
        steps += 1

        moved = False
        for dir in ('>', 'v'):
            if dir == '>':
                vdir = EAST
            else:
                vdir = SOUTH

            move = []
            for pt in grid:
                if grid.get(pt) == vdir:
                    npt = grid.step(pt, dir)

                    # wrap
                    if npt is None:
                        if dir == '>':
                            npt = (0, pt[1])
                        else:
                            npt = (pt[0], 0)

                    if grid.get(npt) == 0:
                        move.append((pt, npt))

            for pt, npt in move:
                grid.set(npt, grid.get(pt))
                grid.set(pt, 0)
                moved = True

        if not moved:
            break

    print()
    grid.print()

    print(steps)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)

if __name__ == '__main__':
    main()
