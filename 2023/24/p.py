#!/usr/bin/env pypy3

import copy
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
    vecs = []
    for line in lines:
        pt, vel = line.replace(',', '').split(' @ ')
        pt = tuple([int(_) for _ in pt.split()])
        vel = tuple([int(_) for _ in vel.split()])
        vecs.append((pt, vel))
    return vecs

def line_intersection(line1, line2, coords=(0, 1)):
    i, j = coords
    line1 = ((line1[0][i], line1[0][j]), (line1[1][i], line1[1][j]))
    line2 = ((line2[0][i], line2[0][j]), (line2[1][i], line2[1][j]))

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def time_intersect(pt, line):
    assert len(line[0]) == len(line[1]) == 2, line
    pa, va = line
    for i in (0, 1):
        if abs(va[i]) > 1e-6:
            return (pt[i] - pa[i]) / va[i]
    return -1

def add_pts(a, b):
    return tuple(c1 + c2 for c1, c2 in zip(a, b))

def sub_pts(a, b):
    return tuple(c1 - c2 for c1, c2 in zip(a, b))

def feq(fa, fb):
    return abs(fa - fb) < 1e-6

def line_intersections(vecs, coords=(0, 1)):
    i, j = coords
    intersections = []
    for a, b in itertools.combinations(vecs, 2):
        pa, va = a
        pb, vb = b

        it = line_intersection(
            (pa, add_pts(pa, va)),
            (pb, add_pts(pb, vb)),
            coords,
        )
        if it:
            ta = time_intersect(it, ((pa[i], pa[j]), (va[i], va[j])))
            tb = time_intersect(it, ((pb[i], pb[j]), (vb[i], vb[j])))
            if ta >= 0 and tb >= 0:
                intersections.append(it)

    return intersections

def part1(vecs):
    mn, mx = 7, 27
    if len(vecs) > 9:
        mn, mx = 200000000000000, 400000000000000

    ints = line_intersections(vecs)
    print(sum(1 for x, y in ints if mn <= x <= mx and mn <= y <= mx))

def part2(vecs):
    # Following a writeup on Reddit, this is hard problem for me cold, but
    # basically if you brute-force some integer velocity (dx, dy, dz) by
    # subtracting it from the given hailstones velocity (putting them in the
    # frame of reference of the rock) then they should all intersect at some
    # common point - the throwing point.
    #
    # We can speed up the search by looking at X/Y first, then searching Z.

    rng = range(-10, 10)
    if len(vecs) > 100:
        rng = range(-400, 400)  # this is a guess

    candidates = []
    for dx in rng:
        for dy in rng:
            vv = (dx, dy, 0)
            L = [(pt, sub_pts(v, vv)) for pt, v in vecs[:10]]
            ints = line_intersections(L)
            if len(ints) > 1 and all(feq(ints[0][0], _[0]) and feq(ints[0][1], _[1]) for _ in ints):
                x, y = int(ints[0][0]), int(ints[0][1])

                # find Z
                for dz in rng:
                    vv = (dx, dy, dz)
                    L = [(pt, sub_pts(v, vv)) for pt, v in vecs[:10]]
                    xints = line_intersections(L, (0, 2))
                    yints = line_intersections(L, (1, 2))

                    if len(xints) > 1 and all(feq(xints[0][0], _[0]) and feq(xints[0][1], _[1]) for _ in xints) and \
                       len(yints) > 1 and all(feq(yints[0][0], _[0]) and feq(yints[0][1], _[1]) for _ in yints):
                        assert feq(xints[0][1], yints[0][1]), (xints[0], yints[0])
                        z = int(xints[0][1])
                        debug((x, y, z), (dx, dy, dz))
                        print(x + y + z)
                        return

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
