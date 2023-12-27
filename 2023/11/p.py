#!/usr/bin/env pypy3

import itertools
import sys

from grid import Point, manhattan_distance

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    pts = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                pts.add(Point(x, y))
    return pts

def part1(pts, N=2):
    for y in range(max(_.y for _ in pts), -1, -1):
        row = [_ for _ in pts if _.y == y]
        if not row:
            L = [_ for _ in pts if _.y > y]
            L.sort(key=lambda pt: (pt.y, pt.x), reverse=True)
            for pt in L:
                pts.add(Point(pt.x, pt.y + (N-1)))
                pts.remove(pt)

    for x in range(max(_.x for _ in pts), -1, -1):
        col = [_ for _ in pts if _.x == x]
        if not col:
            L = [_ for _ in pts if _.x > x]
            L.sort(reverse=True)
            for pt in L:
                pts.add(Point(pt.x + (N-1), pt.y))
                pts.remove(pt)

    tot = sum(manhattan_distance(a, b) for a, b in itertools.combinations(pts, 2))
    print(tot)

def part2(pts):
    part1(pts, 1000000)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(set(data))
    if '2' in sys.argv:
        part2(set(data))

if __name__ == '__main__':
    main()
