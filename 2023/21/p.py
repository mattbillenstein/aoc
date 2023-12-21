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

def part1(grid, start=None, mdist=64):
    end = set()
    for pt in grid:
        c = grid.getc(pt)
        if c == 'S':
            if not start:
                start = pt
            grid.setc(pt, '.')
            end.add(pt)
        elif c == '.':
            end.add(pt)

    def neighbors(pt):
        for npt in grid.neighbors4(pt):
            if grid.get(npt) == 0:
                yield npt

    found = bfs([start], neighbors, end)

    ends = set()

    for pt, dist in found:
        if dist < mdist:
            x = bfs([pt], neighbors, end)
            for npt, ndist in x:
                if dist + ndist == mdist:
                    ends.add(npt)

    if 1:
        for pt in ends:
            grid.setc(pt, 'O')
        grid.print()

    print(len(ends))
    return len(ends)

def calc_fill(grid, pt, dist, parity):
    return part
    

def part2(grid):
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

if __name__ == '__main__':
    main()
