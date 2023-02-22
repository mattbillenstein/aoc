#!/usr/bin/env pypy3

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
    return SparseGrid(lines, {'.': 0, '#': 1, 'W': 2, 'F': 3})

def part1(grid):
    g = grid.copy()

    pt = (g.size[0] // 2, g.size[1] // 2)
    dir = '^'
    cnt = 0

    for i in range(10_000):
        v = g.get(pt)
        if v:
            # turn right
            dir = {'^': '>', '>': 'v', 'v': '<', '<': '^'}[dir]
            # clean
            g.set(pt, 0)
        else:
            # turn left
            dir = {'^': '<', '<': 'v', 'v': '>', '>': '^'}[dir]
            # infect
            g.set(pt, 1)
            cnt += 1

        pt = g.step(pt, dir)

    if DEBUG:
        print()
        g.print()
    print(cnt)

def part2(grid):
    g = grid.copy()

    pt = (g.size[0] // 2, g.size[1] // 2)
    dir = '^'
    cnt = 0

    for i in range(10_000_000):
        c = g.getc(pt)
        if c == '.':
            # turn left
            dir = {'^': '<', '<': 'v', 'v': '>', '>': '^'}[dir]
            g.setc(pt, 'W')
        elif c == 'W':
            # no turn
            g.setc(pt, '#')
            cnt += 1
        elif c == '#':
            # turn right
            dir = {'^': '>', '>': 'v', 'v': '<', '<': '^'}[dir]
            g.setc(pt, 'F')
        elif c == 'F':
            # reverse
            dir = {'^': 'v', '>': '<', '<': '>', 'v': '^'}[dir]
            g.setc(pt, '.')
        else:
            assert 0

        pt = g.step(pt, dir)

    if DEBUG:
        print()
        g.print()
    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
