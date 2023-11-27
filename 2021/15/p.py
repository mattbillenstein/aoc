#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from graph import dijkstra
from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [[int(c) for c in line] for line in lines]
    return lines

def part1(data):
    g = Grid(data, {str(_): _ for _ in range(10)})

    graph = defaultdict(list)
    for pt in g:
        for npt in g.neighbors4(pt):
            graph[pt].append((npt, g.get(npt)))

    start, end = g.box
    path = dijkstra(graph, start, end)

    if DEBUG:
        printer = Grid([[0] * g.size[0] for _ in range(g.size[1])], {'.': 0, '*': 1})

        for pt, cost in path:
            printer.set(pt, 1)

        printer.print()

    print(path[-1][1])

def part2(data):
    # grid multiplied to 5x5
    sizey = len(data)
    sizex = len(data[0])

    L = [[0] * sizex * 5 for _ in range(sizey*5)]

    for j in range(5):
        for i in range(5):
            offset = i + j
            for y in range(len(data)):
                for x in range(len(data[y])):
                    nx = x + i*sizex
                    ny = y + j*sizey
                    v = data[y][x] + offset
                    if v > 9:
                        v -= 9
                    L[ny][nx] = v

    part1(L)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
