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
#    lines = [int(_) for _ in lines]
    lines = [int(_.split()[-1]) for _ in lines]
    return lines

def part1(data):
    p1, p2 = data
    s1 = s2 = rolls = 0
    size = 10

    def roll():
        nonlocal rolls
        rolls += 1
        return rolls % 100

    while s1 < 1000 and s2 < 1000:
        x = sum([roll() for i in range(3)])
        p1 = (p1 + x) % size
        s1 += p1 or 10
        if s1 >= 1000:
            break

        x = sum(roll() for i in range(3))
        p2 = (p2 + x) % size
        s2 += p2 or 10
        if s2 >= 1000:
            break
        
    debug(p1, s1)
    debug(p2, s2)
    debug(rolls)
    print(min(s1, s2) * rolls)

def play_round(p1, p2, s1, s2, universes, outcomes, depth=''):
#    print(depth, p1, p2, s1, s2, universes)
#    time.sleep(1)

    w1 = 0
    w2 = 0

    # simulate all outcomes of a round and recurse
    for roll1 in range(3, 9+1):  # 1+1+1 to 3+3+3
        npos1, nu1 = outcomes[(p1, roll1)]
        if s1 + npos1 >= 21:
            w1 += universes * nu1
            continue

        for roll2 in range(3, 9+1):
            npos2, nu2 = outcomes[(p2, roll2)]

            if s2 + npos2 >= 21:
                w2 += universes * nu1 * nu2
            else:
                nw1, nw2 = play_round(npos1, npos2, s1 + npos1, s2 + npos2, universes * nu1 * nu2, outcomes, depth+' ')
                w1 += nw1
                w2 += nw2

    return w1, w2

def part2(data):
    # universes...
    #
    # 7 outcomes (1+1+1 to 3+3+3) for 27 (3*3*3) universes, significant
    # overlap, simulate all outcomes of one round, how many universes each
    # outcome represents and recurse...

    universes = defaultdict(int)
    die = (1, 2, 3)
    for a in die:
        for b in die:
            for c in die:
                s = sum((a, b, c))
                universes[s] += 1

    debug(universes)

    size = 10

    outcomes = {}
    for pos in range(size):
        pos += 1
        for roll in range(3, 9+1):  # 1+1+1 to 3+3+3
            npos = (pos + roll) % size or size
            k = (pos, roll)
            outcomes[k] = (npos, universes[roll])

    if DEBUG:
        for k, v in outcomes.items():
            print('outcome', k, v)

    p1, p2 = data
    debug(p1, p2)

    w1, w2 = play_round(p1, p2, 0, 0, 1, outcomes)

    print(w1, w2)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
