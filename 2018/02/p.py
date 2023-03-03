#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    cnt2 = 0
    cnt3 = 0
    for line in data:
        d = defaultdict(int)
        for c in line:
            d[c] += 1

        if 2 in d.values():
            cnt2 += 1
        if 3 in d.values():
            cnt3 += 1

    print(cnt2 * cnt3)

def part2(data):
    for s1 in data:
        for s2 in data:
            if s1 == s2:
                continue
            diff = 0
            s = ''
            for c1, c2 in zip(s1, s2):
                if c1 != c2:
                    diff += 1
                else:
                    s += c1

            if diff == 1:
                debug(s1, s2)
                print(s)
                return

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
