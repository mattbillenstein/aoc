#!/usr/bin/env python3

import sys

def parse_input():
    lines = [_.strip('\r\n').split() for _ in sys.stdin]
    return tuple([(hand, int(bid)) for hand, bid in lines])

def hand_type(hand):
    L = [hand.count(_) for _ in set(hand)] + [0]
    L.sort(reverse=True)
    return L[0] * 100 + L[1]

def part(hands, score_hand):
    hands = [(score_hand(hand), bid) for hand, bid in hands]
    hands.sort()

    tot = 0
    for i, tup in enumerate(hands):
        _, bid = tup
        tot += (i+1) * bid
    print(tot)

def part1(hands):
    def score_hand(hand):
        base = hand_type(hand)
        cards = '23456789TJQKA'
        s = ''.join(f'{cards.index(_):02d}' for _ in hand)
        return int(str(base) + s)
    part(hands, score_hand)

def part2(hands):
    def score_hand(hand):
        cards = 'J23456789TQKA'
        base = max(hand_type(hand.replace('J', _)) for _ in cards[1:])
        s = ''.join(f'{cards.index(_):02d}' for _ in hand)
        return int(str(base) + s)
    part(hands, score_hand)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
