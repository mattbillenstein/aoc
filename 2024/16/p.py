#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid, manhattan_distance
from graph import bfs, dfs, dijkstra

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines, {c: i for i, c in enumerate('.#<^>vSEo')})
    return (g,)

def trace(grid, pt, dir, vertices, visited):
    # trace to next junction, return junction and distance
    # from 2023/23
    visited.append(pt)
    dist = 1
    while 1:
        npt = grid.step(pt, dir)
        c = grid.getc(npt)
        if c in ('.', dir):
            pt = npt
            dist += 1
            visited.append(pt)
        elif c == '#':
            found = False
            for ndir in {'^': '<>', 'v': '<>', '<': '^v', '>': '^v'}[dir]:
                npt = grid.step(pt, ndir)
                if npt and npt not in visited and grid.getc(npt) in ('.', ndir):
                    pt = npt
                    dir = ndir
                    dist += 1
                    dist += 1000  # direct turn in path
                    visited.append(pt)
                    found = True
                    break

            if not found:
                return None
        else:
            assert c in '<>v^'
            return None

        if pt in vertices:
            return (pt, dir, dist, visited)

    assert 0

def dfs(start, end, graph, grid, maxdist=0):
    best = [None, maxdist or sys.maxsize]
    visited = set()
    ts = time.time()
    grid = grid.copy()

    def _dfs(pos, dist):
        nonlocal ts
        if time.time() - ts > 10.0:
            ts = time.time()
            g = grid.copy()
            for pt, dir in visited:
                g.setc(pt, dir)
            g.print()
            print(pos, dist)

        if dist > best[1]:
            return

        visited.add(pos)

        if pos[0] == end and dist < best[1]:
            best[0] = list(visited)
            best[1] = dist
            print('BEST', best)
        else:
            for v, d in graph[pos]:
                if v not in visited:
                    _dfs(v, dist + d)

        visited.remove(pos)

    _dfs(start, 0)

    return best


def part1(g):
    g = g.copy()
    if DEBUG:
        g.print()

    # directions and their opposite direction
    dirs = {'<': '>', '>': '<', '^': 'v', 'v': '^'}

    # find start / end and clear
    graph = defaultdict(list)
    for pt in g:
        c = g.getc(pt)
        if c == 'S':
            start = pt
            g.setc(pt, '.')
        elif c == 'E':
            end = pt
            g.setc(pt, '.')

    # compress the grid into a graph, find vertices where we can turn first
    vertices = {start: [], end: []}
    for pt in g:
        if g.getc(pt) != '.':
            continue
        N = sum(1 for _ in g.neighbors4(pt) if g.getc(_) == '.')
        if N > 2:
            vertices[pt] = []

    graph = {}

    # From each vertex, trace in each direction to the next vertex
    for pt, L in vertices.items():
        if pt == end:
            # don't trace from end, we only go to it
            continue
        for dir in dirs:
            npt = g.step(pt, dir)
            if g.getc(npt) == '.':
                x = trace(g, npt, dir, vertices, [pt])
                if x and x[0] != start:  # start is not an end
                    npt, ndir, dist, path = x

                    if npt == end:
                        # add end node to graph ending with this direction
                        graph[(npt, ndir)] = []

                    # add src -> dst vertex mapping if the end direction is
                    # valid or we hit end
                    if g.getc(g.step(npt, ndir)) == '.' or npt == end:
                        graph.setdefault((pt, dir), []).append(((npt, ndir), dist))

                    # if we're not at an end, add nodes ending at this vertex
                    # with a valid turn, dist+1000
                    if npt != end:
                        ndir_opp = dirs[ndir]
                        for turn_dir in dirs:
                            if turn_dir in (ndir, ndir_opp) or g.getc(g.step(npt, turn_dir)) != '.':
                                continue
                            graph.setdefault((pt, dir), []).append(((npt, turn_dir), dist+1000))

    # add nodes from the start if our starting direction isn't available...
    if (start, '>') not in graph:
        for dir in '^v':
            if (start, dir) in graph:
                graph.setdefault((start, '>'), []).extend([(pt, dist+1000) for pt, dist in graph[(start, dir)]])

    # some turns added above go into dead-ends, remove them, but keep nodes to
    # end
    for k, L in graph.items():
        # dead ends
#        for x in L:
#            if x[0] not in graph:
#                print('missing', k, x[0], L)

        L[:] = [_ for _ in L if _[0] in graph or _[0][0] == end]

    # Ok, actual dijkstra
    dist, prev = dijkstra(graph, (start, '>'))

    # min distance to end point, we can end up there from different directions
    # with different costs
    print(min(v for k, v in dist.items() if k[0] == end))

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
