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
    start = time.time()
    possibles = []
    for num in data:
        L = []
        poss = {}
        possibles.append(poss)
        price = num % 10
        for i in range(2000):
            num = ((num * 64) ^ num) % 16777216
            num = ((num // 32) ^ num) % 16777216
            num = ((num * 2048) ^ num) % 16777216
            newprice = num % 10

            L.append(newprice - price)
            price = newprice
            if i >= 3:
                p = tuple(L)
                if p not in poss:
                    poss[p] = price
                L[:] = L[1:]

    #print(time.time() - start)
    s = set()
    for poss in possibles:
        s.update(poss)

    #print(time.time() - start)
    mx = 0
    mp = None
    for p in s:
        x = sum(_.get(p, 0) for _ in possibles)
        if x > mx:
            mx = x
            mp = p

    #print(time.time() - start)
    print(mx) #, mp)


def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
