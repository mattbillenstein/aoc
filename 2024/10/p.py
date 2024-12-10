#!/usr/bin/env pypy3

import sys

from grid import Grid
from graph import bfs

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def search(pt, g, path, paths):
    # find all paths between pt and ends
    path.append(pt)
    v = g.get(pt) + 1
    for npt in g.neighbors4(pt):
        if g.get(npt) == v:
            if v == 9:
                # found an end, push new path
                paths.append(tuple(path) + (npt,))
            else:
                # recurse
                search(npt, g, path, paths)
    path.pop()

def part(data):
    g = Grid(data, chars={_: int(_) for _ in '0123456789'})

    def neighbors(pt):
        v = g.get(pt) + 1
        for npt in g.neighbors4(pt):
            if g.get(npt) == v:
                yield npt

    starts = set()
    ends = set()
    for pt in g:
        if g.get(pt) == 0:
            starts.add(pt)
        if g.get(pt) == 9:
            ends.add(pt)

    # Part 1, find total number of ends reached from each start - simple bfs
    tot = 0
    for pt in starts:
        found = bfs(pt, neighbors, ends)
        tot += len(found)
    print(tot)

    # Part 2, enumerate all paths from each start to any end - recursive dfs
    tot = 0
    for pt in starts:
        paths = []
        search(pt, g, [], paths)
        tot += len(paths)
    print(tot)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
