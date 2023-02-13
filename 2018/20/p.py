#!/usr/bin/env pypy3

import itertools
import json
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
    line = lines[0][1:-1]
    return line

def walk(regex, idx, g, pt):
    startpt = pt

    while idx < len(regex):
        #print()
        #g.print()

        c = regex[idx]
        #print(idx, c, regex[idx-20:idx+20])
        if c in 'NSEW':
            g.remove(pt)
            pt = g.step(pt, c)
            g.setc(pt, '-' if c in 'NS' else '|')
            pt = g.step(pt, c)
            g.setc(pt, 'X')
            for npt in g.neighbors4d(pt):
                g.setc(npt, '#')
            for npt in g.neighbors4(pt):
                if not g.getc(npt):
                    g.setc(npt, '?')
        elif c == '(':
            idx, pt = walk(regex, idx+1, g, pt)
        elif c == '|':
            g.remove(pt)
            pt = startpt
            g.setc(pt, 'X')
        elif c == ')':
            return idx, pt

        idx += 1

def part1(regex):
    print(regex)
    g = SparseGrid([], {'.': 0, '#': 1, '|': 2, '-': 3, '?': 4, 'X': 5})

    pt = (0, 0)
    g.setc(pt, 'X')
    for npt in g.neighbors4d(pt):
        g.setc(npt, '#')
    for npt in g.neighbors4(pt):
        g.setc(npt, '?')

    walk(regex, 0, g, pt)

    for pt in g:
        if g.getc(pt) == '?':
            g.setc(pt, '#')

    print()
    g.print()

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
