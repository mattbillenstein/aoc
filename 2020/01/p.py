#!/usr/bin/env pypy3

import sys
from itertools import combinations
from math import prod

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def run(data, num):
    for x in combinations(data, num):
        if sum(x) == 2020:
            print(prod(x))
            break

def part1(data):
    run(data, 2)

def part2(data):
    run(data, 3)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
