#!/usr/bin/env pypy3

import copy
import itertools
import math
import re
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
    floors = {_+1: set() for _ in range(4)}
    elems = set()
    for i, line in enumerate(lines):
        line = line.replace('-compatible', '')
        for s in re.findall('[a-z]+ (?:generator|microchip)', line):
            s = s.replace('microchip', 'M')
            s = s.replace('generator', 'G')
            floors[i+1].add(tuple(s.split()))
            elems.add(s.split()[0])

    elems = sorted(elems)
    d = dict(zip(elems, 'ABCDEFGHIJKLMNOP'))
    for k in list(floors):
        floors[k] = set([d[_[0]] + _[1] for _ in floors[k]])
    return floors

def part1(floors):
    # so if you have everything on level N, moving everything to N+1 (empty)
    # proceeds:
    #
    # 3 pairs ABC
    #  0. Initial           [AM AG BM BG CM CG] -> []
    #  1. lift AM BM        [AG BG CM CG]       -> [AM BM]
    #  2. drop AM           [AM AG BG CM CG]    -> [BM]
    #  3. lift AM CM        [AG BG CG]          -> [AM BM CM]
    #  4. drop AM           [AM AG BG CG]       -> [BM CM]
    #  5. lift BG CG        [AM AG]             -> [BM BG CM CG]
    #  6. drop BM BG        [AM AG BM BG]       -> [CM CG]        # drop 2 since no single works...
    #  7. lift AG BG        [AM BM]             -> [AG BG CM CG]
    #  8. drop CM           [AM BM CM]          -> [AG BG CG]
    #  9. lift AM BM        [CM]                -> [AM AG BM BG CG]
    # 10. drop AM           [AM CM]             -> [AG BM BG CG]
    # 11. lift AM CM        []                  -> [AM AG BM BG CM CG]

    # so my input starts with two micros on the next level up, lets just unwind
    # that and I'll add 4 at the start...
    floors[1].update(floors[2])
    floors[2].clear()

    E = 1
    E1 = 1
    E2 = 2
    steps = 4

    def other(s):
        return s[0] + 'G' if s[1] == 'M' else 'M'

    while floors[E1]:
        pprint(floors)

        src_gens = [_ for _ in floors[E1] if _[1] == 'G']
        src_mics = [_ for _ in floors[E1] if _[1] == 'M']
        for mic in src_mics:
            if other(mic) not in src_gens and src_gens:
                assert 0

        tgt_gens = [_ for _ in floors[E2] if _[1] == 'G']
        tgt_mics = [_ for _ in floors[E2] if _[1] == 'M']
        for mic in tgt_mics:
            if other(mic) not in tgt_gens and tgt_gens:
                assert 0

        if E == E1:
            if len(tgt_gens) == 0:
                if len(tgt_mics) < 2:
                    # lift two mics if there are two, else mic and gen
                    for i in range(2):
                        x = src_mics.pop() if src_mics else src_gens.pop()
                        floors[E2].add(x)
                        floors[E1].remove(x)
                else:
                    gens = [other(_) for _ in tgt_mics if other(_) not in tgt_gens]
                    if not gens:
                        # if none unpaired, lift two others
                        gens = list(src_gens)
                        print(gens)
                        duh

                    # lift two gens
                    for i in range(2):
                        x = gens.pop()
                        floors[E2].add(x)
                        floors[E1].remove(x)
            else:
                duh

            E = E2
        else:
            # drop one if legal, else pair
            found = None
            for mic in tgt_mics:
                o = other(mic)
                if o in src_gens:
                    found = mic
                    break

            if found:
                floors[E2].remove(found)
                floors[E1].add(found)
            else:
                # drop pair
                x = tgt_mics[0]
                o = other(x)
                floors[E2].remove(x)
                floors[E2].remove(o)
                floors[E1].add(x)
                floors[E1].add(o)

            E = E1

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
