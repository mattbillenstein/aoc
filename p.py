#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def debug(*args):
    pass

if '--debug' in sys.argv:
    def debug(*args):
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    for line in data:
        print(line)

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
