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
    chars = {'.': 0, '#': 1}
    for c in string.ascii_uppercase:
        chars[c] = ord(c)
    grid = Grid(lines, chars)
    return grid

def find_labels(grid):
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
                labels[label].append((zpt, 0))

    return labels

def part1(grid):
    if DEBUG:
        grid.print()

    labels = find_labels(grid)

    if DEBUG:
        pprint(labels)

    portals = {}
    for k, L in labels.items():
        if len(L) == 2:
            portals[L[0][0]] = L[1][0]
            portals[L[1][0]] = L[0][0]
                
    if DEBUG:
        pprint(portals)

    def neighbors(tup):
        pt, level = tup
        L = []
        for npt in grid.neighbors4(pt):
            v = grid.get(npt)
            if v == 0:
                L.append((npt, level))

        if pt in portals:
            L.append((portals[pt], level))

        return L

    AA = labels['AA'][0]
    ZZ = labels['ZZ'][0]
    dist = bfs(AA, neighbors, ZZ)

    print(dist)

def part2(grid):
    # points include the level so we can visit each point in the grid once per
    # level in bfs
    #
    # ((x, y), level)

    if DEBUG:
        grid.print()

    # find portals out on the outermost edge
    maxx = maxy = -1
    minx = miny = sys.maxsize
    for pt in grid:
        if not grid.get(pt):
            if pt[0] < minx:
                minx = pt[0]
            if pt[0] > maxx:
                maxx = pt[0]

            if pt[1] < miny:
                miny = pt[1]
            if pt[1] > maxy:
                maxy = pt[1]
            
    def portal_out(pt):
        return pt[0] in (minx, maxx) or pt[1] in (miny, maxy)

    def portal_in(pt):
        return not portal_out(pt)

    labels = find_labels(grid)

    if DEBUG:
        pprint(labels)

    portals = {}
    for k, L in labels.items():
        if len(L) == 2:
            portals[L[0][0]] = L[1][0]
            portals[L[1][0]] = L[0][0]
                
    if DEBUG:
        pprint(portals)

    def neighbors(tup):
        pt, level = tup
        L = []
        for npt in grid.neighbors4(pt):
            v = grid.get(npt)
            if v == 0:
                L.append((npt, level))

        if pt in portals:
            if portal_out(pt) and level > 0:
                # going out, decrement level
                L.append((portals[pt], level-1))
            elif portal_in(pt):
                # going in, increment level
                L.append((portals[pt], level+1))

        return L

    AA = labels['AA'][0]
    ZZ = labels['ZZ'][0]
    dist = bfs(AA, neighbors, ZZ)

    print(dist)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
