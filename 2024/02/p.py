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
    L = [[int(x) for x in _.split()] for _ in lines]
    return L

def part1(data):
    safe = 0
    for L in data:
        L2 = [L[i]-L[i+1] for i in range(len(L)-1)]
        if all(1 <= abs(_) <= 3 for _ in L2) and len(set(_//abs(_) for _ in L2)) == 1:
            safe += 1
    print(safe)

def part2(data):
    safe = 0
    for L in data:
        is_safe = False
        for i in range(len(L)):
            L3 = [x for j, x in enumerate(L) if j != i]
            L2 = [L3[i]-L3[i+1] for i in range(len(L3)-1)]
            if all(1 <= abs(_) <= 3 for _ in L2) and len(set(_//abs(_) for _ in L2)) == 1:
                is_safe = True
                break
        if is_safe:
            safe += 1
    print(safe)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
