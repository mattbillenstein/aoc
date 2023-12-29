#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import Grid
from graph import dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    grid = Grid(lines, {'.': 1})

    neighbors = defaultdict(list)
    for pt in grid:
        for dir in '<>v^':
            npos = grid.step(pt, dir)
            if npos:
                neighbors[pt].append((npos, dir, int(grid.getc(npos))))
    return neighbors

class State:
    min = 1
    max = 3

    def __init__(self, path, dir, end, steps, cost, neighbors):
        self.path = path
        self.dir = dir
        self.end = end
        self.steps = steps
        self.cost = cost
        self.neighbors = neighbors

    @property
    def key(self):
        return (self.path[-1], self.dir, self.steps)

    @property
    def done(self):
        return self.path[-1] == self.end and self.steps >= self.min

    def next(self):
        # potential speedup, on a turn, jump self.min spaces immediately...
        if self.steps < self.min:
            for npos, ndir, ncost in self.neighbors[self.path[-1]]:
                if npos not in self.path and ndir == self.dir:
                    yield self.__class__(self.path + (npos,), ndir, self.end, self.steps + 1, self.cost + ncost, self.neighbors)
        else:
            for npos, ndir, ncost in self.neighbors[self.path[-1]]:
                if npos not in self.path:
                    if ndir != self.dir or self.steps < self.max:
                        steps = 1 if ndir != self.dir else self.steps + 1
                        yield self.__class__(self.path + (npos,), ndir, self.end, steps, self.cost + ncost, self.neighbors)

class State2(State):
    min = 4
    max = 10

def part1(neighbors, state_class=State):
    start = min(neighbors)
    end = max(neighbors)
    best = None
    for dir in '>v':
        state = state_class((start,), dir, end, 0, 0, neighbors)
        state = dfs(state)
        if not best or state.cost < best.cost:
            best = state

    if DEBUG:
        check = sum(int(grid.getc(_)) for _ in best.visited if _ != start)
        grid.print()
        print()

        for pt in best.visited:
            grid.setc(pt, '.')

        grid.print()
        print(check)

    print(best.cost)

def part2(neighbors):
    part1(neighbors, State2)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
