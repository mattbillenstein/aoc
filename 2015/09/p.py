#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from graph import dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    dists = defaultdict(dict)
    for line in lines:
        L = line.split()
        c1, c2 = L[0], L[2]
        d = int(L[4])
        dists[c1][c2] = d
        dists[c2][c1] = d
    return dists

class State:
    def __init__(self, path, dist, cities):
        self.path = path
        self.dist = dist
        self.cities = cities

    @property
    def done(self):
        # if we're done
        return len(self.path) == len(self.cities)

    @property
    def key(self):
        # the key into the visited dict
        return tuple(self.path)

    @property
    def cost(self):
        # cost, lower is better
        return self.dist

    def next(self):
        # next states
        for c in self.cities:
            if c not in self.path:
                dist = self.cities[self.path[-1]][c] if self.path else 0
                yield self.__class__(self.path + [c], self.dist + dist, self.cities)

    def __repr__(self):
        return f'State({self.path}, {self.dist})'

class State2(State):
    @property
    def cost(self):
        # cost, lower is better
        return -self.dist

def part1(cities):
    best = dfs(State([], 0, cities))
    print(best.dist)

def part2(cities):
    best = dfs(State2([], 0, cities))
    print(best.dist)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
