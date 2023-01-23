#!/usr/bin/env pypy3

import random
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import bfs
from grid import SparseGrid
from intcode import intcode

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def part(mem):
    prog = intcode(mem)
    next(prog)

    g = SparseGrid([], {'.': 0, '#': 1, 'O': 2, 'X': 3})
    start = (0, 0)
    g.set(start, 3)
    visited = set([start])

    rdir = {'N': 1, 'S': 2, 'W': 3, 'E': 4}
    dir = None
    pos = start
    end = None

    # found this visited size by just letting this run awhile... and printing
    # the grid...
    while len(visited) < 799:
        dir = random.choice([_ for _ in 'NSEW' if _ != dir])
        result = None
        while result is None:
            result = prog.send(rdir[dir])

        npos = g.step(pos, dir)
        if result in (1, 2):
            pos = npos
            visited.add(pos)
        else:
            # set wall and make a random turn
            g.set(npos, 1)

        if result == 2:
            end = pos
            g.set(pos, 2)

    assert end

    if DEBUG:
        print()
        g.print()

    def neighbors(pt):
        for dir in 'NSEW':
            npt = g.step(pt, dir)
            if npt in visited:
                yield npt

    # bfs end to start to find shortest path
    distance = bfs(end, neighbors, start)
    print(distance)

    # to compute time to fill, just BFS with no start point, this returns the
    # shortest path to the point that's furthest away...
    distance = bfs(end, neighbors)
    print(distance)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
