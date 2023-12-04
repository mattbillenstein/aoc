#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cards = {}
    for line in lines:
        card, rest = line.split(':')
        card = int(card.split()[1])
        a, b = rest.split('|')
        a = set([int(_.strip()) for _ in a.strip().split()])
        b = set([int(_.strip()) for _ in b.strip().split()])
        cards[card] = (a, b, len(a & b))
    return cards

def part1(data):
    tot = 0
    for c, tup in data.items():
        a, b, li = tup
        if li:
            tot += 2 ** (li-1)
    print(tot)

def part2(data):
    # initial card counts
    cards = {k: 1 for k in data}

    for c, tup in data.items():
        _, _, li = tup
        if li:
            for c2 in range(c+1, c+1+li):
                # for each won card, add N copies from the source card...
                cards[c2] += cards[c]

    print(sum(cards.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
