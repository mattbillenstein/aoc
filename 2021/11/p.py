#!/usr/bin/env pypy3

import copy
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [[int(_) for _ in x] for x in lines]
    return lines

def neighbors(x, y, grid):
    # neighbors here include diagonals...
    for ny in (y-1, y, y+1):
        for nx in (x-1, x, x+1):
            if (nx, ny) != (x, y) and 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                yield nx, ny
    
def flash(grid):
    cells = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] += 1
            if grid[y][x] > 9:
                cells.add((x, y))

    flashes = 0
    while cells:
        x, y = cells.pop()

        grid[y][x] == 0
        flashes += 1

        for nx, ny in neighbors(x, y, grid):
            if grid[ny][nx] == 0:
                continue

            grid[ny][nx] += 1
            if grid[ny][nx] == 10:
                cells.add((nx, ny))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] > 9:
                grid[y][x] = 0

    return flashes

def part1(grid):
#    print('Initial:')
#    for row in grid:
#        print(row)
#    print()

    flashes = 0
    for step in range(100):
        flashes += flash(grid)

#        print(f'Step {step+1}:')
#        for row in grid:
#            print(row)
#        print()

    print(flashes)

def part2(grid):
    for step in range(100000):
        flashes = flash(grid)
        if flashes == 100:
            print(step+1)
            break

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
