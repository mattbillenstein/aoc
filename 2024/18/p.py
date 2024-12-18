#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid
from graph import bfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    bytes = [_.split(',') for _ in lines]
    bytes = [(int(_[0]), int(_[1])) for _ in bytes]
    return (bytes,)

def part(points):
    size = (7, 7)
    start = (0, 0)
    end = (6, 6)
    steps = 12
    if len(points) > 1000:
        size = (71, 71)
        end = (70, 70)
        steps = 1024

    g = Grid(['.' * size[0] for _ in range(size[1])], {'.': 0, '#': 1, 'O': 2})

    for i in range(steps):
        g.setc(points[i], '#')

    def neighbors(pt):
        for npt in g.neighbors4(pt):
            if g.getc(npt) == '.':
                yield npt

    x = bfs(start, neighbors, set([end]))

    if '1' in sys.argv:
        if DEBUG:
            g.print()
        print(x[0][1])

    if not '2' in sys.argv:
        return

    for pt in points[1024:]:
        g.setc(pt, '#')
        if not bfs(start, neighbors, set([end])):
            if DEBUG:
                g.print()
            print('%d,%d' % pt)
            break

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
