#!/usr/bin/env pypy3

import sys

from graph import bfs
from grid import SparseGrid, Point
from algo import picks_shoelace_area

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    directions = []
    for line in lines:
        dir, dist, color = line.split()
        dist = int(dist)
        color = color[2:-1]
        directions.append([dir, dist, color])
    return directions

def part1(directions):
    # build grid and bfs; count set cells
    g = SparseGrid({})
    pt = Point(0, 0)
    for dir, dist, _ in directions:
        for i in range(dist):
            g.set(pt, 1)
            pt = g.step(pt, dir)

    if DEBUG > 1:
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

def fill(edges):
    # scanned left to right, vertical edges pointing up followed by edges
    # pointing down are inside assuming a clockwise path?
    #
    # Scan each Y left to right and take the area of such lines; then we
    # just need to include horizontal lines cononecting Y's in other
    # directions...
    #
    # This reduction could be repeated in X as well, repeating computed area as
    # long as the vertical edges are the same.

    vedges = [_ for _ in edges if _.pt1.x == _.pt2.x]
    hedges = [_ for _ in edges if _.pt1.y == _.pt2.y]

    connectors = set([(_.pt1, _.pt2) for _ in hedges])

    area = 0
    mn, mx = sys.maxsize, 0
    for edge in vedges:
        for pt in edge:
            if pt.y < mn:
                mn = pt.y
            if pt.y > mx:
                mx = pt.y

    for y in range(mn, mx+1):
        # find edges that overlap
        L = [_ for _ in vedges if _.pt1.y <= y <= _.pt2.y]

        # sort by x
        L.sort(key=lambda e: e.pt1.x)

        counted = -10
        for i in range(len(L)-1):
            edge1 = L[i]
            edge2 = L[i+1]

            x1 = edge1.pt1.x
            x2 = edge2.pt1.x

            if edge1.dir == 'U' and edge2.dir == 'D':
                # normal area fill
                area += x2 - x1 + (0 if counted == i-1 else 1)
                counted = i
            elif ((x1, y), (x2, y)) in connectors:
                area += x2 - x1 + (0 if counted == i-1 else 1)
                counted = i

    return area

class Edge:
    def __init__(self, pt1, pt2, dir):
        self.pt1 = pt1
        self.pt2 = pt2
        self.dir = dir

    def __repr__(self):
        return f"Edge({self.pt1.x}, {self.pt1.y}-{self.pt2.y}, {self.dir})"

    def __iter__(self):
        yield self.pt1
        yield self.pt2

def part2a(data):
    # alternate slow scanline fill implementation
    pt = Point(0, 0)
    edges = []
    for dir, dist, color in data:
        # if debug, don't unpack the actual thing... Use the given input.
        if DEBUG == 0:
            dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[color[-1]]
            dist = int(color[:-1], 16)

        if dir == 'U':
            npt = (pt.x, pt.y - dist)
        elif dir == 'D':
            npt = (pt.x, pt.y + dist)
        elif dir == 'R':
            npt = (pt.x + dist, pt.y)
        elif dir == 'L':
            npt = (pt.x - dist, pt.y)
        else:
            assert 0

        if dir in 'UD':
            # order so lesser y coordinate is pt1
            if pt.x <= npt.y:
                edge = Edge(pt, npt, dir)
            else:
                edge = Edge(npt, pt, dir)
        else:
            if pt.x <= npt.x:
                edge = Edge(pt, npt, dir)
            else:
                edge = Edge(npt, pt, dir)

        edges.append(edge)

        pt = npt

    print(fill(edges))

def part2(data):
    # picks formula:
    # i = number of interior points
    # b = number of boundary points
    # Area = i + b/2 - 1

    pt = Point(0, 0)
    vertices = [pt]
    for dir, dist, color in data:
        # if debug, don't unpack the actual thing... Use the given input.
        if DEBUG == 0:
            dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[color[-1]]
            dist = int(color[:-1], 16)

        if dir == 'U':
            npt = Point(pt.x, pt.y - dist)
        elif dir == 'D':
            npt = Point(pt.x, pt.y + dist)
        elif dir == 'R':
            npt = Point(pt.x + dist, pt.y)
        elif dir == 'L':
            npt = Point(pt.x - dist, pt.y)
        else:
            assert 0

        vertices.append(npt)

        pt = npt

    area = picks_shoelace_area(vertices)
    print(area)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)
    if '2a' in sys.argv:
        part2a(data)

if __name__ == '__main__':
    main()
