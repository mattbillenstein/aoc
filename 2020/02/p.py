#!/usr/bin/env pypy3

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

    items = []
    for line in lines:
        a, pw = line.split(':')
        rng, c = a.split()
        pw = pw.strip()
        rng = tuple(int(_) for _ in rng.split('-'))
        items.append((rng, c, pw))

    return items

def part1(data):
    tot = 0
    for rng, ch, pw in data:
        if rng[0] <= pw.count(ch) <= rng[1]:
            tot += 1

    print(tot)

def part2(data):
    tot = 0
    for rng, ch, pw in data:
        if sum(1 for _ in rng if pw[_-1] == ch) == 1:
            tot += 1

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
