#!/usr/bin/env pypy3

import sys

from graph import dfs_longest
from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'.': 0, '#': 1, 'o': 2})

def trace(grid, pt, dir, vertices, visited):
    # trace to next junction, return junction and distance
    visited.append(pt)
    dist = 1
    while 1:
        npt = grid.step(pt, dir)
        c = grid.getc(npt)
        if c in ('.', dir):
            pt = npt
            dist += 1
            visited.append(pt)
        elif c == '#':
            found = False
            for ndir in {'^': '<>', 'v': '<>', '<': '^v', '>': '^v'}[dir]:
                npt = grid.step(pt, ndir)
                if npt and npt not in visited and grid.getc(npt) in ('.', ndir):
                    pt = npt
                    dir = ndir
                    dist += 1
                    visited.append(pt)
                    found = True
                    break

            if not found:
                return None
        else:
            assert c in '<>v^'
            return None

        if pt in vertices:
            return (pt, dist, visited)

    assert 0

class State:
    def __init__(self, path, end, steps, vertices):
        self.path = path
        self.end = end
        self.steps = steps
        self.vertices = vertices

    @property
    def cost(self):
        return -self.steps

    @property
    def done(self):
        return self.path[-1] == self.end

    def step(self, v, dist):
        return State(self.path + (v,), self.end, self.steps + dist, self.vertices)

    def next(self):
        return [self.step(v, d) for v, d, _ in self.vertices[self.path[-1]] if v not in self.path]

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
                x = trace(grid, npt, dir, vertices, [pt])
                if x:
                    L.append(x)

    s = dfs_longest(State((start,), end, 0, vertices))

    if DEBUG:
        g = grid.copy()
        for i in range(len(s.path)-1):
            v1 = s.path[i]
            v2 = s.path[i+1]
            for pt, dist, L in vertices[v1]:
                if pt == v2:
                    for x in L:
                        g.setc(x, 'o')
        g.print()

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
