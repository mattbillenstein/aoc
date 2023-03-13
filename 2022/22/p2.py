#!/usr/bin/env pypy3

import copy
import math
import re
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    grid = SparseGrid(lines[:-2], {' ': 0, '.': 1, '#': 2, '>': 3, '<': 4, 'v': 5, '^': 6})

    directions = re.findall('\d+|[LR]', lines[-1])
    directions = [int(_) if not _ in 'LR' else _ for _ in directions]

    assert ''.join(str(_) for _ in directions) == lines[-1]

    return grid, directions

def part1(grid, directions, translate=None):
    g = grid.copy()

    # start on first tile on the top row facing right
    dir = '>'
    for pt in grid:
        if g.getc(pt) == '.':
            break

    translate = translate or {}
    def move1(grid, pt, dir):
        npt = grid.step(pt, dir)
        c = grid.getc(npt)
        if c == ' ':
            if (pt, dir) not in translate:
                print(pt, dir)
                a, b = grid.box
                if dir == '>':
                    npt = (a[0], pt[1])
                elif dir == '<':
                    npt = (b[0], pt[1])
                elif dir == 'v':
                    npt = (pt[0], a[1])
                elif dir == '^':
                    npt = (pt[0], b[1])

                while not grid.get(npt):
                    npt = grid.step(npt, dir)

                if grid.getc(npt) == '#':
                    npt = pt

                translate[(pt, dir)] = (npt, dir)

            npt, dir =  translate[(pt, dir)]
        elif c == '.':
            pass
        elif c == '#':
            npt = pt

        return npt, dir

    for cmd in directions:
        if cmd in ('L', 'R'):
            dir = {
                'R': {'>': 'v', 'v': '<', '<': '^', '^': '>'},
                'L': {'>': '^', '^': '<', '<': 'v', 'v': '>'},
            }[cmd][dir]

            g.setc(pt, dir)

            if DEBUG:
                print()
                g.print()
        else:
            for i in range(cmd):
                g.set(pt, grid.get(pt))
                pt, dir = move1(grid, pt, dir)
                g.setc(pt, dir)

                if DEBUG:
                    print()
                    g.print()

    if DEBUG:
        print(pt, dir)

    pw = ((pt[1]+1) * 1000) + ((pt[0]+1) * 4) + '>V<^'.index(dir)
    print(pw)

def trace(grid, pt, dir, dist):
    turns = {
        '^': ['<', '>'],
        '>': ['^', 'v'],
        'v': ['>', '<'],
        '<': ['v', '^'],
    }

    pts = []
    for i in range(dist):
        # look in each dir
        dirs = {_: grid.get(grid.step(pt, _)) and 1 for _ in '<>v^'}

        if dirs[dir] and (not pts or not all(dirs[_] for _ in turns[dir])):
            # we can move in same dir, update pt
            pt = grid.step(pt, dir)
        else:
            # off the grid, turn, stay on same pt
            dir = [_ for _ in turns[dir] if dirs[_]][0]

        pts.append((pt, [_ for _ in turns[dir] if grid.get(grid.step(pt, _))][0]))

    return pts

def part2(grid, directions):
    # zip the grid from the concave corners generating a translation dict, and
    # then call part1...

    corners = []
    for pt in grid:
        if grid.get(pt):
            cnt = sum(1 for _ in grid.neighbors8(pt) if grid.get(_))
            if cnt == 7:
                corners.append(pt)

    # there are 3 corners in test and input - is this always the case?
    #
    # there are 12 edges, so 4 per corner, so we simply need to zip 2*size
    # points from each corner?

    # length of side - set points // 6 faces, then sqrt
    size = int(math.sqrt(sum(1 for _ in grid if grid.get(_)) // 6))

    odir = {'<': '>', '>': '<', 'v': '^', '^': 'v'}

    translate = {}
    for pt in corners:
        traces = []
        for npt in grid.neighbors4d(pt):
            if not grid.get(npt):
                if npt[0] > pt[0]:
                    traces.append('>')
                else:
                    traces.append('<')

                if npt[1] > pt[1]:
                    traces.append('v')
                else:
                    traces.append('^')

        for i in range(len(traces)):
            traces[i] = trace(grid, pt, traces[i], size*2)

        for a, b in zip(*traces):
            pt, dir = a
            c = grid.getc(b[0])
            translate[(pt, odir[dir])] = (pt, odir[dir])   # '#' in new pos...
            if c == '.':
                translate[(pt, odir[dir])] = b

            pt, dir = b
            c = grid.getc(a[0])
            translate[(pt, odir[dir])] = (pt, odir[dir])
            if c == '.':
                translate[(pt, odir[dir])] = a

    part1(grid, directions, translate)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*copy.deepcopy(data))
    if '2' in sys.argv:
        part2(*copy.deepcopy(data))

if __name__ == '__main__':
    main()
