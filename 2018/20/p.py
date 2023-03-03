#!/usr/bin/env pypy3

import sys

from graph import bfs
from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    line = lines[0][1:-1]
    return line

def walk(regex, idx, g, pt):
    startpt = pt

    while idx < len(regex):
        #print()
        #g.print()

        c = regex[idx]
        #print(idx, c, regex[idx-20:idx+20])
        if c in 'NSEW':
            g.remove(pt)
            pt = g.step(pt, c)
            g.setc(pt, '-' if c in 'NS' else '|')
            pt = g.step(pt, c)
            g.setc(pt, 'X')
            for npt in g.neighbors4d(pt):
                g.setc(npt, '#')
            for npt in g.neighbors4(pt):
                if not g.get(npt):
                    g.setc(npt, '?')
        elif c == '(':
            idx, pt = walk(regex, idx+1, g, pt)
        elif c == '|':
            g.remove(pt)
            pt = startpt
            g.setc(pt, 'X')
        elif c == ')':
            return idx, pt

        idx += 1

    return idx, pt

def run(regex):
    debug(regex)
    g = SparseGrid([], {'.': 0, '#': 1, '|': 2, '-': 3, '?': 4, 'X': 5})

    pt = (0, 0)
    g.setc(pt, 'X')
    for npt in g.neighbors4d(pt):
        g.setc(npt, '#')
    for npt in g.neighbors4(pt):
        g.setc(npt, '?')

    idx, pt = walk(regex, 0, g, pt)
    g.remove(pt)

    for pt in g:
        if g.getc(pt) == '?':
            g.setc(pt, '#')

    if DEBUG:
        print()
        g.print()

    def neighbors(pt):
        return [_ for _ in g.neighbors4(pt) if g.getc(_) in '.|-']

    ends = set()
    for pt in g:
        if g.getc(pt) == '.':
            ends.add(pt)

    pt = (0, 0)
    found = bfs(pt, neighbors, ends)

    # doors passed through is half distance
    print(max(_[1]//2 for _ in found))

    # part2
    print(sum(1 for _ in found if (_[1] // 2) >= 1000))

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
