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
        if 0 and not all(abs(_) <= 50 for _ in tup):
            debug('Skip', tup)
            continue
        v, x1, x2, y1, y2, z1, z2 = tup
        cube = Cube((x1, y1, z1), (x2, y2, z2), v)

        for c in cubes:
            if cube.contains_cube(c):
                print('Contains:', cube, c)

        cubes.append(cube)

    with open('cubes.txt', 'w') as f:
        f.write('x0 x1 y0 y1 z0 z1\n')
        for c in cubes:
            if not c.value:
                f.write(f'{c.xs[0]} {c.xs[1]} {c.ys[0]} {c.ys[1]} {c.zs[0]} {c.zs[1]}\n')

    cubes_on = defaultdict(int)
    for cube in cubes:
        if cube.value:
            cubes_on[cube] += cube.volume

    print(sum(cubes_on.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
