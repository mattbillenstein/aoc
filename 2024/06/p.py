#!/usr/bin/env pypy3

import copy
import sys
from collections import defaultdict

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

charmap = {'.': 0, '#': 1, '^': 3, '>': 4, 'v': 5, '<': 6, 'O': 7}
dirmap = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

def part1(data):
    g = Grid(data, charmap)
    for pt in g:
        c = g.getc(pt)
        if c == '^':
            dir = c
            break

    g.setc(pt, '.')

    while 1:
        g.setc(pt, dir)
        npt = g.step(pt, dir)
        if npt is None:
            break
        c = g.getc(npt)
        if c == '#':
            dir = dirmap[dir]
        else:
            pt = npt

    # Count points we traversed
    cnt = 0
    for pt in g:
        if g.getc(pt) in dirmap:
            cnt += 1
    print(cnt)

def trace(g, pt, dir, dirs):
    visited = set()

    while 1:
        if (pt, dir) in visited:
            return True

        visited.add((pt, dir))

        dirs[pt].add(dir)
        if DEBUG:
            g.setc(pt, dir)

        npt = g.step(pt, dir)
        if npt is None:
            break

        if dir in dirs[npt]:
            debug('End', npt, dir, dirs[npt])
            return True

        c = g.getc(npt)
        if c == '#':
            dir = dirmap[dir]
        else:
            pt = npt

    return False

def part2(data):
    # 1810 too high

    # place obstructions to force the guard into a loop, if we mark the map
    # as we go, if the position in front of us is empty, but scanning to the
    # right of us is going away from us, putting an obstacle in front of us
    # would put us on the loop...
    g = Grid(data, charmap)
    for pt in g:
        c = g.getc(pt)
        if c == '^':
            dir = c
            break

    g.setc(pt, '.')

    obs = set()
    dirs = defaultdict(set)

    while 1:
        debug(pt, dir, dirs[pt])
        dirs[pt].add(dir)
        if DEBUG:
            g.setc(pt, dir)

        npt = g.step(pt, dir)
        if npt is None:
            break

        c = g.getc(npt)
        if c == '#':
            dir = dirmap[dir]
        else:
            # Could place an obstacle at npt, trace for loop...
            if trace(g, pt, dirmap[dir], copy.deepcopy(dirs)):
                if DEBUG:
                    print()
                    print('Trace', pt, dir, dirmap[dir])
                    g.setc(npt, 'O')
                    g.print()
                    g.setc(npt, '.')
                obs.add(npt)

            pt = npt

    print(len(obs))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
