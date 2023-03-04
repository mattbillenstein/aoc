#!/usr/bin/env pypy3

import itertools
import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def part(data):
    cnt = 0
    d = defaultdict(int)
    for N in range(1, len(data)):
        for tup in itertools.combinations(data, N):
            if sum(tup) == 150:
                cnt += 1
                d[N] += 1
    print(cnt)

#    print(min(d))
    print(d[min(d)])

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
