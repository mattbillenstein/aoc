#!/usr/bin/env pypy3

import itertools
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    tiles = [tuple(int(_) for _ in line.split(',')) for line in lines]
    return (tiles,)

def normalize(a, b):
    return (min(a[0], b[0]), min(a[1], b[1])), (max(a[0], b[0]), max(a[1], b[1]))

def contains(box, pt):
    return box[0][0] < pt[0] < box[1][0] and box[0][1] < pt[1] < box[1][1]

def overlaps(box, line):
    # either end in box, or line span box horizontally, or line span box vertically
    return contains(box, line[0]) or contains(box, line[1]) \
        or (line[0][1] == line[1][1] and line[0][0] <= box[0][0] <= box[1][0] <= line[1][0] and box[0][1] < line[0][1] < box[1][1]) \
        or (line[0][0] == line[1][0] and line[0][1] <= box[0][1] <= box[1][1] <= line[1][1] and box[0][0] < line[0][0] < box[1][0])

def test():
    # contains
    assert overlaps([(0, 0), (10, 10)], [(1, 1), (20, 1)])
    assert overlaps([(0, 0), (10, 10)], [(1, 1), (1, 20)])

    # spans - ends can lie on boundary
    assert overlaps([(0, 0), (10, 10)], [(-1, 1), (20, 1)])
    assert overlaps([(0, 0), (10, 10)], [(1, -1), (1, 20)])
    assert overlaps([(0, 0), (10, 10)], [(0, 1), (20, 1)])
    assert overlaps([(0, 0), (10, 10)], [(1, 0), (1, 20)])

    assert not overlaps([(0, 0), (10, 10)], [(11, 20), (20, 20)])
    assert not overlaps([(0, 0), (10, 10)], [(20, 11), (20, 20)])
    assert not overlaps([(0, 0), (10, 10)], [(-1, 20), (20, 20)])
    assert not overlaps([(0, 0), (10, 10)], [(20, -1), (20, 20)])

def part1(tiles):
    maxarea = 0
    for a, b in itertools.combinations(tiles, 2):
        a, b = normalize(a, b)
        area = (b[0] - a[0] + 1) * (b[1] - a[1] + 1)
        if area > maxarea:
            maxarea = area
    print(maxarea)

def part2(tiles):
    # collect all the edges
    edges = []
    last = tiles[-1]
    for t in tiles:
        a, b = normalize(last, t)
        edges.append([a, b])
        last = t

    maxarea = 0
    for a, b in itertools.combinations(tiles, 2):
        a, b = box = normalize(a, b)
        area = (b[0] - a[0] + 1) * (b[1] - a[1] + 1)
        # faster area test first, then check edge overlaps
        if area > maxarea and not any(overlaps(box, _) for _ in edges):
            maxarea = area
    print(maxarea)

def main():
    data = parse_input()
    if 'test' in sys.argv:
        test()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
