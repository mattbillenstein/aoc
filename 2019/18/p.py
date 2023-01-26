#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
#    lines = [int(_) for _ in lines]

    chars = {'.': 0, '#': 1, '@': 2}
    for c in 'abcdefghijklmnopqrstuvwxyz':
        chars[c] = ord(c)
        chars[c.upper()] = ord(c.upper())

    g = Grid(lines, chars)

    return g

def bfs(frontier, grid, end=None):
    # neighbors is a function that takes a vertex and yields neighboring
    # vertices...

    found = {}

    if not isinstance(frontier, (list, set)):
        frontier = [frontier]

    distance = 0
    visited = set()
    while 1:
        next_frontier = set()
        for x in frontier:
            v = grid.get(x)
            if v > 2:
                visited.add(x)
                found[chr(v)] = (x, distance)
                continue

            visited.add(x)
            for y in grid.neighbors4(x):
                v = grid.get(y)
                if v == 1:
                    continue
                if y not in visited:
                    next_frontier.add(y)

        frontier = next_frontier

        if not frontier:
            return found

        distance += 1

    return found

def part1(grid):
    grid.print()

    for pt in grid:
        if grid.get(pt) == 2:
            pos = pt
            grid.set(pt, 0)

    found = bfs(pos, grid)
    print(found)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()

