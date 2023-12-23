#!/usr/bin/env pypy3

import sys

from graph import dfs_longest
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'.': 0, '#': 1, 'o': 2})

def trace(grid, pt, dir, vertices, visited):
    # trace to next junction, return junction and distance
    dist = 1
    while 1:
        npt = grid.step(pt, dir)
        c = grid.getc(npt)
        if c in ('.', dir):
            pt = npt
            dist += 1
            visited.add(pt)
        elif c == '#':
            found = False
            for ndir in {'^': '<>', 'v': '<>', '<': '^v', '>': '^v'}[dir]:
                npt = grid.step(pt, ndir)
                if npt and npt not in visited and grid.getc(npt) in ('.', ndir):
                    pt = npt
                    dir = ndir
                    dist += 1
                    visited.add(pt)
                    found = True
                    break

            if not found:
                return None
        else:
            assert c in '<>v^'
            return None

        if pt in vertices:
            return (pt, dist)

    assert 0

class State:
    def __init__(self, pos, end, steps, vertices, visited):
        self.vertices = vertices
        self.pos = pos
        self.end = end
        self.steps = steps
        self.visited = visited

        self.cost = -steps
        self.done = self.pos == end

    def next(self):
        for v, dist in self.vertices[self.pos]:
            if v not in self.visited:
                visited = set(self.visited)
                visited.add(v)
                yield State(v, self.end, self.steps+dist, self.vertices, visited)

    def __repr__(self):
        return f'State({self.pos}, {self.steps})'

def part1(grid):
    # find start / end
    for y in (0, grid.box[1][1]):
        for x in grid.xs:
            if grid.get((x, y)) == 0:
                if y == 0:
                    start = (x, y)
                else:
                    end = (x, y)

    vertices = {start: [], end: []}
    for pt in grid:
        N = sum(1 for _ in grid.neighbors4(pt) if grid.getc(_) != '#')
        if N > 2:
            vertices[pt] = []

    for pt, L in vertices.items():
        for dir in '<>v^':
            npt = grid.step(pt, dir)
            if npt and grid.getc(npt) in ('.', dir):
                x = trace(grid, npt, dir, vertices, set([pt]))
                if x:
                    L.append(x)

    s = dfs_longest(State(start, end, 0, vertices, set()))
    print(s.steps)

def part2(grid):
    # part2, clear directions and search again...
    for pt in grid:
        c = grid.getc(pt)
        if c in '<>v^':
            grid.setc(pt, '.')
    part1(grid)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
