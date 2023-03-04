#!/usr/bin/env pypy3

import sys
from pprint import pprint

from graph import bfs, dfs
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines)

class State:
    def __init__(self, path, dist, edges, part):
        self.path = path
        self.dist = dist
        self.edges = edges
        self.part = part

    @property
    def done(self):
        # if we're done
        x = all(_ in self.path for _ in self.edges)
        if self.part == 2:
            x = x and self.path[-1] == '0'
        return x

    @property
    def key(self):
        # the key into the visited dict
        return self.path

    @property
    def cost(self):
        # cost, lower is better
        return self.dist

    def next(self):
        # next states
        pos = self.path[-1]
        found = False
        for c in self.edges:
            if c not in self.path:
                found = True
                dist = self.edges[pos][c]
                yield State(self.path + c, self.dist + dist, self.edges, self.part)

        if not found and pos != '0' and self.part == 2:
            dist = self.edges[pos]['0']
            yield State(self.path + '0', self.dist + dist, self.edges, self.part)

    def __repr__(self):
        return f'State({self.path}, {self.dist}, {self.part})'

def part1(grid, part=1):
    if DEBUG:
        grid.print()

    # collect points of interest
    pts = {}
    for pt in grid:
        c = grid.getc(pt)
        if '0' <= c <= '9':
            pts[pt] = c

    # walk on any non-wall
    def neighbors(pt):
        for npt in grid.neighbors4(pt):
            if grid.getc(npt) != '#':
                yield npt

    # find distances between all points of interest and key by c
    edges = {}
    for pt in grid:
        c = grid.getc(pt)
        if '0' <= c <= '9':
            found = bfs(pt, neighbors, set([_ for _ in pts if _ != pt]))
            edges[c] = {pts[_]: d for _, d in found}

    if DEBUG:
        pprint(edges)

    # initial state
    state = State('0', 0, edges, part)

    best = dfs(state)

    debug(best.path)
    print(best.cost)

def part2(grid):
    part1(grid, 2)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
