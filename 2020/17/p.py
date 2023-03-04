#!/usr/bin/env pypy3

import sys

from grid import SparseGrid
from grid3d import SparseGrid3D
from grid4d import SparseGrid4D

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = SparseGrid(lines)
    return set([_ for _ in g if g.get(_)])

def part1(data):
    # 2d -> 3d
    data = set((_[0], _[1], 0) for _ in data)

    g = SparseGrid3D(data)
    if DEBUG:
        g.print()

    for i in range(6):
        g2 = g.copy()

        box = g2.box
        for x in range(box[0][0]-1, box[1][0]+2):
            for y in range(box[0][1]-1, box[1][1]+2):
                for z in range(box[0][2]-1, box[1][2]+2):
                    pt = (x, y, z)

                    active = sum(g.get(_, 0) for _ in g.neighbors26(pt))
                    if g.get(pt, 0):
                        if not 2 <= active <= 3:
                            g2.remove(pt)
                    else:
                        if active == 3:
                            g2.add(pt)

        g = g2

        if DEBUG:
            print(f'Cycle {i+1}')
            g.print()

    print(sum(g.get(_, 0) for _ in g))

def part2(data):
    # 2d -> 4d
    data = set((_[0], _[1], 0, 0) for _ in data)

    g = SparseGrid4D(data)
    if DEBUG:
        g.print()

    for i in range(6):
        g2 = g.copy()

        box = g2.box
        for x in range(box[0][0]-1, box[1][0]+2):
            for y in range(box[0][1]-1, box[1][1]+2):
                for z in range(box[0][2]-1, box[1][2]+2):
                    for w in range(box[0][3]-1, box[1][3]+2):
                        pt = (x, y, z, w)

                        active = sum(g.get(_, 0) for _ in g.neighbors80(pt))
                        if g.get(pt, 0):
                            if not 2 <= active <= 3:
                                g2.remove(pt)
                        else:
                            if active == 3:
                                g2.add(pt)

        g = g2

        if DEBUG:
            print(f'Cycle {i+1}')
            g.print()

    print(sum(g.get(_, 0) for _ in g))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
