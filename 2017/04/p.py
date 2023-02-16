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
    lines = [_.split() for _ in lines]
    return lines

def part1(data):
    print(sum(1 for _ in data if len(_) == len(set(_))))

def part2(data):
    data = [[''.join(sorted(_)) for _ in line] for line in data]
    print(sum(1 for _ in data if len(_) == len(set(_))))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
