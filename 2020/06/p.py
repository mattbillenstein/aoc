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
    groups = []
    group = defaultdict(int)
    for line in lines:
        if not line:
            groups.append(group)
            group = defaultdict(int)
            continue
        group['size'] += 1
        for c in line:
            group[c] += 1
    
    groups.append(group)

    return groups

def part1(data):
    print(sum(len(_)-1 for _ in data))

def part2(data):
    tot = 0
    for grp in data:
        tot += sum(1 for k, v in grp.items() if k != 'size' and v == grp['size'])
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
