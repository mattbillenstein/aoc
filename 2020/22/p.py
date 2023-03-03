#!/usr/bin/env pypy3

import sys
from collections import deque

DEBUG = sys.argv.count('-v')

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

def combat(d1, d2, level=0):
    debug(d1, d2, level)

    visited = set()

    while d1 and d2:
        k = hash((tuple(d1), tuple(d2)))
        if k in visited:
            return 1
        visited.add(k)

        c1 = d1.popleft()
        c2 = d2.popleft()

        if len(d1) >= c1 and len(d2) >= c2:
            s1 = deque(list(d1)[:c1])
            s2 = deque(list(d2)[:c2])
            winner = combat(s1, s2, level+1)
            if winner == 1:
                d1.append(c1)
                d1.append(c2)
            else:
                d2.append(c2)
                d2.append(c1)
        else:
            if c1 > c2:
                d1.append(c1)
                d1.append(c2)
            else:
                d2.append(c2)
                d2.append(c1)

    if level == 0:
        tot = 0
        for i, c in enumerate(reversed(d1 or d2)):
            tot += (i+1) * c
        debug(d1)
        debug(d1)
        print(tot)

    if d1:
        return 1
    return 2

def part2(data):
    combat(*data)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
