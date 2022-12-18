#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    for line in data:
        print(line)

def main(argv):
    data = parse_input()

    part1(data)

if __name__ == '__main__':
    main(sys.argv)
