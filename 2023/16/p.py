#!/usr/bin/env pypy3

import sys

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines)

def trace(grid, pt, dir, visited):
    while pt:
        visited.add((pt, dir))
        c = grid.getc(pt)
        if c == '\\':
            dir = {'v': '>', '>': 'v', '<': '^', '^': '<'}[dir]
        elif c == '/':
            dir = {'v': '<', '>': '^', '<': 'v', '^': '>'}[dir]
        elif c == '|':
            if dir in '<>':
                for ndir in '^v':
                    npt = grid.step(pt, ndir)
                    if npt and (npt, ndir) not in visited:
                        trace(grid, npt, ndir, visited)
                return
        elif c == '-':
            if dir in 'v^':
                for ndir in '<>':
                    npt = grid.step(pt, ndir)
                    if npt and (npt, ndir) not in visited:
                        trace(grid, npt, ndir, visited)
                return

        # otherwise trace straight
        pt = grid.step(pt, dir)

def energized(grid, pt=(0, 0), dir='>'):
    visited = set()
    trace(grid, pt, dir, visited)
    return len(set(_[0] for _ in visited))

def part1(grid):
    print(energized(grid))

def part2(grid):
    mx = 0
    box = grid.box
    x1, x2 = grid.box[0][0], grid.box[1][0]
    for y in grid.ys:
        n = energized(grid, (x1, y), '>')
        if n > mx:
            mx = n
        n = energized(grid, (x2, y), '<')
        if n > mx:
            mx = n

    y1, y2 = grid.box[0][1], grid.box[1][1]
    for x in grid.xs:
        n = energized(grid, (x, y1), 'v')
        if n > mx:
            mx = n
        n = energized(grid, (x, y2), '^')
        if n > mx:
            mx = n

    print(mx)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
