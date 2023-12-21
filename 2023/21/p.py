#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import bfs
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'.': 0, '#': 1, 'S': 2, 'O': 3})

def manhattan(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def fill(grid, start, mdist=64, parity=0):
    end = set(_ for _ in grid if grid.get(_) == 0)

    def neighbors(pt):
        for npt in grid.neighbors4(pt):
            if grid.get(npt) == 0:
                yield npt

    # fill entire grid, this will exclude closed-off points
    found = bfs(start, neighbors, end)

    # take points within manhattan distance
    pts = [_[0] for _ in found if _[1] <= mdist]

    # and matching parity
    pts = [_ for _ in pts if manhattan(start, _) % 2 == parity]

    if DEBUG:
        for pt in pts:
            grid.setc(pt, 'O')

        grid.setc(start, 'S')

        grid.print()
    
    return pts

def part1(grid, n=64):
    for pt in grid:
        c = grid.getc(pt)
        if c == 'S':
            start = pt
            grid.setc(pt, '.')
            break

    print(len(fill(grid, start, n)))

def repeat_grid(grid, repeat):
    grid = grid.copy()
    for pt in grid:
        c = grid.getc(pt)
        if c == 'S':
            start = pt
            grid.setc(pt, '.')
            break

    size = grid.size[0]
    assert size == grid.size[1]

    ngrid = Grid([[0] * size * repeat for _ in range(size * repeat)], chars=grid.chars)

    for y in range(0, size * repeat, size):
        for x in range(0, size * repeat, size):
            ngrid.place((x, y), grid)

    nstart = (repeat // 2 * size + start[0], repeat // 2 * size + start[1])

    return ngrid, nstart

def part2a(grid):
    # do a larger fill on the test input and check
    ngrid, nstart = repeat_grid(grid, 20)
    for n in (6, 10, 50, 100): #, 500):
        x = fill(ngrid.copy(), nstart, n)
        print(n, len(x))

def part2(grid):
    size = grid.size[0]
    assert size == grid.size[1]

    ngrid, nstart = repeat_grid(grid, 5)

    x = fill(ngrid.copy(), nstart, ngrid.box[1][0] - nstart[0], 0)
    print(len(x))

    x = fill(ngrid.copy(), nstart, ngrid.box[1][0] - nstart[0], 1)
    print(len(x))

    # now, extract tiles for each parity and calculate expanded grid...

    duh

    N = 26501365

    for pt in grid:
        c = grid.getc(pt)
        if c == 'S':
            start = pt
            grid.setc(pt, '.')
            break

    size = grid.size[0]
    assert size == grid.size[1]

    tiles = N // size

    t = 0
    for y in range(start[1] - tiles * size, start[1] + tiles * size + 1, size):
        for x in range(start[0] - tiles * size, start[0] + tiles * size + 1, size):
            t += 1

    print(t)

    cnt = 0

    assert cnt < 609789877775394 # too high
    assert cnt < 609786863497944

    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))
    if '2a' in sys.argv:
        part2a(copy.deepcopy(data))

if __name__ == '__main__':
    main()
