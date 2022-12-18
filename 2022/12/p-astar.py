#!/usr/bin/env python3

import sys
import time
from collections import namedtuple

last = 0

letters = 'SabcdefghijklmnopqrstuvwxyzE'

START = letters.index('S')
END = letters.index('E')

Point = namedtuple("Point", "x y")

class Node:
    def __init__(self, x, y, h, parent, cost_start, cost_end):
        self.x = x
        self.y = y
        self.h = h
        self.parent = parent
        self.cost_start = cost_start
        self.cost_end = cost_end

    @property
    def cost(self):
        return self.cost_start # + self.cost_end

    def neighbors(self):
        return [
            (self.x+1, self.y),
            (self.x-1, self.y),
            (self.x,   self.y+1),
            (self.x,   self.y-1),
        ]

    def __repr__(self):
        return f'Node({self.x}, {self.y}, {self.h}, {self.cost})'

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
        elif node.h == START:
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
        node = node.parent

    print()
    print(cnt-1)
    for row in grid:
        print(''.join(row))


def search(grid, startpt, endpt):
    # https://web.archive.org/web/20171022224528/http://www.policyalmanac.org:80/games/aStarTutorial.htm
    global last

    gridx = len(grid[0])
    gridy = len(grid)

    nodes = {}
    open = []
    closed = set()

    n = Node(
        startpt.x,
        startpt.y,
        grid[startpt.y][startpt.x],
        None,
        0,
        abs(endpt.x - startpt.x + endpt.y - startpt.y)
    )

    nodes[(n.x, n.y)] = n
    open.append(n)

    while open:
        open.sort(key=lambda _: _.cost, reverse=True)
        print(open)

        node = open.pop()

        print_path(node, len(grid[0]), len(grid))

        closed.add((node.x, node.y))

        for x, y in node.neighbors():
            if (x, y) in closed or x < 0 or y < 0 or x >= gridx or y >= gridy:
                continue

            height = grid[y][x]
#            if abs(height - node.h) > 1:
            if (height - node.h) > 1:
                continue

            if existing := nodes.get((x, y)):
                # in open list... Reachable from a better node...
                if existing.cost_start > (node.cost_start + 1):
                    existing.parent = node
                    existing.cost_start = node.cost_start + 1
            else:
                newnode = Node(x, y, height, node, node.cost_start + 1, abs(endpt.x - x + endpt.y - y))

                if height == END:
                    print_path(newnode, len(grid[0]), len(grid))
                else:
                    nodes[(newnode.x, newnode.y)] = newnode
                    open.append(newnode)

#    now = time.time()
#    if now - last > 10:
#        last = now
#        print("\033c", end='')
#        print(len(path))
#        print_path(path, len(grid[0]), len(grid))

    return []

'''
v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
'''

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

    print(startpt, endpt)

    print_grid(grid)

    search(grid, startpt, endpt)


if __name__ == '__main__':
    main(sys.argv)
