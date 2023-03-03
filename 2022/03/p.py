#!/usr/bin/env pypy3

import string
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

priorities = ' ' + string.ascii_letters

def part1(data):
    tot = 0
    for line in data:
        mid = len(line) // 2
        A, B = line[:mid], line[mid:]
        assert len(A) == len(B)
        common = set(A) & set(B)
        assert len(common) == 1
        common = common.pop()
        tot += priorities.index(common)

    print(tot)

def part2(data):
    tot = 0
    L = []
    for line in data:
        L.append(line)
        if len(L) == 3:
            common = set(L[0]) & set(L[1]) & set(L[2])
            assert len(common) == 1
            common = common.pop()
            tot += priorities.index(common)
            L.clear()

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
