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
        for c in ',=>':
            line = line.replace(c, '')
        line = line.split()
        elements = []
        for i in range(0, len(line), 2):
            n, elem = line[i], line[i+1]
            n = int(n)
            elements.append((elem, n))
        elem, n = elements.pop()
        d[elem] = (n, elements)

    return d

def compute_ore_needed(data, L, n):
    L = [(_[0], _[1] * n) for _ in L]

    extra = defaultdict(int)

    ores = []
    while 1:
        ores += [_ for _ in L if _[0] == 'ORE']
        L = [_ for _ in L if _[0] != 'ORE']
        if not L:
            break

        elem, needed = L.pop()
        if extra[elem] > needed:
            extra[elem] -= needed
            continue
        elif extra[elem]:
            needed -= extra[elem]
            extra[elem] = 0

        produces, needs = data[elem]

        times = math.ceil(needed / produces)
        extra[elem] = times * produces - needed

        for el, n in needs:
            L.append((el, n*times))

    return sum(_[1] for _ in ores)

def part1(data):
    n, L = data['FUEL']
    print(compute_ore_needed(data, L, n))

def part2(data):
    n, L = data['FUEL']
    T = 1_000_000_000_000
    mn = 1
    mx = T
    while (mx - mn) > 10:
        new = mn + (mx-mn)//2
        if compute_ore_needed(data, L, new) < T:
            mn = new
        else:
            mx = new
            
    for n in range(mn, mx):
        if compute_ore_needed(data, L, n) > T:
            break
            
    # prev n would be < T
    n -= 1

    print(n)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
