#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import bfs
from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    directions = []
    for line in lines:
        dir, dist, color = line.split()
        dist = int(dist)
        color = color[2:-1]
        directions.append([dir, dist, color])
    return directions

def is_corner(edge, y):
    return edge[0][1] == y or edge[1][1] == y

def both_corners(edge1, edge2, y):
    return is_corner(edge1, y) and is_corner(edge2, y)

def corners_same_dir(edge1, edge2, y):
    return both_corners(edge1, edge2, y) and \
        ((edge1[0][1] < y and edge2[0][1] < y) or (edge1[1][1] > y and edge2[1][1] > y))

def fill(edges):
    # for every y, fill left to right
    area = 0
    mn = sys.maxsize
    mx = 0
    for pts in edges:
        for pt in pts:
            if pt[1] < mn:
                mn = pt[1]
            if pt[1] > mx:
                mx = pt[1]

    for y in range(mn, mx+1):
        # find edges that overlap
        L = [_ for _ in edges if _[0][1] <= y <= _[1][1]]

        # sort by x
        L.sort()

        inside = False
        for i in range(len(L)-1):
            filled = False
            edge1 = L[i]
            edge2 = L[i+1]

            if corners_same_dir(edge1, edge2, y):
                # fill horizontal edge, still either in or out
                area += edge2[0][0] - edge1[0][0]
                if not inside:
                    area += 1
                filled = True
                print(y, 'fill corners same dir', edge1[0][0], edge2[0][0], area, inside)
            elif both_corners(edge1, edge2, y):
                # fill between corners, if we were outside, now in, if in, still in...
                area += edge2[0][0] - edge1[0][0]
                filled = True
                if not inside:
                    inside = True
                print(y, 'fill both corners', edge1[0][0], edge2[0][0], area, inside)
            elif not is_corner(edge1, y) and not is_corner(edge2, y):
                # standard case, fill of we're transitioning out -> in
                inside = not inside
                if inside:
                    area += edge2[0][0] - edge1[0][0] + 1
                    filled = True
                    print(y, 'fill regular', edge1[0][0], edge2[0][0], area, inside)
            else:
                # came to an edge. fill and flip
                if inside:
                    area += edge2[0][0] - edge1[0][0] + 1
                    filled = True
                    print(y, 'fill normal', edge1[0][0], edge2[0][0], area, inside)
                else:
                    print(y, 'fill skip', edge1[0][0], edge2[0][0], area, inside)
                
                inside = not inside

        print(y, L, area)

    return area

def part1(directions):
    g = SparseGrid({})
    pt = (0, 0)
    for dir, dist, _ in directions:
        for i in range(dist):
            g.set(pt, 1)
            pt = g.step(pt, dir)

    g.print()

    for y in g.ys:
        for x in g.xs:
            if g.get((x, y)) and not g.get((x-1, y)) and not g.get((x+1, y)):
                fillpt = (x+1, y)
                break

    def neighbors(pt):
        g.set(pt, 1)
        L = []
        for npt in g.neighbors4(pt):
            if not g.get(npt):
                L.append(npt)
        return L

    bfs({fillpt}, neighbors)

    cnt = 0
    for pt in g:
        if g.get(pt):
            cnt += 1

    print(cnt)

def part1a(data):
    pt = (0, 0)
    edges = []
    for dir, dist, _ in data:
        if dir == 'U':
            npt = (pt[0], pt[1] - dist)
        elif dir == 'D':
            npt = (pt[0], pt[1] + dist)
        elif dir == 'R':
            npt = (pt[0] + dist, pt[1])
        elif dir == 'L':
            npt = (pt[0] - dist, pt[1])
        else:
            assert 0

        if dir in 'UD':
            if pt[1] <= npt[1]:
                edges.append((pt, npt))
            else:
                edges.append((npt, pt))

        pt = npt

    print(fill(edges))

def part2(data):
    pt = (0, 0)
    edges = []
    for _, _, color in data:
        dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[color[-1]]
        dist = int(color[:-1], 16)

        if dir == 'U':
            npt = (pt[0], pt[1] - dist)
        elif dir == 'D':
            npt = (pt[0], pt[1] + dist)
        elif dir == 'R':
            npt = (pt[0] + dist, pt[1])
        elif dir == 'L':
            npt = (pt[0] - dist, pt[1])
        else:
            assert 0

        # don't need horizontal edges, just vertical...
        if dir in 'UD':
            edges.append((pt, npt))

        pt = npt

#    print(edges)
    print(fill(edges))
        
def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '1a' in sys.argv:
        part1a(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
