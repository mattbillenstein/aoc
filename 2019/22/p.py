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
    steps = []

    for line in lines:
        if line == 'deal into new stack':
            steps.append(('reverse',))
        elif line.startswith('cut '):
            steps.append(('cut', int(line.split()[-1])))
        elif line.startswith('deal with increment '):
            steps.append(('deal', int(line.split()[-1])))
        elif line.startswith('Result: '):
            print(line)
        else:
            assert 0

    return steps

def part1(steps):
    deck = list(range(10007))

    for step in steps:
        f, *args = step
        if f == 'reverse':
            deck.reverse()
        elif f == 'cut':
            n = args[0]
            deck = deck[n:] + deck[:n]
        elif f == 'deal':
            n = args[0]
            i = 0
            for i, c in enumerate(list(deck)):
                deck[(i*n) % len(deck)] = c

    print(deck.index(2019))

def math(steps, cards, shuffles, pos):
    # this is mostly cribbed from the solution thread...
    # https://topaz.github.io/paste/#XQAAAQAgBQAAAAAAAAAzHIoib6pENkSmUIKIED8dy140D1lKWSMhNhZz+hjKgIgfJKPuwdqIBP14lxcYH/qI+6TyUGZUnsGhS4MQYaEtf9B1X3qIIO2JSejFjoJr8N1aCyeeRSnm53tWsBtER8F61O2YFrnp7zwG7y303D8WR4V0eGFqtDhF/vcF1cQdZLdxi/WhfyXZuWC+hs8WQCBmEtuId6/G0PeMA1Fr78xXt96Um/CIiLCievFE2XuRMAcBDB5We73jvDO95Cjg0CF2xgF4yt3v4RB9hmxa+gmt6t7wRI4vUIGoD8kX2k65BtmhZ7zSZk1Hh5p1obGZ6nuuFIHS7FpuSuv1faQW/FuXlcVmhJipxi37mvPNnroYrDM3PFeMw/2THdpUwlNQj0EDsslC7eSncZQPVBhPAHfYojh/LlqSf4DrfsM926hSS9Fdjarb9xBYjByQpAxLDcmDCMRFH5hkmLYTYDVguXbOCHcY+TFbl+G/37emZRFh/d+SkeGqbFSf64HJToM2I7N2zMrWP7NDDY5FWehD5gzKsJpEg34+sG7x2O82wO39qBlYHcYg1Gz4cLBrH1K1P+KWvEdcdj/NBtrl6yftMlCu6pH4WTGUe9oidaiRuQZOGtw71QsTQUuhpdoWO4mEH0U9+CiPZCZLaQolFDSky1J9nDhZZHy3+ETcUeDOfSu+HI3WuKC0AtIRPdG8B9GhtxZQKAx+5kyi/ek7A2JAY9SjrTuvRADxx5AikbHWXIsegZQkupAc2msammSkwY8dRMk0ilf5vh6kR0jHNbSi0g0KJLCJfqggeX24fKk5Mdh8ULZXnMfMZOmwEGfegByYbu91faLijfW4hoXCB1nlsWTPZEw2PCZqqhl9oc1q25H2YkkvKLxEZWl6a9eFuRzxhB840I1zdBjUVgfKd9/V4VdodzU2Z2e+VEh7RbJjQNFC/rG8dg==

    a, b = 1, 0
    for step in steps:
        f, *args = step
        if f == 'reverse':
            la, lb = -1, -1
        elif f == 'cut':
            n = args[0]
            la, lb = 1, -n
        elif f == 'deal':
            n = args[0]
            la, lb = n, 0

        # la * (a * x + b) + lb == la * a * x + la*b + lb
        # The `% n` doesn't change the result, but keeps the numbers small.
        a = (la * a) % cards
        b = (la * b + lb) % cards

    # Now want to morally run:
    # la, lb = a, b
    # a = 1, b = 0
    # for i in range(M):
    #     a, b = (a * la) % n, (la * b + lb) % n

    # For a, this is same as computing (a ** M) % n, which is in the computable
    # realm with fast exponentiation.
    # For b, this is same as computing ... + a**2 * b + a*b + b
    # == b * (a**(M-1) + a**(M) + ... + a + 1) == b * (a**M - 1)/(a-1)
    # That's again computable, but we need the inverse of a-1 mod n.

    # Fermat's little theorem gives a simple inv:
    def inv(a, n):
        return pow(a, n-2, n)

    Ma = pow(a, shuffles, cards)
    Mb = (b * (Ma - 1) * inv(a-1, cards)) % cards

    # This computes "where does 2020 end up", but I want "what is at 2020".
    #print((Ma * c + Mb) % n)

    # So need to invert (2020 - MB) * inv(Ma)
    print(((pos - Mb) * inv(Ma, cards)) % cards)

def part1a(steps):
    cards    = 10007
    shuffles = 1
    pos = 4775

    math(steps, cards, shuffles, pos)  # 2019 from part1

def part2(steps):
    cards    = 119315717514047
    shuffles = 101741582076661
    pos = 2020

    math(steps, cards, shuffles, pos)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '1a' in sys.argv:
        part1a(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
