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
    return [int(_) for _ in lines[0].split()]

def part1(data):
    seen = set()
    i = 0
    while 1:
        if tuple(data) in seen:
            break
        seen.add(tuple(data))
        i += 1
        idx = data.index(max(data))
        x = data[idx]
        data[idx] = 0
        while x:
            idx += 1
            data[idx % len(data)] += 1
            x -= 1

    print(i)

def part2(data):
    seen = set()
    i = 0
    last = 0
    while 1:
        if tuple(data) in seen:
            print(i, i - last)
            last = i
            seen.clear()

        seen.add(tuple(data))
        i += 1
        idx = data.index(max(data))
        x = data[idx]
        data[idx] = 0
        while x:
            idx += 1
            data[idx % len(data)] += 1
            x -= 1

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(list(data))
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
