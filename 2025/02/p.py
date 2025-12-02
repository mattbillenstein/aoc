#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    items = [_.split('-') for _ in lines[0].split(',')]
    items = [(int(a), int(b)) for a, b in items]
    return (items,)

def part1(data):
    tot = 0
    for a, b in data:
        for x in range(a, b+1):
            s = str(x)
            n = len(s)
            nx2 = n // 2
            if n % 2 == 0:
                if s[:nx2] == s[nx2:]:
                    tot += x
    print(tot)

def part2(data):
    tot = 0
    for a, b in data:
        for x in range(a, b+1):
            s = str(x)
            n = len(s)
            for m in range(1, n // 2 + 1):
                q, r = divmod(n, m)
                if r == 0 and s[:m] * q == s:
                    tot += x
                    break
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
