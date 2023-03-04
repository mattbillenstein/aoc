#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return SparseGrid(lines)

def part(grid, part_num):
    dirs = ['N', 'S', 'W', 'E']

    rnd = 0
    while 1:
        if DEBUG:
            print()
            grid.print()
            print(len(grid))

        rnd += 1

        # how many elves moved this round
        moved = 0

        # positions elves propose to move to
        propose = defaultdict(list)

        for pt in grid:
            if grid.get(pt):
                # if elf has no neighbors, don't move
                if all(not grid.get(npt) for npt in grid.neighbors8(pt)):
                    continue
            
                # look through dirs, propose move to adjacent N/W/S/E position if
                # neighbors to that side are empty...
                for dir in dirs:
                    if all(not grid.get(npt) for npt in grid.neighbors8(pt, dir)):
                        npt= grid.step(pt, dir)
                        propose[npt].append(pt)
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
                print(sum(1 for _ in grid if not grid.get(_)))
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
    if '1' in sys.argv:
        part(grid.copy(), '1')
    if '2' in sys.argv:
        part(grid.copy(), '2')

if __name__ == '__main__':
    main()
