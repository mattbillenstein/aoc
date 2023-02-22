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
    links = []
    for line in lines:
        links.append(tuple(sorted([int(_) for _ in line.split('/')])))
    links.sort()
    return links

def strength(L):
    return sum(a+b for a, b in L)

def search(bridge, connect, links, best):
    found = False
    for link in list(links):
        if connect in link:
            found = True
            links.remove(link)
            bridge.add(link)
            c = link[0]
            if link[0] == connect:
                c = link[1]
            search(bridge, c, links, best)
            bridge.remove(link)
            links.add(link)

    if not found:
        score = strength(bridge)
        if score > best[0][0]:
            best[0][0] = score
            best[0][1] = tuple(bridge)

        if (len(bridge), score) > best[1][0]:
            best[1][0] = (len(bridge), score)
            best[1][1] = tuple(bridge)

def part(links):
    links = set(links)
    best = [
        [0, None],
        [(0, 0), None],
    ]
    for link in list(links):
        if link[0] == 0:
            links.remove(link)
            search(set([link]), link[1], links, best)
            links.add(link)

    print(best[0][0])
    print(best[1][0][1])

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
