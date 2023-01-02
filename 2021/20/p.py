#!/usr/bin/env pypy3

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

    algo = ['.#'.index(_) for _ in lines[0]]
    grid = lines[2:]
    return grid, algo

def run(grid, algo, times):
    g = SparseGrid(grid)
    if DEBUG:
        g.print()

    box = g.box
    for i in range(times):
        ng = g.copy()
        ng.clear()

        # supposed to be an infinite grid, so the pixels set way outside the
        # grid get cancelled out on the real input, so, just artificially
        # increase the grid every iteration and then trim it back
        for y in range(box[0][1]-times*10, box[1][1]+times*10):
            for x in range(box[0][0]-times*10, box[1][0]+times*10):
                value = 0
                shift = 8
                for ny in range(y-1, y+2):
                    for nx in range(x-1, x+2):
                        value |= g.get((nx, ny), 0) << shift
                        shift -= 1

                v = algo[value]
                if v:
                    ng.set((x, y), v)
                elif (x, y) in ng:
                    ng.remove((x, y))

        g = ng

        if DEBUG:
            print()
            g.print()

    # now trim our inflated box
    for pt in list(g):
        if not (box[0][0]-times*5 <= pt[0] <= box[1][0]+times*5) \
            or not (box[0][1]-times*5 <= pt[1] <= box[1][1]+times*5):
            g.remove(pt)

    if DEBUG:
        print()
        g.print()

    print(sum(g.get(_, 0) for _ in g))

def part1(grid, algo):
    run(grid, algo, 2)

def part2(grid, algo):
    run(grid, algo, 50)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
