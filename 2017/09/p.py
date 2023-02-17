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
    return lines[0]

def count_garbage(garbage):
    cnt = 0
    for i, c in enumerate(garbage):
        if c == '!':
            continue

        # count preceding !
        j = 1
        while garbage[i-j] == '!':
            j += 1
        j -= 1
        if j % 2 == 0:
            cnt += 1

    return cnt

def part(data):
    groups = []
    score = 0
    tot = 0
    garbage = -1
    cnt = 0
    for i, c in enumerate(data):
        if garbage >= 0:
            if c == '>':
                # count preceding !
                j = 1
                while data[i-j] == '!':
                    j += 1
                j -= 1
                if j % 2 == 0:
                    cnt += count_garbage(data[garbage+1:i])
                    garbage = -1
        else:
            if c == '<':
                garbage = i
            elif c == '{':
                score += 1
                tot += score
            elif c == '}':
                score -= 1

    print(tot)
    print(cnt)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
