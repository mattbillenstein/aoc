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
            # mirror, change dir
            dir = {'v': '>', '>': 'v', '<': '^', '^': '<'}[dir]
        elif c == '/':
            dir = {'v': '<', '>': '^', '<': 'v', '^': '>'}[dir]
        elif c == '|':
            # splitter, trace two other dirs and stop, if we've traced in the
            # new pt/dir already, no need to do it again...
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
    # energized is # of unique points we visited regardless of direction
    return len(set(_[0] for _ in visited))

def part1(grid):
    print(energized(grid))

def part2(grid):
    ul, lr = grid.box
    x1, x2 = ul[0], lr[0]
    y1, y2 = ul[1], lr[1]

    mx = 0

    for y in grid.ys:
        mx = max(energized(grid, (x1, y), '>'), mx)
        mx = max(energized(grid, (x2, y), '<'), mx)

    for x in grid.xs:
        mx = max(energized(grid, (x, y1), 'v'), mx)
        mx = max(energized(grid, (x, y2), '^'), mx)

    print(mx)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
