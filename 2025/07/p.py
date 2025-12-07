#!/usr/bin/env pypy3

import sys
from collections import defaultdict
from functools import lru_cache

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, 'S.|^')

def part(g):
    # trace each pt in grid down one step counting splits and building our
    # adjacency list - this mutates the grid along the way...
    splits = 0
    graph = defaultdict(set)
    for pt in g:  # importantly iterates top row to bottom
        c = g.getc(pt)
        if c in ('S', '|'):
            npt = g.step(pt, 'v')
            if npt:
                nc = g.getc(npt)
                if nc == '.':
                    g.setc(npt, '|')
                    graph[pt].add(npt)
                elif nc == '|':
                    # already got here, but add this to graph coming from other
                    # direction...
                    graph[pt].add(npt)
                elif nc == '^':
                    splits += 1
                    for dir in ('<', '>'):
                        xpt = g.step(npt, dir)
                        if xpt:
                            graph[pt].add(xpt)
                            g.setc(xpt, '|')

    if '1' in sys.argv:
        print(splits)

    if '2' not in sys.argv:
        return

    start = [_ for _ in g if g.getc(_) == 'S'][0]

    @lru_cache(maxsize=None)
    def trace(pt):
        if not graph[pt]:
            return 1
        else:
            return sum(trace(_) for _ in graph[pt])

    print(trace(start))

def main():
    grid = parse_input()
    part(grid)

if __name__ == '__main__':
    main()
