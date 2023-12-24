#!/usr/bin/env pypy3

import sys

from grid import Grid
from graph import dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'.': 1})

class State:
    min = 1
    max = 3

    def __init__(self, path, dir, end, steps, cost, grid):
        self.path = path
        self.dir = dir
        self.end = end
        self.steps = steps
        self.cost = cost
        self.grid = grid

    @property
    def key(self):
        return (self.path[-1], self.dir, self.steps)

    @property
    def done(self):
        return self.path[-1] == self.end and self.steps >= self.min

    def next(self):
        # potential speedup, on a turn, jump self.min spaces immediately...
        if self.steps < self.min:
            npos = self.grid.step(self.path[-1], self.dir)
            if npos and npos not in self.path:
                cost = self.cost + int(self.grid.getc(npos))
                yield self.__class__(self.path + (npos,), self.dir, self.end, self.steps + 1, cost, self.grid)
        else:
            for dir in '<>v^':
                npos = self.grid.step(self.path[-1], dir)
                if npos and not npos in self.path:
                    steps = 1
                    if dir == self.dir:
                        steps = self.steps + 1
                    if dir != self.dir or steps <= self.max:
                        cost = self.cost + int(self.grid.getc(npos))
                        yield self.__class__(self.path + (npos,), dir, self.end, steps, cost, self.grid)

class State2(State):
    min = 4
    max = 10

def part1(grid, state_class=State):
    start, end = grid.box
    best = None
    for dir in '>v':
        state = state_class((start,), dir, end, 0, 0, grid)
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

def part2(grid):
    part1(grid, State2)

def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
