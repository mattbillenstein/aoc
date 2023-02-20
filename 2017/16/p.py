#!/usr/bin/env pypy3

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
    ops = []
    for item in lines[0].split(','):
        item = item.replace('/', ' ')
        item = [item[0]] + item[1:].split()
        if item[0] == 's':
            item[1] = int(item[1])
        elif item[0] == 'x':
            item[1] = int(item[1])
            item[2] = int(item[2])
        ops.append(tuple(item))
    return ops

def dance(data, L, times=1):
    for _ in range(times):
        for tup in data:
            if tup[0] == 's':
                n = tup[1]
                L[:] = L[-n:] + L[:-n]
            elif tup[0] == 'x':
                a, b = tup[1], tup[2]
                L[a], L[b] = L[b], L[a]
            elif tup[0] == 'p':
                a = L.index(tup[1])
                b = L.index(tup[2])
                L[a], L[b] = L[b], L[a]

def part1(data):
    L = list('abcdefghijklmnop')
    dance(data, L)
    print(''.join(L))

def part2(data):
    # compute the period to repeat back to the original order and then just run
    # 1e9 % period times
    s = 'abcdefghijklmnop'
    O = list(s)
    L = list(s)
    for i in range(1, 1_000_000):
        dance(data, L)
        if L == O:
            period = i
            break

    times = 1_000_000_000 % period
    L = list(s)
    dance(data, L, times)
    print(''.join(L))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
