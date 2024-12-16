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
    print('>>>>>>>>>>>>>>>>>>>>>')
    g.print()

    dirs = {'<': '>', '>': '<', '^': 'v', 'v': '^'}

    graph = defaultdict(list)
    for pt in g:
        c = g.getc(pt)
        if c == 'S':
            start = pt
            g.setc(pt, '.')
        elif c == 'E':
            end = pt
            g.setc(pt, '.')

    # first bfs to get an upper bound on cost so we can better bound dfs
    visited = {}
    def neighbors(pt):
        for npt in g.neighbors4(pt):
            if g.getc(npt) == '.' and npt not in visited:
                visited[npt] = pt
                yield npt
 
    bfs(start, neighbors, end)

    path = []
    pt = end
    while pt != start:
        path.append(pt)
        pt = visited[pt]
    path.append(start)
    path.reverse()

#    for pt in path:
#        g.setc(pt, 'o')
#    g.print()

    maxdist = len(path)
    for i in range(1, len(path)-2):
        if path[i-1][0] != path[i+1][0] and path[i-1][1] != path[i+1][1]:
            maxdist += 1000

    vertices = {start: [], end: []}
    for pt in g:
        if g.getc(pt) != '.':
            continue
        N = sum(1 for _ in g.neighbors4(pt) if g.getc(_) == '.')
        if N > 2:
            vertices[pt] = []

    graph = defaultdict(list)

    for pt, L in vertices.items():
        for dir in dirs:
            npt = g.step(pt, dir)
            if g.getc(npt) == '.':
                x = trace(g, npt, dir, vertices, [pt])
                if x:
                    npt, ndir, dist, path = x
                    graph[(pt, dir)].append(((npt, ndir), dist))

                    # add just turns at npt cost 1000
                    ndir_opp = dirs[ndir]
                    # add cost for turns omitting a 180 and the same dir...
                    for odir in dirs:
                        if odir != ndir_opp and odir != ndir and g.getc(g.step(npt, odir)) == '.':
                            rec = ((npt, odir), 1000)
                            if rec not in graph[(npt, ndir)]:
                                graph[(npt, ndir)].append(((npt, odir), 1000))

    if not graph[(start, '>')]:
        for dir in dirs:
            if dir != '>':
                graph[(start, '>')].append(((start, dir), 1000))

    pprint(graph)
    print()

    print(maxdist)
    best = dfs((start, '>'), end, graph, g, 30000)
    print(best)

    duh
    '''
        if c == '.':
            # if I'm on a tile facing any direction, store neightbors and their
            # cost to the direction they are...
            for current_dir in dirs:
                opp_dir = dirs[current_dir]
                for new_dir in dirs:
                    if new_dir == opp_dir:  # don't allow 180 turn
                        continue
                    npt = g.step(pt, new_dir)
                    c = g.getc(npt)
                    if c == '.':
                        graph[(pt, current_dir)].append( ((npt, new_dir), 1 if current_dir == new_dir else 1001) )
                graph[(pt, current_dir)].sort(key=lambda x: x[1])
    '''

    if DEBUG:
        for pt, dir in best.path:
            g.setc(pt, dir)
        g.print()
        
    print(best)

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
