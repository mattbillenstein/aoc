#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import bfs, dfs_longest
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'.': 0, '#': 1, 'o': 2})

class State:
    def __init__(self, grid, neighbors, pos, end, steps, visited):
        self.grid = grid
        self.neighbors = neighbors
        self.pos = pos
        self.end = end
        self.visited = visited

        self.cost = steps
        self.done = self.pos == end
        self.key = None

    def next(self):
        for npt in self.neighbors[self.pos]:
            if npt not in self.visited:
                visited = set(self.visited)
                visited.add(npt)
                yield State(self.grid, self.neighbors, npt, self.end, self.cost+1, visited)

    def print(self):
        g = self.grid.copy()
        for pt in self.visited:
            if g.getc(pt) == '.':
                g.setc(pt, 'o')
        g.print()

    def __repr__(self):
        return f'State({self.pos}, {self.cost})'

def part1(grid):
    for y in (0, grid.box[1][1]):
        for x in grid.xs:
            if grid.get((x, y)) == 0:
                if y == 0:
                    start = (x, y)
                else:
                    end = (x, y)

    neighbors = {}
    for pt in grid:
        c = grid.getc(pt)
        if c in '<>v^':
            npt = grid.step(pt, c)
            neighbors[pt] = []
            if grid.getc(npt) != '#':
                neighbors[pt].append(npt)
        elif c == '.':
            neighbors[pt] = [_ for _ in grid.neighbors4(pt) if grid.getc(_) in '.<>v^']

    s = dfs_longest(State(grid, neighbors, start, end, 0, set()))

    print()
    g = grid.copy()
    for pt in s.visited:
        g.setc(pt, 'o')
    g.print()
    print(s.cost)

def part2(grid):
    for y in (0, grid.box[1][1]):
        for x in grid.xs:
            if grid.get((x, y)) == 0:
                if y == 0:
                    start = (x, y)
                else:
                    end = (x, y)

    for pt in grid:
        c = grid.getc(pt)
        if c in '<>v^':
            grid.setc(pt, '.')

    vertices = set()
    for pt in grid:
        N = sum(1 for _ in grid.neighbors4(pt) if grid.getc(_) == '.')
        if N > 2:
            vertices.add(pt)

    def neighbors(pt):
        for npt in grid.neighbors4(pt):
            if grid.getc(npt) == '.':
                yield npt

    found = bfs(start, neighbors, vertices)
    found.sort(key=lambda x: x[1])
    for x in found:
        print(x)
    
    pt = (9, 81)
    visited = set()
    s = dfs(State(grid, start, pt, 0, visited))

    print('to end')
    s = dfs(State(grid, pt, end, s.cost, visited))
    
    print(s.cost)


def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
