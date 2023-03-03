#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    claims = []
    for line in lines:
        for c in '#@,:x':
            line = line.replace(c, ' ')
        tup = [int(_) for _ in line.strip().split()]
        claims.append({'id': tup[0], 'loc': (tup[1], tup[2]), 'size': (tup[3], tup[4])})
    return claims

def part(data):
    d = defaultdict(int)
    for claim in data:
        loc = claim['loc']
        size = claim['size']
        for x in range(loc[0], loc[0] + size[0]):
            for y in range(loc[1], loc[1] + size[1]):
                d[(x, y)] += 1

    print(sum(1 for _ in d.values() if _ >= 2))

    for claim in data:
        loc = claim['loc']
        size = claim['size']
        cnt = 0
        for x in range(loc[0], loc[0] + size[0]):
            for y in range(loc[1], loc[1] + size[1]):
                if d[(x, y)] > 1:
                    cnt += 1
        if not cnt:
            print(claim['id'])
            break

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
