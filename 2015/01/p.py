#!/usr/bin/env pypy3

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
    return lines[0]

def part1(data):
    print(data.count('(') - data.count(')'))

def part2(data):
    floor = 0
    for i, c in enumerate(data):
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1

        if floor == -1:
            break

    print(i+1)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
