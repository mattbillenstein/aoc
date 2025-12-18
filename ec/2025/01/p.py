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
    names = lines[0].split(',')
    instructions = [int(_[1:]) * (-1 if _[0] == 'L' else 1) for _ in lines[2].split(',')]
    return (names, instructions)

def part1(names, instructions):
    i = 0
    for n in instructions:
        if n < 0:
            i = max(0, i+n)
        else:
            i = min(i+n, len(names)-1)
    print(names[i])

def part2(names, instructions):
    i = 0
    for n in instructions:
        j = (i+n) % len(names)
        #print(i, n, names[i], names[j])
        i = j
    print(names[i])

def part3(names, instructions):
    for n in instructions:
        i = 0
        j = (i+n) % len(names)
        names[j], names[i] = names[i], names[j]
    print(names[i])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)
    if '3' in sys.argv:
        part3(*data)

if __name__ == '__main__':
    main()
