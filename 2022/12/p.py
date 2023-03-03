#!/usr/bin/env pypy3

import sys

from graph import bfs
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'S': ord('a')-1, 'E': ord('z')+1})

def part(grid):
    if DEBUG:
        grid.print()

    As = []
    for pt in grid:
        c = grid.getc(pt)
        if c == 'S':
            start = pt
        elif c == 'E':
            end = pt
        elif c == 'a':
            As.append(pt)

    def neighbors(pt):
        v = grid.get(pt)
        for npt in grid.neighbors4(pt):
            nv = grid.get(npt)
            if nv - v <= 1:
                yield npt

    # part1 min dist S -> E
    dist = bfs(start, neighbors, end)
    print(dist)

    # part2 min dist E -> any 'a'
    dists = [bfs(_, neighbors, end) for _ in As]
    dist = min(_ for _ in dists if _ is not None)
    print(dist)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
