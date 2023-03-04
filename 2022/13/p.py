#!/usr/bin/env pypy3

import json
import sys
from functools import cmp_to_key
from itertools import zip_longest

def cmp(L, R):
    types = (type(L), type(R))

    # If both values are integers, the lower integer should come first
    if types == (int, int):
        if L < R:
            return -1
        if L == R:
            return 0
        return 1

    # If both values are lists, compare the first value of each list, then the
    # second value, and so on. If L runs out of items first, they're in order
    if types == (list, list):
        for a, b in zip_longest(L, R):
            # exhausted
            if a is None:
                return -1
            if b is None:
                return 1

            x = cmp(a, b)
            if x != 0:
                return x

        # lists equal
        return 0

    # If exactly one value is an integer, convert the integer to a list which
    # contains that integer as its only value, then retry the comparison.
    if types == (int, list):
        return cmp([L], R)
    if types == (list, int):
        return cmp(L, [R])

    assert 0, types

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    pairs = []
    item = []
    for line in lines:
        if line:
            item.append(json.loads(line))
            if len(item) == 2:
                pairs.append(tuple(item))
                item.clear()

    return pairs

def part(data):
    # part 1, sum of index of sorted items, first is 1
    i = sum = 0
    for a, b in data:
        i += 1
        x = cmp(a, b)
        if x == -1:
            sum += i

    print(sum)

    # part 2 - product of index of these two markers
    markers = [[[2]], [[6]]]
    items = list(markers)
    for a, b in data:
        items.append(a)
        items.append(b)

    items.sort(key=cmp_to_key(cmp))

    tot = 1
    i = 0
    for item in items:
        i += 1
        if item in markers:
            tot *= i

    print(tot)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
