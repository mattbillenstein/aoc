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

    fields = {}
    for i, line in enumerate(lines):
        if not line:
            break
        name, rest = line.split(': ')
        nums = rest.replace(' or ', ' ').replace('-', ' ').split()
        nums = [int(_) for _ in nums]
        fields[name] = [(nums[0], nums[1]), (nums[2], nums[3])]

    idx = lines.index('your ticket:')
    yours = [int(_) for _ in lines[idx+1].split(',')]

    idx = lines.index('nearby tickets:')
    nearby = []
    for line in lines[idx+1:]:
        nearby.append([int(_) for _ in line.split(',')])

    return fields, yours, nearby

def part1(fields, yours, nearby):
    valid = set()
    for k, L in fields.items():
        for a, b in L:
            for x in range(a, b+1):
                valid.add(x)

    tot = 0
    good = []
    for ticket in nearby:
        bad = False
        for x in ticket:
            if not x in valid:
                tot += x
                bad = True

        if not bad:
            good.append(ticket)

    print(tot)

    return fields, yours, good

def part2(*data):
    fields, yours, nearby = part1(*data)

    # [set()] for each ticket field that matches on each ticket
    matches = [[] for _ in range(len(nearby))]

    for i, ticket in enumerate(nearby):
        for j, num in enumerate(ticket):
            matches[i].append(set())
            for field, L in fields.items():
                (a1, a2), (b1, b2) = L
                if a1 <= num <= a2 or b1 <= num <= b2:
                    matches[i][j].add(field)

    # we end up with most ticket fields matching most fields, but often, we can
    # exclude one field from a given position for a given ticket which excludes
    # it for that position on all tickets...
    #
    # create list of sets representing what fields are possible for a given
    # position from this data...

    sfields = set(fields)

    possible = [set(fields) for _ in range(len(fields))]
    for mtch in matches:
        for i, fset in enumerate(mtch):
            for field in sfields - fset:
                possible[i].remove(field)

    # now where we find a position can only have one field, iteratively remove
    # that field from all other positions creating new positions which can only
    # be one field - if this "solves' we can stop, otherwise we may need to
    # guess and check?

    while not all(isinstance(_, str) for _ in possible):
        found = -1
        for i, x in enumerate(possible):
            if len(x) == 1:
                found = i

        if found == -1:
            print('broken? guess and check?')
            break

        possible[found] = field = possible[found].pop()
        for x in possible:
            if isinstance(x, set) and field in x:
                x.remove(field)

    debug(possible)

    prod = 1
    for field, value in zip(possible, yours):
        debug(field, value)
        if field.startswith('departure'):
            prod *= value

    print(prod)

def main():
    data = parse_input()
    part2(*data)

if __name__ == '__main__':
    main()
