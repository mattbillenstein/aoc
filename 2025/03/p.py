#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from functools import lru_cache
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return (lines,)

def part1(data):
    L = []
    for bank in data:
        v = 0
        for i in range(len(bank)):
            for j in range(i+1, len(bank)):
                if j > i:
                    x = int(bank[i] + bank[j])
                    if x > v:
                        v = x
        L.append(v)
    print(sum(L))

def part2(data):
    L = []
    for bank in data:
        s = ''
        rest = bank
        for i in range(11, 0, -1):
            digit = max(rest[:-i])
            s += digit
            idx = rest[:-i].find(digit)
            rest = rest[idx+1:]
        s += max(rest)
        L.append(int(s))
    print(sum(L))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
