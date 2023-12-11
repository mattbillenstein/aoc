#!/usr/bin/env pypy3

import itertools
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    s = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                s.add((x, y))
    return s

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def part1(pts, N=2):
    npts = set(pts)

    for y in range(max(_[1] for _ in npts), -1, -1):
        row = [_ for _ in npts if _[1] == y]
        if not row:
            L = [_ for _ in npts if _[1] > y]
            L.sort(key=lambda pt: (pt[1], pt[0]), reverse=True)
            for pt in L:
                npt = (pt[0], pt[1] + (N-1))
                npts.add(npt)
                npts.remove(pt)

    for x in range(max(_[0] for _ in npts), -1, -1):
        col = [_ for _ in npts if _[0] == x]
        if not col:
            L = [_ for _ in npts if _[0] > x]
            L.sort(reverse=True)
            for pt in L:
                npt = (pt[0] + (N-1), pt[1])
                npts.add(npt)
                npts.remove(pt)

    tot = 0
    for a, b in itertools.combinations(npts, 2):
        tot += manhattan(a, b)
    print(tot)

def part2(data):
    part1(data, 1000000)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data.copy())
    if '2' in sys.argv:
        part2(data.copy())

if __name__ == '__main__':
    main()
