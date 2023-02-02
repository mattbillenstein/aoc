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

    chars = {'.': 0, '#': 1, '@': 2}
    for c in 'abcdefghijklmnopqrstuvwxyz':
        chars[c] = ord(c)
        chars[c.upper()] = ord(c.upper())

    g = Grid(lines, chars)

    return g

def bfs(frontier, grid, end=None):
    # Record key/door position and distance reachable from given point...
    found = []

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
                found.append((x, chr(v), distance))
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

last = time.time()
bdist = sys.maxsize
best = {}
def find_keys(grid, pos, keys, all_keys, dist):
    global last, best, bdist

    fs = frozenset(keys)
    if best.get((pos, fs), sys.maxsize) < dist:
        return None

    # recurse until we find all keys
    if keys == all_keys:
        if dist < bdist:
            bdist = dist
        return dist

    doprint = time.time() - last > 10
    if DEBUG or doprint:
        last = time.time()
        grid.print()
        print(pos, keys, dist, bdist)

    found = bfs(pos, grid)
    found.sort(key=lambda x: x[2])

    # if dist + the distance to the furthest key/door > bdist continue
    maxfound = max(_[2] for _ in found)
    if dist + maxfound > bdist:
        return dist + maxfound

    if DEBUG or doprint:
        print(found)
        print()

    mdist = bdist
    for pt, c, fdist in found:
        if dist + fdist > bdist:
            continue

        if 'a' <= c <= 'z':
            grid.set(pt, 0)
            keys.add(c)
            ndist = find_keys(grid, pt, keys, all_keys, dist + fdist)
            if ndist is not None and ndist < mdist:
                mdist = ndist
            keys.remove(c)
            grid.set(pt, ord(c))
        elif 'A' <= c <= 'Z' and c.lower() in keys:
            grid.set(pt, 0)
            ndist = find_keys(grid, pt, keys, all_keys, dist + fdist)
            if ndist < mdist:
                mdist = ndist
            grid.set(pt, ord(c))

    return mdist

def part1(grid):
    grid.print()

    all_keys = set()
    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if v == 2:
            pos = pt
            grid.set(pt, 0)
        elif 'a' <= c <= 'z':
            all_keys.add(c)
#            grid.set(pt, 0)
#            found = bfs(pt, grid)
#            grid.set(pt, v)
#            print(c, pt, found)

    dist = find_keys(grid, pos, set(), all_keys, 0)
    print(dist)

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

