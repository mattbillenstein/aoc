#!/usr/bin/env pypy3

import sys

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines)

def fill(grid, pt):
    q = [pt]
    found = set()
    border = set()
    while q:
        pt = q.pop()
        found.add(pt)
        for npt in [grid.step(pt, _) for _ in '<>v^']:
            # found the edge, can just abort
            if npt is None:
                return None

            if npt in found:
                continue

            found.add(npt)

            c = grid.getc(npt)
            if c == '.':
                q.append(npt)
            else:
                border.add(npt)

    return border

def parts(grid):
    for pt in grid:
        if grid.getc(pt) == 'S':
            pos = pt
            break

    visited = set()

    dir = '>'
    dist = 0
    while 1:
        visited.add(pt)
        dist += 1
        pt = grid.step(pt, dir)
        c = grid.getc(pt)
        if c == 'J':
            if dir == '>':
                dir = '^'
            else:
                dir = '<'
        elif c == 'F':
            if dir == '^':
                dir = '>'
            else:
                dir = 'v'
        elif c == 'L':
            if dir == '<':
                dir = '^'
            else:
                dir = '>'
        elif c == '7':
            if dir == '>':
                dir = 'v'
            else:
                dir = '<'
        elif c == 'S':
            break

    print(dist // 2)

def main():
    data = parse_input()
    parts(data)

if __name__ == '__main__':
    main()
