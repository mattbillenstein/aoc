#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    L = []
    x = []
    for line in lines:
        if not line:
            L.append(Grid(x))
            x = []
        else:
            x.append(line)
    L.append(Grid(x))
    return L

def reflect_rows(L):
    if DEBUG > 0:
        for item in L:
            print(item)
        print()
    N = len(L)
    for i in range(N-1):
        if L[i] == L[i+1]:
            up = i+1
            down = N - up

            debug(i, N, up, down, 1)

            if down > up:
                L1 = L[0:up]
                L2 = L[up:up+len(L1)]
                assert len(L1) == len(L2)
            else:
                L2 = L[up:]
                L1 = L[up-len(L2):up]
                assert len(L1) == len(L2)

            L2.reverse()
            if L1 == L2:
                return up

    return 0

def part1(grids):
    totrows = 0
    totcols = 0
    for g in grids:
        g = g.copy()
        rows = reflect_rows(g.g)
        g.rotate_cw()
        cols = reflect_rows(g.g)

        totrows += rows
        totcols += cols

    print(totrows*100 + totcols)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
