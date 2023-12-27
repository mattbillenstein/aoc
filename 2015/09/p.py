#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    dists = defaultdict(list)
    for line in lines:
        L = line.split()
        c1, c2 = L[0], L[2]
        d = int(L[4])
        dists[c1].append((c2, d))
        dists[c2].append((c1, d))
    return dists

def dfs(start, graph):
    best = [None, sys.maxsize]
    worst = [None, 0]
    visited = set()

    def _dfs(pos, dist):
        visited.add(pos)
        if len(visited) == len(graph):
            if dist < best[1]:
                best[0] = list(visited)
                best[1] = dist
            if dist > worst[1]:
                worst[0] = list(visited)
                worst[1] = dist
        else:
            for v, d in graph[pos]:
                if v not in visited:
                    _dfs(v, dist + d)
        visited.remove(pos)
    _dfs(start, 0)

    return (best, worst)

def part(cities):
    best = [None, sys.maxsize]
    worst = [None, 0]
    for city in cities:
        b, w = dfs(city, cities)
        if b[1] < best[1]:
            best = b
        if w[1] > worst[1]:
            worst = w
    print(best[1])
    print(worst[1])

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
