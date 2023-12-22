#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'
        
class Brick:
    def __init__(self, id, a, b):
        self.a = Point3D(*a)
        self.b = Point3D(*b)
        self.id = id

    @property
    def minx(self):
        return min(self.a.x, self.b.x)
    @property
    def maxx(self):
        return max(self.a.x, self.b.x)
    @property
    def miny(self):
        return min(self.a.y, self.b.y)
    @property
    def maxy(self):
        return max(self.a.y, self.b.y)
    @property
    def minz(self):
        return min(self.a.z, self.b.z)
    @property
    def maxz(self):
        return max(self.a.z, self.b.z)

    def overlaps_xy(self, b):
        return (
            (
                self.minx <= b.minx <= self.maxx or self.minx <= b.maxx <= self.maxx or
                b.minx <= self.minx <= b.maxx or b.minx <= self.maxx <= b.maxx
            ) and (
                self.miny <= b.miny <= self.maxy or self.miny <= b.maxy <= self.maxy or
                b.miny <= self.miny <= b.maxy or b.miny <= self.maxy <= b.maxy
            )
        )

    def move(self, dx=0, dy=0, dz=0):
        for pt in (self.a, self.b):
            pt.x += dx
            pt.y += dy
            pt.z += dz

    def __repr__(self):
        return f'Brick({self.id:04d}, {self.a}, {self.b})'

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    bricks = []
    for i, line in enumerate(lines):
        a, b = line.split('~')
        a = [int(_) for _ in a.split(',')]
        b = [int(_) for _ in b.split(',')]
        bricks.append(Brick(i, a, b))
    return bricks

def pack(bricks):
    # sort by min/max z
    bricks_by_minz = defaultdict(list)
    bricks_by_maxz = defaultdict(list)
    for b in bricks:
        bricks_by_minz[b.minz].append(b)
        bricks_by_maxz[b.maxz].append(b)

    # settle the bricks
    moved = True
    while moved:
        moved = False
        for z, L in sorted(bricks_by_minz.items()):
            if z <= 1:
                continue

            for b in list(L):
                if not any(b.overlaps_xy(_) for _ in bricks_by_maxz[z-1]):
                    #print('move', b)
                    bricks_by_minz[b.minz].remove(b)
                    bricks_by_maxz[b.maxz].remove(b)
                    b.move(dz=-1)
                    bricks_by_minz[b.minz].append(b)
                    bricks_by_maxz[b.maxz].append(b)
                    moved = True

    return bricks_by_maxz, bricks_by_minz

def part1(bricks):
    bricks_by_maxz, bricks_by_minz = pack(bricks)

    disintegrated = []

    for z, L in sorted(bricks_by_maxz.items()):
        # for each brick maxz..
        for b in L:
            # find which bricks it's supporting
            supporting = [_ for _ in bricks_by_minz[b.maxz+1] if b.overlaps_xy(_)]
            # if nothing, we can disintegrate
            if not supporting:
                disintegrated.append(b)
                continue

            # for each brick we're supporting, see how many bricks support it
            needed = False
            for b2 in supporting:
                supported_by = [_ for _ in bricks_by_maxz[b2.minz-1] if b2.overlaps_xy(_)]
                # if only 1, b is essential
                if len(supported_by) == 1:
                    assert supported_by[0] is b
                    needed = True
                    break

            if not needed:
                disintegrated.append(b)

    assert len(disintegrated) < 412, f'{len(disintegrated)} too high'
    print(len(disintegrated))

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
