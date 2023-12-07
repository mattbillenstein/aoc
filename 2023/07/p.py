#!/usr/bin/env pypy3

import copy
import itertools
import math
import sys
import time
from collections import defaultdict
from functools import cmp_to_key
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [_.split() for _ in lines]
    return [(hand, int(bid)) for hand, bid in lines]

def hand_type(hand):
    groups = defaultdict(int)
    for c in hand:
        groups[c] += 1

    L = [(v, k) for k, v in groups.items()]
    L.sort(reverse=True)

    if L[0][0] == 5:
        # five of a kind
        base = 7
    elif L[0][0] == 4:
        # four of a kind
        base = 6
    elif L[0][0] == 3 and L[1][0] == 2:
        # full house
        base = 5
    elif L[0][0] == 3:
        # three of a kind
        base = 4
    elif L[0][0] == 2 and L[1][0] == 2:
        # two pair
        base = 3
    elif L[0][0] == 2:
        # one pair
        base = 2
    elif L[0][0] == 1:
        # high card
        base = 1
    else:
        assert 0

    return 10**base

def score_hand1(hand):
    base = hand_type(hand)
    cards = '23456789TJQKA'
    s = ''.join(f'{cards.index(_):02d}' for _ in hand)
    return int(str(base) + s)

def hand_cmp(a, b, f=score_hand1):
    a = f(a[0])
    b = f(b[0])
    if a < b:
        return -1
    if a == b:
        return 0
    return 1

def part1(hands):
    hands.sort(key=cmp_to_key(hand_cmp))
    tot = 0
    for i, x in enumerate(hands):
        hand, bid = x
        tot += (i+1) * bid
    print(tot)

def score_hand2(hand):
    cards = 'J23456789TQKA'
    base = max(hand_type(hand.replace('J', _)) for _ in cards[1:])
    s = ''.join(f'{cards.index(_):02d}' for _ in hand)
    return int(str(base) + s)

def part2(hands):
    hands.sort(key=cmp_to_key(lambda a, b: hand_cmp(a, b, score_hand2)))
    tot = 0
    for i, x in enumerate(hands):
        hand, bid = x
        tot += (i+1) * bid
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
