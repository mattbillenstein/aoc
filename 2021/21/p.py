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
#    lines = [int(_) for _ in lines]
    lines = [int(_.split()[-1]) for _ in lines]
    return lines

def part1(data):
    p1, p2 = data
    s1 = s2 = rolls = 0
    size = 10

    def roll():
        nonlocal rolls
        rolls += 1
        return rolls % 100

    while s1 < 1000 and s2 < 1000:
        x = sum([roll() for i in range(3)])
        p1 = (p1 + x) % size
        s1 += p1 or 10
        if s1 >= 1000:
            break

        x = sum(roll() for i in range(3))
        p2 = (p2 + x) % size
        s2 += p2 or 10
        if s2 >= 1000:
            break
        
    debug(p1, s1)
    debug(p2, s2)
    debug(rolls)
    print(min(s1, s2) * rolls)

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
