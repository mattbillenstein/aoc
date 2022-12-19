#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split(',')]

def part1(crabs):
    best = (-1, 1e18)
    for pos in range(min(crabs), max(crabs)+1):
        fuel = sum(abs(pos-_) for _ in crabs)
        if fuel < best[1]:
            best = (pos, fuel)
    print(*best)

def part2(crabs):
    best = (-1, 1e18)
    for pos in range(min(crabs), max(crabs)+1):
        # sum 1..N = N(N+1)/2
        fuel = sum(abs(pos-_)*(abs(pos-_)+1)//2 for _ in crabs)
        if fuel < best[1]:
            best = (pos, fuel)
    print(*best)

def main(argv):
    data = parse_input()

    part1(data)
    part2(data)

if __name__ == '__main__':
    main(sys.argv)
