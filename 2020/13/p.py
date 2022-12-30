#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    ts = int(lines[0])
    busses = [int(_) for _ in lines[1].replace('x', '0').split(',')]
    return ts, busses

def part1(ts, busses):
    mn = (sys.maxsize, 0)
    for b in busses:
        if b == 0:
            continue

        n = ts // b
        if ts % b != 0:
            n += 1

        t = n * b
        if t < mn[0]:
            mn = (t, b)

    debug(mn)

    print((mn[0] - ts) * mn[1])

################################
# Eh, my math is too weak for this one... Cribbed from:
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python

from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

################################

def part2(ts, busses):
    # eh, this is cribbed, I don't understand really what this is doing...

    bus_time = [(b, _) for _, b in enumerate(busses) if b > 0]

    ni = []
    bi = []
    for i, b in enumerate(busses):
        if b > 0:
            ni.append(b)
            # convert to x = r (mod b) ?
            bi.append((b - i % b) % b)

    print(chinese_remainder(ni, bi))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

    if '2a' in sys.argv:
        part2a(*data)

if __name__ == '__main__':
    main()
