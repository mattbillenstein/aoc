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
    data = [[int(_) for _ in line.split()] for line in lines]
    return data

def part1(data):
    print(sum(max(_)-min(_) for _ in data))

def part2(data):
    tot = 0
    for row in data:
        for i in range(len(row)):
            for j in range(len(row)):
                if i == j:
                    continue

                if row[i] >= row[j]:
                    if row[i] % row[j] == 0:
                        tot += row[i] // row[j]

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
