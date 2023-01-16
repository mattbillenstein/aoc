#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from cube import Cube
from grid3d import SparseGrid3D

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
#    lines = [int(_) for _ in lines]
    cubes = []
    for line in lines:
        for s in ('..', 'x=', ',y=', ',z='):
            line = line.replace(s, ' ')
        line = line.replace('on', '1')
        line = line.replace('off', '0')
        tup = tuple([int(_) for _ in line.split()])
        cubes.append(tup)

    return cubes

def part1(data):
    grid = SparseGrid3D(set())
    for tup in data:
        if not all(abs(_) <= 50 for _ in tup):
            debug('Skip', tup)
            continue
        v, x1, x2, y1, y2, z1, z2 = tup

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    grid.set((x, y, z), v)

    cnt = 0
    for pt in grid:
        if grid.get(pt):
            cnt += 1

    print(cnt)

def part2(data):
    cubes = []
    for tup in data:
        if not all(abs(_) <= 50 for _ in tup):
            debug('Skip', tup)
            continue
        v, x1, x2, y1, y2, z1, z2 = tup
        cubes.append(Cube((x1, y1, z1), (x2, y2, z2), v))

#    print(cubes)

    c1 = Cube((0,0,0), (20,20,20), 1)
    c2 = Cube((1,1,1), (3,3,3), 1)
    c3 = Cube((10,10,10), (30,30,30), 1)

    print(c1.contains((1,1,1)))
    print(c1.contains((2,2,2)))
    print(c1.contains((30,30,30)))

    print(c1.intersection(c2))
    print(c2.intersection(c1))

    print(c1.intersection(c3))
    print(c3.intersection(c1))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
