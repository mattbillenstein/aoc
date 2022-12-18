#!/usr/bin/env pypy3

import re
import sys
from collections import defaultdict
from pprint import pprint

MAX_MINUTES = 30

def parse_input(fname):
    with open(fname ) as f:
        lines = [_.strip('\r\n') for _ in f]

    valves = {}
    edges = {}
    for line in lines:
        mobj = re.match('^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([ ,A-Z]+)$', line)
        assert mobj, line
        name, rate, others = mobj.groups()
        others = others.split(', ')

        valves[name] = int(rate)
        edges[name] = {_: 1 for _ in others}

    return valves, edges

def score_path(opened, valves, verbose=False):
    if verbose:
        print(opened)

    score = 0
    for n, m in sorted(opened.items(), key=lambda x: x[1]):
        mins = max(MAX_MINUTES - m, 0)
        x = mins * valves[n]
        score += x
        if verbose:
            print(m, n, mins, valves[n], x, score)

    return score

def search(current, valves, edges, opened, best, minutes):
#    print('search', current, opened, minutes)

    if minutes >= MAX_MINUTES or len(opened) == len(edges):
        score = score_path(opened, valves)
        if score > best[0]:
            print(score, opened)
            score_path(opened, valves, True)
            print()
            best[0] = score

        return

    if current not in opened:
        opened[current] = minutes + 1
        search(current, valves, edges, opened, best, minutes + 1)
        opened.pop(current)
    else:
        for n, dist in sorted(edges[current].items()):
            if n not in opened:
                search(n, valves, edges, opened, best, minutes + dist)

def bfs(frontier, end, edges):
    depth = 1
    while True:
        next_frontier = set()
        for x in frontier:
            if x == end:
                return depth
            for y in edges[x]:
                next_frontier.add(y)
        frontier = next_frontier
        depth += 1

def part1(valves, edges):
    pprint(edges)
    print()
    pprint(valves)

    # I cribbed this part from another solution - basically the key insight is
    # to generate a graph of edges from every non-zero valve to every other
    # one...

    # generate graph from every non-zero valve (plus AA) to every other
    # valve...
    newedges = defaultdict(dict)
    nonzero = [k for k, v in valves.items() if v > 0]
    for v in nonzero + ['AA']:
        for v2 in nonzero:
            if v2 != v:
                newedges[v][v2] = bfs(edges[v], v2, edges)
    edges = dict(newedges)

    print()
    pprint(edges)

    opened = {'AA': 0}
    best = [-1]
    search('AA', valves, edges, opened, best, 0)

    print()
    print(best[0])

def main(argv):
    valves, edges = parse_input(argv[1])

    part1(valves, edges)

if __name__ == '__main__':
    main(sys.argv)
