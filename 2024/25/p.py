#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    locks = []
    keys = []
    L = [0] * 5
    y = 0
    for line in lines:
        if not line:
            L = [0] * 5
            y = 0
            continue

        if y == 0:
            if all(_ == '#' for _ in line):
                locks.append(L)
            else:
                keys.append(L)

        for i, c in enumerate(line):
            if c == '#':
                L[i] += 1

        y += 1
        
    return (locks, keys)

def part1(locks, keys):
    tot = 0
    for lock in locks:
        for key in keys:
            if all(a + b <= 7 for a, b in zip(lock, key)):
                tot += 1
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)

if __name__ == '__main__':
    main()
