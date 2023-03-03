#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    edges = defaultdict(list)
    for line in lines:
        n1, n2 = line.split('-')
        edges[n1].append(n2)
        edges[n2].append(n1)
    return dict(edges)

def is_small_cave(node):
    return node.lower() == node

def dfs(path, end, edges, discovered, paths, visit_twice=None):
    node = path[-1]
    if node == end:
        paths.append(tuple(path))
        return

    discovered[node] += 1
 
    # do for every edge (v, u)
    for u in edges[node]:
        if u == 'start':
            continue
        is_small = is_small_cave(u)
        if not is_small or discovered[u] < (2 if u == visit_twice else 1):
            path.append(u)
            dfs(path, end, edges, discovered, paths, visit_twice)
            path.pop()

    discovered[node] -= 1

def part1(edges):
    paths = []
    
    dfs(['start'], 'end', edges, defaultdict(int), paths)

    if DEBUG:
        for path in paths:
            print(','.join(path))

    print(len(paths))

def part2(edges):
    paths = []
    
    # iterate dfs for every small cave we visit twice and unique paths after...
    for node in edges:
        if not node in ('start', 'end') and is_small_cave(node):
            dfs(['start'], 'end', edges, defaultdict(int), paths, visit_twice=node)

    paths = sorted(set(paths))
    if DEBUG:
        for path in paths:
            print(','.join(path))

    print(len(paths))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
