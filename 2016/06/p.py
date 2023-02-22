#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part(data):
    d = defaultdict(lambda: defaultdict(int))
    for line in data:
        for i, c in enumerate(line):
            d[i][c] += 1

    s = ''
    t = ''
    for pos in sorted(d):
        L = sorted([(v, k) for k, v in d[pos].items()])
        s += L[-1][1]
        t += L[0][1]

    print(s)
    print(t)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
