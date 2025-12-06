#!/usr/bin/env pypy3

import sys

from algo import merge_ranges

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    fresh = []
    ingredients = []

    for line in lines:
        if '-' in line:
            fresh.append(tuple([int(_) for _ in line.split('-')]))
        elif line:
            ingredients.append(int(line))

    return fresh, ingredients

def part1(fresh, ingredients):
    tot = 0
    for i in ingredients:
        for a, b in fresh:
            if a <= i <= b:
                tot += 1
                break
    print(tot)

def part2(fresh, _):
    # sort, take a copy
    fresh = sorted(fresh)

    # iterate the sorted list merging any following overlapping range onto the
    # i-th one and marking the j-th removed
    for i in range(len(fresh)):
        if not fresh[i]:
            continue
        a1, a2 = fresh[i]
        for j in range(i + 1, len(fresh)):
            b1, b2 = fresh[j]
            if b1 <= a1 <= b2 or b1 <= a2 <= b2 or a1 <= b1 <= a2 or a1 <= b2 <= a2:
                fresh[i] = (a1, a2) = (min(a1, b1), max(a2, b2))
                fresh[j] = None

    tot = 0
    for tup in fresh:
        if tup:
            tot += tup[1] - tup[0] + 1
    print(tot)

def part2a(fresh, _):
    print(sum(b - a + 1 for a, b in merge_ranges(fresh)) )

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)
    if '2a' in sys.argv:
        part2a(*data)

if __name__ == '__main__':
    main()
