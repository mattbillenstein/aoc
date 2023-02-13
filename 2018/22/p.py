#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    depth = int(lines[0].split()[1])
    target = tuple([int(_) for _ in lines[1].split()[1].split(',')])
    return depth, target

def generate(depth, target):
    g = Grid([[0] * (target[0]+21) for _ in range(target[1]+21)], {'.': 0, '=': 1, '|': 2, 'M': 10, 'T': 11})

    els = {}
    for pt in g:
        x, y = pt
        if pt == target:
            gi = 0
        elif x == 0:
            gi = y * 48271
        elif y == 0:
            gi = x * 16807
        else:
            gi = els[(x, y-1)] * els[(x-1, y)]

        el = (gi + depth) % 20183
        els[pt] = el
        g.set(pt, el % 3)

    return g

def part1(depth, target):
    g = generate(depth, target)

    if DEBUG:
        print()
        g.print()

    print(sum(g.get(_) for _ in g if _[0] <= target[0] and _[1] <= target[1]))

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
