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
    state = lines[0].split()[-1]
    state = [1 if _ == '#' else 0 for _ in state]
    rules = {}
    for line in lines[2:]:
        line = line.split()
        k = tuple([1 if _ == '#' else 0 for _ in line[0]])
        rules[k] = 1 if line[-1] == '#' else 0

    return state, rules

def run(state, rules, gens):
    pad = 10
    offset = -10
    state = [0] * pad + list(state) + [0] * pad

    debug(0, ''.join('#' if _ else '.' for _ in state))

    for i in range(1, gens+1):
        nextstate = list(state)
        for j in range(0, len(state) - 5):
            k = tuple(state[j:j+5])
            nextstate[j+2] = rules.get(k, 0)
        state = nextstate

        # trim state
        if not any(state[:2*pad]):
            state = state[pad:]
            offset += pad

        if any(state[-pad:]):
            state += [0] * pad

        debug(i, offset, ''.join('#' if _ else '.' for _ in state))

    return state, offset

def part1(state, rules):
    state, offset = run(state, rules, 20)
    x = sum(_[1] for _ in zip(state, range(offset, offset + len(state))) if _[0])
    print(x)

def part2(state, rules):
    state, offset = run(state, rules, 1000)

    # points are just moving one step to the right per gen now...
    gens = 50_000_000_000

    offset = offset + gens - 1000
    x = sum(_[1] for _ in zip(state, range(offset, offset + len(state))) if _[0])
    print(x)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
