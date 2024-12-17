#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import Grid
from graph import PriorityQueue

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines, {c: i for i, c in enumerate('.#<^>vSEO')})
    return (g,)

def dijkstra(graph, start):
    # modified dijkstra to return a set of parent nodes instead of only one
    pq = PriorityQueue()
    dist = {}
    prev = {}
    for v in graph:
        dist[v] = d = 0 if v == start else sys.maxsize
        prev[v] = set()
        pq.add_task(v, d)

    while pq:
        u = pq.pop_task()
        for v, w in graph[u]:
            if v in pq:
                alt = dist[u] + w
                if alt <= dist[v]:
                    pq.add_task(v, alt)
                    dist[v] = alt
                    prev[v].add(u)

    return dist, prev

def part(g):
    if DEBUG:
        g.print()

    # directions and their opposite direction
    dirs = {'<': '>', '>': '<', '^': 'v', 'v': '^'}
    # turn directions
    tdirs = {'>': '^v', '^': '<>', 'v': '<>', '<': '^v'}

    # find start/end and clear
    for pt in g:
        c = g.getc(pt)
        if c in 'SE':
            if c == 'S':
                start = pt
            else:
                end = pt
            g.setc(pt, '.')

    # collect graph edges for each '.'
    graph = defaultdict(list)
    for pt in g:
        c = g.getc(pt)
        if c != '.':
            continue

        for dir, odir in dirs.items():
            # step off the tile in any same direction, cost 1
            npt = g.step(pt, dir)
            if g.getc(npt) == '.':
                # step in same dir, cost 1
                graph[(pt, dir)].append(((npt, dir), 1))

            # turn, cost 1000
            for tdir in tdirs[dir]:
                if g.getc(g.step(pt, tdir)) == '.':
                    # valid turn
                    graph[(pt, dir)].append(((pt, tdir), 1000))

    # add end nodes for end
    ends = []
    for dir, odir in dirs.items():
        if g.getc(g.step(end, dir)) == '.':
            ends.append((end, odir))
            graph[(end, odir)] = []

    if DEBUG > 1:
        for k, v in sorted(graph.items()):
            print(k, v)

    dist, prev = dijkstra(graph, (start, '>'))

    # Part 1
    # min distance to end point, we can end up there from different directions
    # with different costs
    cost = min(v for k, v in dist.items() if k[0] == end)
    if '1' in sys.argv:
        print(cost)

    if '2' not in sys.argv:
        return

    # Part 2, how many tiles are touched by all equal paths
    # Modified dijkstra to return multiple parents for each tile, use dfs from
    # end to start to trace all paths...

    _visited = set()  # must be ordered
    def dfs(pos):
        # dfs tracing backwards end -> start, yields paths start -> end
        _visited.add(pos)
        if pos == (start, '>'):
            L = list(_visited)
            L.reverse()
            yield L
        else:
            for v in prev[pos]:
                if v not in _visited:
                    for p in dfs(v):
                        yield p
        _visited.remove(pos)

    # for each end, dfs to start, compute cost of path, for paths with min
    # cost, add tiles
    tiles = set()
    for e in ends:  # found earlier
        for path in dfs(e):
            assert path[0] == (start, '>')

            t = path[0][1]
            turns = 0
            for pt, dir in path[1:]:
                if dir != t:
                    turns += 1
                    t = dir

            path_cost = len(set(_[0] for _ in path if _[0] != start))
            path_cost += turns * 1000
            if path_cost == cost:
                # matching path, add tiles
                tiles.update([_[0] for _ in path])

    if DEBUG:
        for pt in tiles:
            g.setc(pt, 'O')
        g.print()

    # Output # tiles
    print(len(tiles))

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
