#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return int(lines[0])

def part1(n):
    L = [0]
    pos = 0
    size = 1
    for i in range(1, 2017+1):
        pos = ((pos + n) % size) + 1
        L.insert(pos, i)
        size += 1

    print(L[L.index(2017) + 1])

def part2(n):
    # value at position 1, we don't need to keep the list, just record every
    # time we put something at position 1...

    pos = 0
    size = 1
    for i in range(1, 50_000_000+1):
        pos = ((pos + n) % size) + 1
        if pos == 1:
            last = i
        size += 1

    print(last)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
