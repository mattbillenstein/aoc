#!/usr/bin/env pypy3

import sys

from grid import Grid
from graph import bfs

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    points = [_.split(',') for _ in lines]
    points = [(int(_[0]), int(_[1])) for _ in points]
    return (points,)

def part(points):
    size = (7, 7)
    start = (0, 0)
    end = (6, 6)
    steps = 12
    if len(points) > 1000:
        size = (71, 71)
        end = (70, 70)
        steps = 1024

    g = Grid(['.' * size[0] for _ in range(size[1])], {'.': 0, '#': 1, 'O': 2})

    for pt in points[:steps]:
        g.setc(pt, '#')

    if DEBUG > 1:
        g.print(2)
        if DEBUG > 2:
            g.draw(20)

    prev = {}
    def neighbors(pt):
        for npt in g.neighbors4(pt):
            if g.getc(npt) == '.':
                if npt not in prev:
                    prev[npt] = pt
                yield npt

    x = bfs(start, neighbors, set([end]))

    if '1' in sys.argv:
        if DEBUG:
            path = [end]
            pt = end
            while pt != start:
                pt = prev[pt]
                path.append(pt)

            for pt in path:
                g.setc(pt, 'O')

            g.print(0.05)
            if DEBUG > 1:
                g.print(2)
                if DEBUG > 2:
                    g.draw(20)

            for pt in path:
                g.setc(pt, '.')

        print(x[0][1])

    if not '2' in sys.argv:
        return

    for pt in points[steps:]:
        g.setc(pt, '#')
        if not bfs(start, neighbors, set([end])):
            if DEBUG:
                for pt in prev:
                    g.setc(pt, 'O')
                g.print(0.05)
                if DEBUG > 1:
                    g.print(1)
                    if DEBUG > 2:
                        g.draw()

            print('%d,%d' % pt)
            break

        if DEBUG:
            path = [end]
            pt = end
            while pt != start:
                pt = prev[pt]
                path.append(pt)

            for pt in path:
                g.setc(pt, 'O')

            if DEBUG > 1:
                g.print(0.05)
                if DEBUG > 2:
                    g.draw()

            prev.clear()
            for pt in path:
                g.setc(pt, '.')

    if DEBUG > 1:
        g.print(10)

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
