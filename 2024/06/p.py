#!/usr/bin/env pypy3

import sys

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

charmap = {'.': 0, '#': 1, '^': 3, '>': 4, 'v': 5, '<': 6, 'O': 7, 'X': 8}
dirmap = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

def trace(g, pt, dir):
    visited = set()
    while 1:
        if (pt, dir) in visited:
            return True
        visited.add((pt, dir))

        npt = g.step(pt, dir)
        if npt is None:
            break
        if g.getc(npt) == '#':
            dir = dirmap[dir]
        else:
            pt = npt

    return False

def part(data):
    g = Grid(data, charmap)
    for pt in g:
        c = g.getc(pt)
        if c in dirmap:
            startpt = pt
            startdir = c
            break

    g.setc(startpt, '.')

    visited = set()

    pt, dir = startpt, startdir
    while 1:
        visited.add(pt)
        #g.setc(pt, dir)
        npt = g.step(pt, dir)
        if npt is None:
            break
        if g.getc(npt) == '#':
            dir = dirmap[dir]
        else:
            pt = npt

    # g.print()

    # part 1
    print(len(visited))

    # part 2
    # For each pt visited in part 1, create an obstruction if there isn't one
    # and trace from the start...
    obs = 0
    for pt in visited:
        if pt == startpt:
            continue
        if g.getc(pt) != '#':
            g.setc(pt, '#')
            if trace(g, startpt, startdir):
                obs += 1
            g.setc(pt, '.')

    print(obs)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
