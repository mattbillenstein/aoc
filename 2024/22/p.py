#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return (lines,)

def part1(data):
    tot = 0
    for num in data:
        for i in range(2000):
            num = ((num * 64) ^ num) % 16777216
            num = ((num // 32) ^ num) % 16777216
            num = ((num * 2048) ^ num) % 16777216
        tot += num
    print(tot)

def part2(data):
    possibles = defaultdict(dict)
    for seller, num in enumerate(data):
        p = 0
        price = num % 10
        for i in range(2000):
            num = ((num * 64) ^ num) % 16777216
            num = ((num // 32) ^ num) % 16777216
            num = ((num * 2048) ^ num) % 16777216
            newprice = num % 10

            delta = newprice - price
            price = newprice

            # pack the delta prices into a 32-bit int, 1-byte per
            p = ((p << 8) | (delta + 100)) & 0xffffffff
            if i >= 3:
                if seller not in possibles[p]:
                    possibles[p][seller] = price

    mx = 0
    mp = None
    for p, d in possibles.items():
        x = sum(d.values())
        if x > mx:
            mx = x
            mp = p

    print(mx)


def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
