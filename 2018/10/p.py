#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    points = []
    for line in lines:
        for c in '<>,':
            line = line.replace(c, ' ')
        L = line.split()
        L = [[int(L[1]), int(L[2])], (int(L[4]), int(L[5]))]
        points.append(L)

    return points

def part1(data):
    t = 0
    last_size = 0
    while 1:
        points = set(tuple(_[0]) for _ in data)
        g = SparseGrid(points)

        if last_size and last_size < (g.size[0] * g.size[1]):
            break

        t += 1
        last_size = g.size[0] * g.size[1]

        if g.size[0] < 100 or g.size[1] < 100:
            g.print()
            print()

        for pt, vel in data:
            pt[0] += vel[0]
            pt[1] += vel[1]

    print(t - 1)

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
