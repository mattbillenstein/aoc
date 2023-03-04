#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return SparseGrid(lines)

def part(grid, part_num):
    if DEBUG:
        grid.print()

    dirs = ['N', 'S', 'W', 'E']

    rnd = 0
    while 1:
        rnd += 1

        # how many elves moved this round
        moved = 0

        # positions elves propose to move to
        propose = defaultdict(list)

        for pt in grid:
            # if elf has no neighbors, don't move
            if all(n not in grid for n in grid.neighbors8(pt)):
                continue
        
            # look through dirs, propose move to adjacent N/W/S/E position if
            # neighbors to that side are empty...
            for dir in dirs:
                if all(n not in grid for n in grid.neighbors8(pt, dir)):
                    nx, ny = grid.step(pt, dir)
                    propose[(nx, ny)].append(pt)
                    break

        # now, move elves that were the only one to propose a position
        for new, L in propose.items():
            if len(L) == 1:
                grid.move(L[0], new)
                moved += 1

        # rotate dirs
        dirs = dirs[1:] + [dirs[0]]

        if part_num == '1':
            if rnd >= 10:
                size = grid.size
                print(size[0] * size[1] - len(grid))
                break

        if part_num == '2':
            if moved == 0:
                print(rnd)
                break

    if DEBUG:
        print()
        grid.print()

def main():
    grid = parse_input()
    part(grid.copy(), '1')
    part(grid.copy(), '2')

if __name__ == '__main__':
    main()
