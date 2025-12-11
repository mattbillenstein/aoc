#!/usr/bin/env pypy3

import sys
from functools import lru_cache

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    graph = {}
    for line in lines:
        L = line.replace(':', '').split()
        graph[L[0]] = tuple(L[1:])
    return (graph,)

def part1(graph):
    def trace(node):
        if node == 'out':
            return 1
        return sum(trace(n) for n in graph[node])
    print(trace('you'))

def part2(graph):
    @lru_cache(maxsize=None)
    def trace(node, fft=False, dac=False):
        if node == 'out':
            return 1 if fft and dac else 0
        return sum(trace(n, fft or node == 'fft', dac or node == 'dac') for n in graph[node])
    print(trace('svr'))

def part2a(graph):
    # A solution from reddit I quite like, re-implementing it here for future
    # reference - this is a touch faster

    @lru_cache(maxsize=None)
    def trace(node, end):
        if node == end:
            return 1
        return sum(trace(n, end) for n in graph.get(node, []))

    tot = trace('svr', 'fft') * trace('fft', 'dac') * trace('dac', 'out') + \
          trace('svr', 'dac') * trace('dac', 'fft') * trace('fft', 'out')

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)
    if '2a' in sys.argv:
        part2a(*data)

if __name__ == '__main__':
    main()
