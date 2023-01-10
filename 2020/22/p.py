#!/usr/bin/env pypy3

import math
import sys
import time
from collections import deque
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    decks = []
    for line in lines:
        if line.startswith('Player '):
            deck = deque()
            decks.append(deck)
        elif line:
            deck.append(int(line))
    return decks

def part1(data):
    d1, d2 = data

    rounds = 0
    while d1 and d2:
        rounds += 1
        c1 = d1.popleft()
        c2 = d2.popleft()

        if c1 > c2:
            d1.append(c1)
            d1.append(c2)
        else:
            d2.append(c2)
            d2.append(c1)

    debug(d1)
    debug(d2)

    tot = 0
    for i, c in enumerate(reversed(d1 or d2)):
        tot += (i+1) * c
        
    print(rounds, tot)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
