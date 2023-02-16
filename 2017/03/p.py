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
    return int(lines[0])

def manhattan(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def spiral():
    pt = [0, 0]
    size = 1
    i = 1

    yield (tuple(pt), i)

    while 1:
        i += 1
        size += 2
        pt[0] += 1
        yield (tuple(pt), i)

        for _ in range(size-2):
            i += 1
            pt[1] -= 1
            yield (tuple(pt), i)
        for _ in range(size-1):
            i += 1
            pt[0] -= 1
            yield (tuple(pt), i)
        for _ in range(size-1):
            i += 1
            pt[1] += 1
            yield (tuple(pt), i)
        for _ in range(size-1):
            i += 1
            pt[0] += 1
            yield (tuple(pt), i)

def part1(num):
    for pt, i in spiral():
        if i == num:
            break
    print(pt, manhattan((0, 0), pt))

def part2(num):
    g = SparseGrid([])
    for pt, i in spiral():
        if i == 1:
            g.set(pt, i)
        else:
            x = sum(g.get(npt, 0) for npt in g.neighbors8(pt))
            if x > num:
                print(x)
                break
            g.set(pt, x)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
