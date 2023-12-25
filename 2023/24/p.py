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
    xdiff = (line1[0][i] - line1[1][i], line2[0][i] - line2[1][i])
    ydiff = (line1[0][j] - line1[1][j], line2[0][j] - line2[1][j])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def time_intersect(pt, line, coord=0):
    pa, va = line
    if abs(va[coord]) > 1e-6:
        return (pt[coord] - pa[coord]) / va[coord]
    return -1

def add_pts(a, b):
    return tuple(c1 + c2 for c1, c2 in zip(a, b))

def sub_pts(a, b):
    return tuple(c1 - c2 for c1, c2 in zip(a, b))

def feq(fa, fb):
    return abs(fa - fb) < 1e-6

def part1(vecs):
    rangex = (7, 27)
    rangey = (7, 27)
    if len(vecs) > 100:
        rangex = (200000000000000, 400000000000000)
        rangey = (200000000000000, 400000000000000)

    cnt = 0
    for a, b in itertools.combinations(vecs, 2):
        pa, va = a
        pb, vb = b

        it = line_intersection(
            (pa, add_pts(pa, va)),
            (pb, add_pts(pb, vb)),
            (0, 1),
        )
        if it:
            ta = time_intersect(it, a)
            tb = time_intersect(it, b)
            if rangex[0] <= it[0] <= rangex[1] and rangey[0] <= it[1] <= rangey[1] and ta > 0 and tb > 0:
                cnt += 1

    print(cnt)

def part2(vecs):
    # I'm not math smart, so took an idea from Reddit here - brute force dx,
    # dy, dz looking for a velocity vector that intersects some number of the
    # lines in each xy, xz, yz and t. Then find an integer starting point for
    # this vector...

    rng = range(-10, 10)
    if len(vecs) > 100:
        rng = range(-500, 500)

    start = time.time()
    for dx in rng:
#        print(time.time() - start, dx)
        for dy in rng:
            for dz in rng:
                # just compare first 10 lines
                cnt = 0
                vv = (dx, dy, dz)
                for i in range(5):
                    for j in range(i+1, 5):
                        pa, va = vecs[i]
                        pb, vb = vecs[j]

                        # subtract velocity from each line then see if they intersect
                        vap = sub_pts(va, vv)
                        vbp = sub_pts(vb, vv)

                        # compute intersections in each plane
                        line1 = (pa, add_pts(pa, vap))
                        line2 = (pb, add_pts(pb, vbp))

                        ixy = line_intersection(line1, line2, (0, 1))
                        ixz = line_intersection(line1, line2, (0, 2))
                        iyz = line_intersection(line1, line2, (1, 2))

                        if any(_ is None for _ in (ixy, ixz, iyz)):
                            continue

                        # convert back to 3-tuple
                        ixy = ixy + (0,)
                        ixz = (ixz[0], 0, ixz[1])
                        iyz = (0,) + iyz

                        # compare intersection times on opposite axes...
                        matches = 0
                        for it, coords in [(ixy, (0, 1)), (ixz, (0, 2)), (iyz, (1, 2))]:
                            for line in [(pa, vap), (pb, vbp)]:
                                t1 = time_intersect(it, line, coords[0])
                                t2 = time_intersect(it, line, coords[1])
                                if t1 >= 0 and t2 >= 0 and feq(t1, t2):
                                    print(vv, t1, t2)
                                    matches += 1

                        if matches >= 2:
                            cnt += 1

                if 1: #cnt > 18:
                    print(cnt, vv)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
