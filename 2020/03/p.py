#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines)
    return g

def count_along_slope(grid, dx, dy):
    if DEBUG:
        grid.print()
        print(grid.size)

    cnt = 0
    for y in range(0, grid.size[1], dy):
        if y == 0:
            x = 0
        else:
            x = (x + dx) % grid.size[0]

        if DEBUG:
            print(x, y, dx, dy, grid.get((x, y)))
        if grid.get((x, y)):
            cnt += 1

    return cnt
        
def part1(grid):
    print(count_along_slope(grid, 3, 1))

def part2(data):
    p = 1
    for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        cnt = count_along_slope(data, dx, dy)
        p *= cnt
    print(p)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
