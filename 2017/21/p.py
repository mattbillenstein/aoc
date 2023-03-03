#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    grids = []
    for line in lines:
        g1, _ , g2 = line.split()
        g1 = Grid(g1.split('/'))
        g2 = Grid(g2.split('/'))
        grids.append((g1, g2))
    return grids

def part1(grids, times=5):
    tiles = {}
    for g1, g2 in grids:
        for i in range(4):
            g1.rotate_cw()
            tiles[g1.hash()] = g2

        g1.flip_x()

        for i in range(4):
            g1.rotate_cw()
            tiles[g1.hash()] = g2

    g = Grid(['.#.', '..#', '###'])

    for i in range(times):
        if DEBUG:
            print()
            print(sum(1 for _ in g if g.get(_)))
            g.print()

        size = g.size[0]

        old, new = 3, 4
        if size % 2 == 0:
            old, new = 2, 3

        newsize = size // old * new
        ng = Grid(['.' * newsize] * newsize)

        for x in range(0, size, old):
            for y in range(0, size, old):
                source = g.slice((x, y), (x+old-1, y+old-1))
                tile = tiles[source.hash()]
                nx, ny = x // old * new, y // old * new
                ng.place((nx, ny), tile)

        g = ng

    print(sum(1 for _ in g if g.get(_)))

    if DEBUG:
        print()
        g.print()

def part2(data):
    part1(data, times=18)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
