#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def transform(subject, loop, find=-1):
    v = 1
    for times in range(loop):
        v *= subject
        v %= 20201227
        if v == find:
            return times + 1
    return v
    
def part1(data):
    cpub, dpub = data
    cloop = transform(7, 2**64, cpub)
    dloop = transform(7, 2**64, dpub)

    assert transform(7, cloop) == cpub
    assert transform(7, dloop) == dpub
    assert transform(cpub, dloop) == transform(dpub, cloop)

    print(transform(cpub, dloop))

def main():
    data = parse_input()
    part1(data)

if __name__ == '__main__':
    main()
