#!/usr/bin/env pypy3

import copy
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

    rules = defaultdict(list)
    updates = []
    for line in lines:
        if '|' in line:
            x, y = line.split('|')
            x = int(x)
            y = int(y)
            rules[x].append(y)
        elif line:
            updates.append([int(_) for _ in line.split(',')])
            
    return rules, updates

def find(x, L):
    try:
        return L.index(x)
    except ValueError:
        return None

def is_valid(update, rules):
    for x, L2 in rules.items():
        xidx = find(x, update)
        if xidx is not None:
            for y in L2:
                yidx = find(y, update)
                if yidx is not None and yidx < xidx:
                    return False
    return True

def part1(rules, updates):
    tot = 0
    for L in updates:
        if is_valid(L, rules):
            z = L[len(L) // 2]
            tot += z
    print(tot)

def fix(update, rules):
    update = list(update)
    for x, L2 in rules.items():
        xidx = find(x, update)
        if xidx is not None:
            for y in L2:
                yidx = find(y, update)
                if yidx is not None and yidx < xidx:
                    # swap
                    update[xidx], update[yidx] = update[yidx], update[xidx]
    return update
                    
def part2(rules, updates):
    tot = 0
    for L in updates:
        if not is_valid(L, rules):
            while not is_valid(L, rules):
                L = fix(L, rules)
            z = L[len(L) // 2]
            tot += z
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
