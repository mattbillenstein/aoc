#!/usr/bin/env pypy3

import copy
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
    return lines

def part1(data):
    g = Grid(data)

    changed = True
    while changed:
        changed = False
        for pt in g:
            if g.getc(pt) == 'O':
                npt = g.step(pt, '^')
                while npt and g.getc(npt) == '.':
                    changed = True
                    g.setc(npt, 'O')
                    g.setc(pt, '.')
                    pt = npt
                    npt = g.step(pt, '^')

    score = g.size[1]
    tot = 0
    for y in range(g.size[1]):
        score = g.size[1] - y
        for x in range(g.size[0]):
            if g.getc((x, y)) == 'O':
                tot += score

    print(tot)


def part2(data):
    g = Grid(data)

    seen = {}
    period = 0
    target = 1_000_000_000
    for i in range(1, 1_000_000_000):
        for dir in '^<v>':
            changed = True
            while changed:
                changed = False
                for pt in g:
                    if g.getc(pt) == 'O':
                        npt = g.step(pt, dir)
                        while npt and g.getc(npt) == '.':
                            changed = True
                            g.setc(npt, 'O')
                            g.setc(pt, '.')
                            pt = npt
                            npt = g.step(pt, dir)

        state = g.hash()
        if state in seen:
            if not period:
                period = i - seen[state]
            else:
                assert period == i - seen[state]

        seen[state] = i

        if period and (target - i) % period == 0:
            break

    score = g.size[1]
    tot = 0
    for y in range(g.size[1]):
        score = g.size[1] - y
        for x in range(g.size[0]):
            if g.getc((x, y)) == 'O':
                tot += score

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
