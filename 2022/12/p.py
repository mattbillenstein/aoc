#!/usr/bin/env python3

import sys
import time
from collections import namedtuple

INF = sys.maxsize

letters = 'SabcdefghijklmnopqrstuvwxyzE'

START = letters.index('S')
END = letters.index('E')

Point = namedtuple("Point", "x y")

class Node:
    def __init__(self, x, y, h, dist=INF, prev=None):
        self.x = x
        self.y = y
        self.h = h
        self.dist = dist
        self.prev = prev

    def neighbors(self):
        return [
            (self.x+1, self.y),
            (self.x-1, self.y),
            (self.x,   self.y+1),
            (self.x,   self.y-1),
        ]

    def __repr__(self):
        return f'Node({self.x}, {self.y}, {self.h}, {self.dist})'


def print_grid(grid):
    for row in grid:
        print(''.join(letters[_] for _ in row))


def print_path(node, sizex, sizey):
    grid = [['.'] * sizex for _ in range(sizey)]
    prev = None
    cnt = 0
    while node:
        cnt += 1
        c = '*'
        if node.h == END:
            c = 'E'
        elif not node.prev:
            c = 'S'
        elif prev:
            if node.x < prev.x:
                c = '>'
            elif node.x > prev.x:
                c = '<'
            elif node.y > prev.y:
                c = '^'
            elif node.y < prev.y:
                c = 'v'

        grid[node.y][node.x] = c

        prev = node
        node = node.prev

    print(cnt-1)
    for row in grid:
        print(''.join(row))


def search(grid, startpt, endpt):
    # djikstra's algorithm
    visited = {}
    unvisited = {}

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            unvisited[(x, y)] = Node(x, y, grid[y][x])

    # set start point dist to 0
    unvisited[(startpt.x, startpt.y)].dist = 0
    end_node = unvisited[(endpt.x, endpt.y)]

    while unvisited:
        pt = None
        dist = INF
        for k, n in unvisited.items():
            if n.dist <= dist:
                pt = k
                dist = n.dist

        node = unvisited.pop(pt)

        for x, y in node.neighbors():
            other = unvisited.get((x, y))
            if not other or (other.h - node.h) > 1:
                continue

            alt_dist = node.dist + 1
            if alt_dist < other.dist:
                other.dist = alt_dist
                other.prev = node

                if other is end_node:
                    return other


def main(argv):
    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    grid = []
    for y, line in enumerate(lines):
        row = [letters.index(c) for c in line]
        grid.append(row)
        if START in row:
            startpt = Point(row.index(START), y)
        if END in row:
            endpt = Point(row.index(END), y)

    gridx = len(grid[0])
    gridy = len(grid)

    print(startpt, endpt)

    print_grid(grid)

    # part 1, min distance from start to end...
    node = search(grid, startpt, endpt)

    print()
    print(node)
    print_path(node, gridx, gridy)

    # part 2, consider all starting points elevation 'a' and 'S' as start, what
    # is the min dist from any of these points to end
    min_dist = INF
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c <= letters.index('a'):
                node = search(grid, Point(x, y), endpt)
                if node and node.dist < min_dist:
                    min_dist = node.dist

                if node:
                    print()
                    print(node)
                    print_path(node, gridx, gridy)

    print()
    print(min_dist)


if __name__ == '__main__':
    main(sys.argv)
