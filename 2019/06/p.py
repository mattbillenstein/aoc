#!/usr/bin/env pypy3

import itertools
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
    lines = [_.split(')') for _ in lines]
    return lines

def run(data):
    orbits = {}
    for a, b in data:
        orbits[b] = a

    cnt = 0
    for x in orbits:
        while x != 'COM':
            cnt += 1
            x = orbits[x]

    print(cnt)
    
    paths = []
    for x in ('YOU', 'SAN'):
        path = []
        paths.append(path)
        while x != 'COM':
            x = orbits[x]
            path.append(x)

    for path in paths:
        path.reverse()

    cnt = 0
    for x1, x2 in zip(*paths):
        if x1 != x2:
            break
        cnt += 1

    debug(cnt)
    debug(paths[0][:cnt])
    debug(paths[1][:cnt])
    debug(paths[0][cnt:])
    debug(paths[1][cnt:])

    print(len(paths[0][cnt:]) + len(paths[1][cnt:]))

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
