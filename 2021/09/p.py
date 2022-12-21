#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [[int(_) for _ in x] for x in lines]
    return lines

def neighbors(x, y, grid):
    for nx, ny in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            yield nx, ny
    
def flood(x, y, grid):
    if grid[y][x] >= 9:
        return set()

    basin = set([(x, y)])
    visited = set()
    frontier = set([(x, y)])
    while frontier:
        next_frontier = set()
        for x, y in frontier:
            visited.add((x, y))
            for nx, ny in neighbors(x, y, grid):
                if grid[ny][nx] < 9:
                    basin.add((nx, ny))
                    if (nx, ny) not in visited:
                        next_frontier.add((nx, ny))

        frontier = next_frontier

    return basin

def part1(grid):
    lowest = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            found = True
            for nx, ny in neighbors(x, y, grid):
                if grid[y][x] >= grid[ny][nx]:
                    found = False
                    break
            if found:
                lowest.append(grid[y][x])

    print(sum(_+1 for _ in lowest))

def part2(grid):
    basins = []
    visited = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) not in visited:
                basin = flood(x, y, grid)
                if basin:
                    visited |= basin
                    basins.append(basin)

    basins.sort(key=lambda x: len(x))

    print(len(basins[-3]) * len(basins[-2]) * len(basins[-1]))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
