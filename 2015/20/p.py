#!/usr/bin/env pypy3

import math
import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return int(lines[0])

def part1(num):
    h = 1
    while 1:
        tot = 0
        i = 1
        for i in range(1, int(math.sqrt(h))):
            if h % i == 0:
                tot += i
                tot += h // i
            i += 1
        tot *= 10

        if tot > num:
            break
        h += 1

    print(h)

def part2(num):
    cnt = defaultdict(int)

    h = 1
    while 1:
        tot = 0
        i = 1
        for i in range(1, int(math.sqrt(h))):
            if h % i == 0:
                if cnt[i] < 50:
                    tot += i
                    cnt[i] += 1

                j = h // i
                if cnt[j] < 50:
                    tot += j
                    cnt[j] += 1
            i += 1
        tot *= 11

        if tot > num:
            break
        h += 1

    print(h)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
