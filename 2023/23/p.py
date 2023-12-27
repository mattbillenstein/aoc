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

    graph = {k: [_[:2] for _ in L] for k, L in vertices.items()}
    path, dist = dfs_longest(start, end, graph)

    if DEBUG:
        g = grid.copy()
        for i in range(len(path)-1):
            v1 = path[i]
            v2 = path[i+1]
            for pt, d, L in vertices[v1]:
                if pt == v2:
                    for x in L:
                        g.setc(x, 'o')
        g.print()
        print(path)

    print(dist)

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
