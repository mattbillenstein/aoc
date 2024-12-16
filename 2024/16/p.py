#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid
from graph import dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines, {c: i for i, c in enumerate('.#<^>vSE')})
    return (g,)

def dfs_shortest(start, end, graph):
    best = [None, sys.maxsize]
    visited = set()

    def _dfs(pos, dist):
        visited.add(pos[0])
        if pos == end and dist < best[1]:
            best[0] = list(visited)
            best[1] = dist
        else:
            for v, d in graph[pos]:
                if v[0] not in visited:
                    _dfs(v, dist + d)
        visited.remove(pos[0])
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
            c = '.'
        elif c == 'E':
            end = pt
            g.setc(pt, '.')
            c = '.'

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

    class State:
        def __init__(self, path, dist):
            self.path = path
            self.dist = dist

        @property
        def done(self):
            return self.path[-1][0] == end

        @property
        def key(self):
            return self.path[-1]

        @property
        def cost(self):
            return self.dist

        def next(self):
            pos = self.path[-1]
            opp = dirs[pos[-1]]

            for ptdir, cost in graph[pos]:
                yield State(self.path + (ptdir,), self.dist + cost)

        def __repr__(self):
            return f'State({self.path}, {self.dist})'

        def print(self):
            x = g.copy()
            for pt, dir in self.path:
                x.setc(pt, dir)
            x.print()

    best = dfs(State(((start, '>'),), 0))

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
