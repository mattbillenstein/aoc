#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def dragon(s, n):
    while len(s) < n:
        s += '0' + ''.join('0' if _ == '1' else '1' for _ in reversed(s))
    return s[:n]

def checksum(s):
    while 1:
        L = []
        for i in range(0, len(s), 2):
            a, b = s[i], s[i+1]
            if a == b:
                L.append('1')
            else:
                L.append('0')

        s = ''.join(L)
        if len(s) % 2 == 1:
            break

    return s

def part1(data, n=272):
    s = dragon(data, n)
    debug(s)
    c = checksum(s)
    print(c)

def part2(data):
    n = 35651584
    part1(data, n)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
