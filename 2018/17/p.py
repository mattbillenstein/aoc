#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = SparseGrid([], {'.': 0, '#': 1, '|': 2, '~': 3, '+': 4})
    for line in lines:
        for c in '=,.':
            line = line.replace(c, ' ')
        L = line.split()

        if L[0] == 'x':
            x0 = x1 = int(L[1])
            y0 = int(L[3])
            y1 = int(L[4])
        elif L[0] == 'y':
            y0 = y1 = int(L[1])
            x0 = int(L[3])
            x1 = int(L[4])

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                g.setc((x, y), '#')

    return g

def drop(pt, grid, maxy):
    # drop down from pt to wall or water and fill visited points with sand
    while 1:
        npt = grid.step(pt, 'v')
        if npt[1] > maxy:
            return None

        c = grid.getc(npt)
        if c not in '.|':
            break

        grid.setc(npt, '|')

        pt = npt

    return pt

def fill(startpt, grid, srcs):
    # check we're on something...
    assert grid.get(grid.step(startpt, 'v'), 0)

    scan = {}

    # scan left and right from given point
    for dir in '<>':
        pt = startpt
        while 1:
            npt = grid.step(pt, dir)
            c = grid.getc(npt)
            if c == '#':
                scan[dir] = ('wall', pt)
                break

            elif c in '.|':
                if grid.getc(grid.step(npt, 'v')) in '.|':
                    scan[dir] = ('drop', npt)
                    break
                pt = npt

    # fill left to right with still water if wall, otherwise sand
    L, R = scan['<'], scan['>']
    c = '|'
    if L[0] == R[0] == 'wall':
        c = '~'

    y = L[1][1]
    for x in range(L[1][0], R[1][0]+1):
        pt = (x, y)
        grid.setc(pt, c)

        # if we set a source to still water, remove it
        if c == '~' and pt in srcs:
            srcs.remove(pt)

    # if we found a new source, add it
    for tup in (L, R):
        if tup[0] == 'drop':
            srcs.add(tup[1])
        
def run(grid):
    miny = min(_[1] for _ in grid)
    maxy = max(_[1] for _ in grid)

    faucet = (500, 0)
    grid.setc(faucet, '+')

    # keep a set of sources where we drop water from, these are added as we
    # fill and spillover and removed as we fill and replace them with still
    # water
    srcs = set([faucet])

    while 1:
        g = grid.copy()

        if DEBUG > 1:
            print()
            grid.print()

        for pt in list(srcs):
            # we modify srcs along the way, make sure pt is still valid
            if pt not in srcs:
                continue

            # drop from the given point, if we fall off the grid, we get
            # None...
            pt = drop(pt, grid, maxy)
            if pt is None:
                continue

            # fill either still water or sand from the given point
            fill(pt, grid, srcs)

        if g.g == grid.g:
            break

    if DEBUG:
        print()
        grid.print()

    # count amount of water/sand
    cnts = defaultdict(int)
    for pt in grid:
        if miny <= pt[1] <= maxy:
            c = grid.getc(pt)
            cnts[c] += 1

    # part1
    print(cnts['~'] + cnts['|'])

    # part2
    print(cnts['~'])

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
