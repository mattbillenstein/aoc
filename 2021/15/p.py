#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import dijkstra
from grid import Grid

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

    start, end = zip(*g.box)
    path = dijkstra(graph, start, end)

    printer = Grid([[0] * g.size[0] for _ in range(g.size[1])], {'.': 0, '*': 1})

    for pt, cost in path:
        printer.set(pt, 1)

    printer.print()

    print('Cost:', path[-1][1])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
