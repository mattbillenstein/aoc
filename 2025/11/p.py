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

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
