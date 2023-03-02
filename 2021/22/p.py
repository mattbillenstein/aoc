#!/usr/bin/env pypy3

import sys

from cube import Cube
from grid3d import SparseGrid3D

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
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
    tot = 0
    cubes = []
    for tup in data:
        if 0 and not all(abs(_) <= 50 for _ in tup):
            debug('Skip', tup)
            continue
        v, x1, x2, y1, y2, z1, z2 = tup
        cube = Cube((x1, y1, z1), (x2, y2, z2), 1 if v else -1)

        to_add = []

        # add if an 'on' cube
        if cube.value == 1:
            to_add.append(cube)

        # for each existing cube, compute intersection and mark it
        # as 'on' (1) or 'off' (-1)
        for c in cubes:
            it = cube.intersection(c)
            if it:
                it.value = -c.value
                to_add.append(it)

        cubes += to_add

    for cube in cubes:
        tot += cube.value * cube.volume

    if DEBUG:
        with open('cubes.txt', 'w') as f:
            f.write('x0 x1 y0 y1 z0 z1\n')
            for c in cubes:
                if c.value == 1:
                    f.write(f'{c.pt1[0]} {c.pt2[0]} {c.pt1[1]} {c.pt2[1]} {c.pt1[2]} {c.pt2[2]}\n')

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
