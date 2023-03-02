#!/usr/bin/env pypy3

import sys

from grid import SparseGrid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    brk = lines.index('')
    pts = [_.split(',') for _ in lines[:brk]]
    pts = set([(int(_[0]), int(_[1])) for _ in pts])

    folds = [_.split()[-1].split('=') for _ in lines[brk+1:]]
    folds = [(_[0], int(_[1])) for _ in folds]

    grid = SparseGrid(pts)
    return grid, folds

def fold(grid, folds):
    for axis, z in folds:
        for pt in grid:
            if axis == 'x':
                if pt[0] > z:
                    newpt = (z - (pt[0]-z), pt[1])
                    grid.move(pt, newpt)
            elif axis == 'y':
                if pt[1] > z:
                    newpt = (pt[0], z - (pt[1]-z))
                    grid.move(pt, newpt)

def part1(grid,folds):
    fold(grid, folds[:1])
    print(len(grid))

def part2(grid,folds):
    fold(grid, folds)
    grid.print()

def main():
    grid, folds = parse_input()
    if '1' in sys.argv:
        part1(grid.copy(), folds)
    if '2' in sys.argv:
        part2(grid.copy(), folds)

if __name__ == '__main__':
    main()
