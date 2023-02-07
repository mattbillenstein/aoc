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

class State:
    def __init__(self, pos, dist, keys, all_keys, edges):
        self.pos = pos
        self.dist = dist
        self.keys = keys
        self.all_keys = all_keys
        self.edges = edges

    def copy(self):
         return State(self.pos, self.dist, set(self.keys), self.all_keys, self.edges)

    def __repr__(self):
        keys = ''.join(self.keys)
        return f'State({self.pos}, {self.dist}, {keys})'

best_at = {}

_last = time.time()
def dfs(state, best):
    global _last

    if state.dist > best[0]:
        return

    if len(state.keys) > 1:
        at = tuple(state.keys)
        at = tuple(sorted(at[:-1])) + (at[-1],)
        bdist = best_at.get(at, sys.maxsize)
        if state.dist > bdist:
            return
        elif state.dist < bdist:
            best_at[at] = state.dist

    if state.keys == state.all_keys:
        if state.dist < best[0]:
            best[0] = state.dist

    if time.time() - _last > 10:
        _last = time.time()
        print(best[0], state)

    for v, d, doors in state.edges[state.pos]:
        if v not in state.keys and state.keys.issuperset(doors):
            s = state.copy()
            s.pos = v
            s.dist += d
            s.keys.add(v)
            dfs(s, best)

def part1(grid):
    grid.print()

    edges = {}
    all_keys = set()

    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if c == '@':
            grid.set(pt, 0)
            edges[c] = bfs(pt, grid)
        elif 'a' <= c <= 'z':
            all_keys.add(c)
            grid.set(pt, 0)
            edges[c] = bfs(pt, grid)
            grid.set(pt, v)

    if DEBUG:
        pprint(edges)

    state = State('@', 0, set(), all_keys, edges)

    best = [sys.maxsize]
    dfs(state, best)

    print(best[0])

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
