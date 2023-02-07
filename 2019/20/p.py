#!/usr/bin/env pypy3

import itertools
import math
import string
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import bfs
from grid import Grid

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n').replace(' ', '#') for _ in sys.stdin]
#    lines = [int(_) for _ in lines]
    chars = {'.': 0, '#': 1}
    for c in string.ascii_uppercase:
        chars[c] = ord(c)
    grid = Grid(lines, chars)
    return grid

def part1(grid):
    grid.print()

    # find labels
    labels = defaultdict(list)

    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if 'A' <= c <= 'Z':
            zpt = None
            c2 = None
            for pt2 in grid.neighbors4(pt):
                v2 = grid.get(pt2)
                if v2 == 0:
                    zpt = pt2
                    continue
                x = chr(v2)
                if 'A' <= x <= 'Z':
                    c2 = x

            if zpt and c2:
                label = ''.join(sorted(c + c2))
                labels[label].append(zpt)

    if DEBUG:
        pprint(labels)

    portals = {}
    for k, L in labels.items():
        if len(L) == 2:
            portals[L[0]] = L[1]
            portals[L[1]] = L[0]
                
    if DEBUG:
        pprint(portals)

    def neighbors(pt):
        L = []
        for npt in grid.neighbors4(pt):
            v = grid.get(npt)
            if v == 0:
                L.append(npt)

        if pt in portals:
            L.append(portals[pt])

        return L

    AA = labels['AA'][0]
    ZZ = labels['ZZ'][0]
    dist = bfs(AA, neighbors, ZZ)

    print(dist)

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
