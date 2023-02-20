#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    d = {}
    for line in lines:
        line = line.replace(':', '')
        k, v = [int(_) for _ in line.split()]
        d[k] = v
    return d

def sim(layers, delay):
    d = {k: 0 for k in layers}
    inc = {k: 1 for k in layers}
    score = 0

    for _ in range(delay):
        for k in layers:
            if inc[k] == 1 and d[k] == layers[k] - 1:
                inc[k] = -1
            elif inc[k] == -1 and d[k] == 0:
                inc[k] = 1
            d[k] += inc[k]

    for p in range(0, max(d) + 1):
        if p in d and d[p] == 0:
            score += p * layers[p]
            if delay and score:
                break
        
        for k in layers:
            if inc[k] == 1 and d[k] == layers[k] - 1:
                inc[k] = -1
            elif inc[k] == -1 and d[k] == 0:
                inc[k] = 1
            d[k] += inc[k]

    return score

def part1(layers):
    print(sim(layers, 0))

def part2(layers):
    # each scanner has a period of 2n-2 and an offset that eliminates potential
    # starting times that are a multiple of the period...

    L = [(k, v * 2 - 2) for k, v in layers.items()]
    debug(L)
    # print(math.lcm(*[_[1] for _ in L]))
    # 465585120

    for delay in range(465585120):
        if not any((delay + offset) % period == 0 for offset, period in L):
            break

    print(delay)
    assert sim(layers, delay) == 0

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
