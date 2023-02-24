#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return int(lines[0])

def part1(n):
    L = [[_+1] for _ in range(n)]
    pos = 0
    found = True
    while found:
        if L[pos]:
            found = False
            i = (pos + 1) % n
            while i != pos:
                if L[i]:
                    found = True
                    L[pos].extend(L[i])
                    L[i].clear()
                    break
                i = (i + 1) % n
        pos = (pos + 1) % n

    for i in range(len(L)):
        if L[i]:
            print(i+1)
            break

def part2(n):
    # this is slow af, 15m to run, there's some pattern here, but oh well...
    L = [_+1 for _ in range(n)]
    pos = 0
    while len(L) > 1:
        i = (len(L) // 2 + pos) % len(L)
        L.pop(i)
        if i > pos:
            pos += 1
        pos = pos % len(L)
        if DEBUG:
            if len(L) % 1000 == 0 or len(L) < 20:
                print(pos, len(L))

    print(L[0])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
