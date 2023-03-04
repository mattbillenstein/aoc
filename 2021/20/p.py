#!/usr/bin/env pypy3

import sys

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    algo = ['.#'.index(_) for _ in lines[0]]
    grid = lines[2:]
    return grid, algo

def run(grid, algo, times):
    g = SparseGrid(grid)
    if DEBUG:
        g.print()

    ng = g.copy()

    box = g.box
    for i in range(times):
        ng.clear()

        # supposed to be an infinite grid, so the pixels set way outside the
        # grid get cancelled out on the real input, so, just artificially
        # increase the grid every iteration and then trim it back
        for y in range(box[0][1]-times*4, box[1][1]+times*4):
            for x in range(box[0][0]-times*4, box[1][0]+times*4):
                value = 0
                shift = 8
                for ny in range(y-1, y+2):
                    for nx in range(x-1, x+2):
                        value |= g.get((nx, ny)) << shift
                        shift -= 1

                v = algo[value]
                if v:
                    ng.set((x, y), v)
                else:
                    ng.remove((x, y))

        g, ng = ng, g

        if DEBUG:
            print()
            g.print()

    # now trim our inflated box
    for pt in list(g):
        if not (box[0][0]-times*2 <= pt[0] <= box[1][0]+times*2) \
            or not (box[0][1]-times*2 <= pt[1] <= box[1][1]+times*2):
            g.remove(pt)

    if DEBUG:
        print()
        g.print()

    print(sum(g.get(_) for _ in g))

def part1(grid, algo):
    run(grid, algo, 2)

def part2(grid, algo):
    run(grid, algo, 50)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
