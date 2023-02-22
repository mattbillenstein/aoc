#!/usr/bin/env pypy3

import copy
import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    parts = []
    for i, line in enumerate(lines):
        for c in '=<>,pva':
            line = line.replace(c, ' ')
        L = [int(_) for _ in line.split()]
        parts.append({
            'i': i,
            'p': L[:3],
            'v': L[3:6],
            'a': L[6:],
        })
    return parts

def mdist(pt):
    return sum(abs(_) for _ in pt)

def update(part):
    for i in (0, 1, 2):
        part['v'][i] += part['a'][i]
        part['p'][i] += part['v'][i]

def part1(parts):
    # rather arbitrary, but once a particle bubbles up with 0 acceleration and
    # least manhattan distance, it will be the particle that remains the
    # closest thereafter...
    for i in range(1000):
        for part in parts:
            update(part)

    L = [(mdist(_['p']), _) for _ in parts]
    L.sort(key=lambda x: x[0])
    debug(L[0])
    print(L[0][1]['i'])

def part2(parts):
    for i in range(1000):
        d = defaultdict(list)
        for part in parts:
            d[tuple(part['p'])].append(part)

        remove = []
        for k, L in d.items():
            if len(L) > 1:
                remove.extend([_['i'] for _ in L])

        parts = [_ for _ in parts if _['i'] not in remove]

        for part in parts:
            update(part)

    print(len(parts))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
