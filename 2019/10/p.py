#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines, {'.': 0, '#': 1, 'O': 2, 'X': 3})
    return g

def compute_slope(pt1, pt2):
    slope = (pt2[0]-pt1[0], pt2[1]-pt1[1])
    gcd = math.gcd(*slope)
    if gcd > 1:
        slope = (slope[0]//gcd, slope[1]//gcd)
    return slope

def can_see(pt1, pt2, rocks):
    # check all ordinal points in between for a rock
    slope = compute_slope(pt1, pt2)

    pt = pt1
    while 1:
        pt = (pt[0] + slope[0], pt[1] + slope[1])
        if pt == pt2:
            break

        if pt in rocks:
            break

    return pt == pt2

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def compute_angle(src, dst):
    # 0 is up, 90 right, 180 down, 270 left...
    dx, dy = dst[0]-src[0], dst[1]-src[1]
    angle = math.atan2(dy, dx) * 180.0 / math.pi + 90.0
    if angle < 0.0:
        angle = 360.0 + angle
    return angle

def part(grid):
    rocks = set([_ for _ in grid if grid.get(_)])
    seen = defaultdict(set)
    for pt1 in rocks:
        for pt2 in rocks:
            if pt1 == pt2 or pt1 in seen[pt2]:
                continue

            if can_see(pt1, pt2, rocks):
                seen[pt1].add(pt2)
                seen[pt2].add(pt1)

    mxpt = None
    mx = 0
    for pt, L in seen.items():
        if len(L) > mx:
            mx = len(L)
            mxpt = pt

    print(mxpt, mx)

    if DEBUG:
        g = grid.copy()
        g.set(mxpt, 3)
        for pt in rocks:
            if pt == mxpt:
                continue
            if not can_see(mxpt, pt, rocks):
                g.set(pt, 2)
        g.print()

    if DEBUG:
        pts = [
            (mxpt[0],   mxpt[1]-1), # 0
            (mxpt[0]+1, mxpt[1]-1), # 45
            (mxpt[0]+1, mxpt[1]),   # 90
            (mxpt[0]+1, mxpt[1]+1), # 135
            (mxpt[0],   mxpt[1]+1), # 180
            (mxpt[0]-1, mxpt[1]+1), # 225
            (mxpt[0]-1, mxpt[1]),   # 270
            (mxpt[0]-1, mxpt[1]-1), # 315
        ]

        for pt in pts:
            print(mxpt, pt, compute_angle(mxpt, pt))

    # from mxpt, order points by angle, distance
    rocks_sorted = []
    for pt in rocks:
        if pt == mxpt:
            continue

        # quantize the angle to an int, given an angle, we only want to remove
        # the first rock we can see at that angle so we need to compare angles
        # of different rocks...
        angle = int(compute_angle(mxpt, pt) * 1e6)
        dist = manhattan(mxpt, pt)
        rocks_sorted.append((angle, dist, pt))

    rocks_sorted.sort()

    if DEBUG:
        for tup in rocks_sorted:
            print(tup)

    g = grid.copy()
    g.set(mxpt, 3)
    i = 0
    while rocks_sorted:
        if DEBUG:
            print()
            print(len(rocks))
            g.print()

        last_angle = -1
        remove = set()
        for tup in rocks_sorted:
            angle, _, pt = tup
            if angle == last_angle:
                continue

            last_angle = angle
            assert can_see(mxpt, pt, rocks)
            i += 1
            if i == 200:
                print('Vaporize', i, pt, pt[0]*100 + pt[1])
            g.set(pt, 0)
            rocks.remove(pt)
            remove.add(tup)

        rocks_sorted = [_ for _ in rocks_sorted if _ not in remove]

    if DEBUG:
        print()
        print(len(rocks))
        g.print()

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
