#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import dijkstra
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    depth = int(lines[0].split()[1])
    target = tuple([int(_) for _ in lines[1].split()[1].split(',')])
    return depth, target

def generate(depth, target):
    g = Grid([[0] * (target[0]+21) for _ in range(target[1]+21)], {'.': 0, '=': 1, '|': 2, 'M': 10, 'T': 11, 't': 12, 'c': 13, 'n': 14})

    els = {}
    for pt in g:
        x, y = pt
        if pt == target:
            gi = 0
        elif x == 0:
            gi = y * 48271
        elif y == 0:
            gi = x * 16807
        else:
            gi = els[(x, y-1)] * els[(x-1, y)]

        el = (gi + depth) % 20183
        els[pt] = el
        g.set(pt, el % 3)

    return g

def part1(depth, target):
    g = generate(depth, target)

    if DEBUG:
        print()
        g.print()

    print(sum(g.get(_) for _ in g if _[0] <= target[0] and _[1] <= target[1]))

def part2(depth, target):
    # find shortest (time) path - turn grid into an adjacency list using the
    # given rules/costs and then dijkstra...

    mouth = (0, 0)

    # 0 = neither, 1 = torch, 2 = climbing gear
    valid_tools = {
        # rocky - climbing or torch
        0: (1, 2),
        # wet - climbing or neither
        1: (0, 2),
        # narrow - torch or neither
        2: (0, 1),
    }

    g = generate(depth, target)

    # generate graph, from each point with each valid tool, compute cost to
    # neighboring squares with each valid tool there - bake in tool change
    # cost...
    graph = defaultdict(list)
    for pt in g:
        t1 = g.get(pt)
        for npt in g.neighbors4(pt):
            t2 = g.get(npt)
            for e1 in valid_tools[t1]:
                for e2 in valid_tools[t2]:
                    cost = 1 if e1 == e2 else 8
                    graph[(pt, e1)].append(((npt, e2), cost))

    # search from the mouth with the torch to the target with the torch...
    path = dijkstra(graph, (mouth, 1), (target, 1))

    print(path[-1][1])

    if DEBUG:
        print()
        g.print()

        print()
        print(path, len(path))

        # mark path on the grid using the tool type
        for tup in path:
            k, dist = tup
            pt, e = k
            c = {0: 'n', 1: 't', 2: 'c'}[e]
            g.setc(pt, c)

        g.setc(mouth, 'M')
        g.setc(target, 'T')

        print()
        g.print()

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
