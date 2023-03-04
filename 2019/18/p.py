#!/usr/bin/env pypy3

import sys
import time
from pprint import pprint

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

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
    global _last, best_at

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
        debug(best[0], state)

    for v, d, doors in state.edges[state.pos]:
        if v not in state.keys and state.keys.issuperset(doors):
            s = state.copy()
            s.pos = v
            s.dist += d
            s.keys.add(v)
            dfs(s, best)

def part1(grid):
    if DEBUG:
        grid.print()

    edges = {}
    all_keys = set()

    starts = []
    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if c == '@':
            starts.append(pt)
            grid.set(pt, 0)
            edges[c] = bfs(pt, grid)
            all_keys = set([_[0] for _ in edges[c]])

    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if 'a' <= c <= 'z':
            grid.set(pt, 0)
            edges[c] = bfs(pt, grid)
            grid.set(pt, v)

    if DEBUG:
        pprint(edges)

    state = State('@', 0, set(), all_keys, edges)

    best = [sys.maxsize]
    dfs(state, best)

    print(best[0])

def part2(grid):
    # Min steps with 4 robots - one in each quadrant
    global best_at

    # draw in the cross and 4 start points if there's only one start point...
    if sum(1 for _ in grid if grid.getc(_) == '@') == 1:
        pt = [_ for _ in grid if grid.getc(_) == '@'][0]
        grid.setc(pt, '#')

        grid.setc((pt[0], pt[1]-1), '#')
        grid.setc((pt[0], pt[1]+1), '#')
        grid.setc((pt[0]-1, pt[1]), '#')
        grid.setc((pt[0]+1, pt[1]), '#')

        grid.setc((pt[0]-1, pt[1]-1), '@')
        grid.setc((pt[0]+1, pt[1]-1), '@')
        grid.setc((pt[0]-1, pt[1]+1), '@')
        grid.setc((pt[0]+1, pt[1]+1), '@')

    if DEBUG:
        grid.print()

    points = {}

    starts = []
    for pt in grid:
        v = grid.get(pt)
        c = chr(v)
        if c == '@':
            starts.append(pt)
            grid.set(pt, 0)
        elif 'a' <= c <= 'z':
            points[c] = pt

    tot = 0
    for spt in starts:
        best_at = {}
        edges = {}
        found = bfs(spt, grid)
        all_keys = set([_[0] for _ in found])
        edges['@'] = [(_[0], _[1], _[2].intersection(all_keys)) for _ in found]

        for c, dist, doors in edges['@']:
            pt = points[c]
            grid.set(pt, 0)
            found = bfs(pt, grid)
            grid.set(pt, ord(c))

            # just ignore doors not in this quadrant, assume they'll be
            # unlocked by another robot before we get to them... This doesn't
            # work on the 72-step example (test-p2.txt) - it calculates 70...
            edges[c] = [(_[0], _[1], _[2].intersection(all_keys)) for _ in found]

        if DEBUG:
            pprint(edges)

        state = State('@', 0, set(), all_keys, edges)
        best = [sys.maxsize]
        dfs(state, best)

        tot += best[0]

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
