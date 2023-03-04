#!/usr/bin/env pypy3

import copy
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
    line = lines[0]
    for c in ',.':
        line = line.replace(c, '')
    L = line.split()
    return list(reversed([int(_) for _ in L if _.isdigit()]))

def part1(pt):
    c = 20151125
    x = y = lasty = 1
    while x != pt[0] or y != pt[1]:
        debug(x, y, c)
        c = (c * 252533) % 33554393
        x += 1
        y -= 1
        if y == 0:
            x = 1
            y = lasty + 1
            lasty = y

    debug(x, y)
    print(c)

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
