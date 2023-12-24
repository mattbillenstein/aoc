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
    pts = []
    for line in lines:
        pt, vel = line.replace(',', '').split(' @ ')
        pt = tuple([int(_) for _ in pt.split()])
        vel = tuple([int(_) for _ in vel.split()])
        pts.append((pt, vel))
    return pts

def line_intersection(line1, line2):
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

def part1(pts):
    rangex = (7, 27)
    rangey = (7, 27)
    if len(pts) > 100:
        rangex = (200000000000000, 400000000000000)
        rangey = (200000000000000, 400000000000000)

    cnt = 0
    for a, b in itertools.combinations(pts, 2):
        pt1 = a[0][:2]
        s1 = a[1][:2]
        pt2 = b[0][:2]
        s2 = b[1][:2]

        it = line_intersection(
            (pt1, (pt1[0] + s1[0], pt1[1] + s1[1])), 
            (pt2, (pt2[0] + s2[0], pt2[1] + s2[1])), 
        )
        if it:
            ta = (it[0] - pt1[0]) / s1[0]
            tb = (it[0] - pt2[0]) / s2[0]
            if rangex[0] <= it[0] <= rangex[1] and rangey[0] <= it[1] <= rangey[1] and ta > 0 and tb > 0:
                cnt += 1

    print(cnt)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
