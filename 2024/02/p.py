#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    L = [[int(x) for x in _.split()] for _ in lines]
    return L

def check_safe(L):
    return all(1 <= abs(_) <= 3 for _ in L) and len(set(_//abs(_) for _ in L)) == 1

def part1(data):
    safe = 0
    for L in data:
        L2 = [L[i]-L[i+1] for i in range(len(L)-1)]
        if check_safe(L2):
            safe += 1
    print(safe)

def part2(data):
    safe = 0
    for L in data:
        # iterate over all lists removing one item and check
        for i in range(len(L)):
            L3 = [x for j, x in enumerate(L) if j != i]
            L2 = [L3[i]-L3[i+1] for i in range(len(L3)-1)]
            if check_safe(L2):
                safe += 1
                break
    print(safe)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
