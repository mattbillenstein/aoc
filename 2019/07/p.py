#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from intcode import intcode

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def run_thrusters(mem, phases, repeat=False):
    v = 0
    gens = []
    for p in phases:
        g = intcode(mem)
        gens.append(g)
        next(g)
        g.send(p)
        v = g.send(v)

    if not repeat:
        return v

    while 1:
        try:
            for g in gens:
                next(g)
                v = g.send(v)
        except StopIteration:
            break

    return v
        
def part(mem, phases, repeat=False):
    mx = 0
    for L in itertools.permutations(phases, 5):
        thrust = run_thrusters(mem, L, repeat)
        if thrust > mx:
            mx = thrust
    print(mx)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part(data, [0, 1, 2, 3, 4])
    if '2' in sys.argv:
        part(data, [5, 6, 7, 8, 9], True)

if __name__ == '__main__':
    main()
