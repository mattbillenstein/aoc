#!/usr/bin/env pypy3

import itertools
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    tiles = [tuple(int(_) for _ in line.split(',')) for line in lines]
    return (tiles,)

def normalize(a, b):
    return (min(a[0], b[0]), min(a[1], b[1])), (max(a[0], b[0]), max(a[1], b[1]))

def part1(tiles):
    maxarea = 0
    for a, b in itertools.combinations(tiles, 2):
        a, b = normalize(a, b)
        area = (b[0] - a[0] + 1) * (b[1] - a[1] + 1)
        if area > maxarea:
            maxarea = area
    print(maxarea)

def contains(box, pt):
    return box[0][0] < pt[0] < box[1][0] and box[0][1] < pt[1] < box[1][1]

def part2(tiles):
    maxarea = 0

    edge = set()
    last = tiles[-1]
    for t in tiles:
        a, b = normalize(last, t)
        for x in range(a[0], b[0] + 1):
            for y in range(a[1], b[1] + 1):
                edge.add((x, y))
        last = t

    for a, b in itertools.combinations(tiles, 2):
        a, b = normalize(a, b)
        area = (b[0] - a[0] + 1) * (b[1] - a[1] + 1)
        if area > maxarea and not any(contains([a, b], _) for _ in edge):
            maxarea = area

    print(maxarea)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
