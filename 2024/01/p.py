#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    L1 = []
    L2 = []
    for line in lines:
        a, b = line.split()
        L1.append(int(a))
        L2.append(int(b))
    return L1, L2

def part1(L1, L2):
    print(sum(abs(a-b) for a, b in zip(sorted(L1), sorted(L2))))

def part2(L1, L2):
    print(sum(a * L2.count(a) for a in L1))

def main():
    L1, L2 = parse_input()
    if '1' in sys.argv:
        part1(L1, L2)
    if '2' in sys.argv:
        part2(L1, L2)

if __name__ == '__main__':
    main()
