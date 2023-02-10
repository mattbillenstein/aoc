#!/usr/bin/env pypy3

import itertools
import math
import string
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
#    lines = [int(_) for _ in lines]
    points = []
    for line in lines:
        x, y = line.replace(',', '').split()
        points.append((int(x), int(y)))
    return points

def manhattan(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

def part(points):
    minx = min(_[0] for _ in points) - 5
    maxx = max(_[0] for _ in points) + 5
    miny = min(_[1] for _ in points) - 5
    maxy = max(_[1] for _ in points) + 5

    tot = 0

    # for each point in the bounding box, mark it's closest point or None if
    # equally close to multiple...
    d = {}
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            pt1 = (x, y)
            d[pt1] = None

            dists = []
            for pt2 in points:
                dist = manhattan(pt1, pt2)
                dists.append((dist, pt2))

            dists.sort()
            if dists[0][0] != dists[1][0]:
                d[pt1] = dists[0][1]

            # part2
            if sum(_[0] for _ in dists) < 10000:
                tot += 1

    # count them
    cnts = defaultdict(int)
    for pt1, pt2 in d.items():
        if pt2 is not None:
            cnts[pt2] += 1


    # now remove anything that is infinite - touches an edge...
    for pt1, pt2 in d.items():
        if pt1[0] == 0 or pt1[0] == maxx:
            cnts.pop(pt2, None)
        elif pt1[1] == 0 or pt1[1] == maxy:
            cnts.pop(pt2, None)

    if DEBUG:
        pprint(cnts)
        print(len(cnts))

    # print largest non-infinite area
    mx = max(cnts.values())
    for pt, area in cnts.items():
        if area == mx:
            print(pt, area)

    # part2, size of area where sum of manhattan distance to all points < 10000
    print(tot)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
