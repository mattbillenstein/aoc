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
    def __init__(self, grid, pos, dir, end, steps, visited, cost):
        self.grid = grid
        self.pos = pos
        self.dir = dir
        self.end = end
        self.steps = steps
        self.visited = set(visited)
        self.visited.add(pos)
        self.cost = cost

        self.key = (pos, dir, steps)

    @property
    def done(self):
        return self.pos == self.end

    def next(self):
        for dir in '<>v^':
            npos = self.grid.step(self.pos, dir)
            if npos and not npos in self.visited:
                if dir != self.dir or self.steps < 2:
                    steps = 0 if dir != self.dir else self.steps + 1
                    cost = self.cost + int(self.grid.getc(npos))
                    yield self.__class__(self.grid, npos, dir, self.end, steps, self.visited, cost)

class State2(State):
    @property
    def done(self):
        return self.pos == self.end and self.steps >= 4

    def next(self):
        if self.steps < 3:
            dir = self.dir
            npos = self.grid.step(self.pos, dir)
            if npos:
                steps = self.steps + 1
                cost = self.cost + int(self.grid.getc(npos))
                yield self.__class__(self.grid, npos, dir, self.end, steps, self.visited, cost)
        else:
            for dir in '<>v^':
                npos = self.grid.step(self.pos, dir)
                if npos and not npos in self.visited:
                    if dir != self.dir or self.steps < 9:
                        steps = self.steps + 1
                        if dir != self.dir:
                            steps = 0
                        cost = self.cost + int(self.grid.getc(npos))
                        yield self.__class__(self.grid, npos, dir, self.end, steps, self.visited, cost)

def part1(grid):
    start, end = grid.box
    cost = sys.maxsize
    best = None
    for dir in 'v>':
        state = State(grid, start, dir, end, 0, set(), 0)
        state = dfs(state)
        if state.cost < cost:
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
    start, end = grid.box
    cost = sys.maxsize
    best = None
    for dir in 'v>':
        state = State2(grid, start, dir, end, 0, set(), 0)
        state = dfs(state)
        if state.cost < cost:
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

def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
