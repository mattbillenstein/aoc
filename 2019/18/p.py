#!/usr/bin/env pypy3

import itertools
import math
import random
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

    chars = {'.': 0, '#': 1, '@': 64}
    for c in 'abcdefghijklmnopqrstuvwxyz':
        chars[c] = ord(c)
        chars[c.upper()] = ord(c.upper())

    g = Grid(lines, chars)

    return g

def bfs(frontier, grid, end=None):
    # Record key/door position and distance reachable from given point...
    found = []

    if not isinstance(frontier, (list, set)):
        frontier = [(frontier, frozenset())]

    distance = 0
    visited = set()
    while 1:
        next_frontier = set()
        for x, doors in frontier:
            v = grid.get(x)
            c = chr(v)
            if 'a' <= c <= 'z':
                found.append((c, distance, doors))
            elif 'A' <= c <= 'Z':
                doors = doors.union(c.lower())

            visited.add(x)
            for y in grid.neighbors4(x):
                v = grid.get(y)
                if v == 1:
                    continue
                if y not in visited:
                    next_frontier.add((y, doors))

        frontier = next_frontier

        if not frontier:
            return found

        distance += 1

def part1(grid):
    grid.print()

    edges = {}

    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if c == '@':
            grid.set(pt, 0)
            edges[c] = bfs(pt, grid)
        elif 'a' <= c <= 'z':
            grid.set(pt, 0)
            edges[c] = bfs(pt, grid)
            grid.set(pt, v)

    pprint(edges)

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
