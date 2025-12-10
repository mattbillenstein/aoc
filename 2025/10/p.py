#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from functools import lru_cache
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    machines = []
    for line in lines:
        for c in '[](){}':
            line = line.replace(c, '')

        lights, *buttons, joltages = line.split()

        m = {}
        machines.append(m)
        m['lights'] = 0
        for i, c in enumerate(lights):
            if c == '#':
                m['lights'] = m['lights'] | (1 << i)

        m['buttons'] = []
        for b in buttons:
            x = 0
            for c in b.split(','):
                x |= 1 << int(c)
            m['buttons'].append(x)

        m['joltages'] = [int(_) for _ in joltages.split(',')]

    return (machines,)

def part1(machines):
    tot = 0
    for m in machines:
        lights = m['lights']
        found = -1
        for p in range(100):
            for buttons in itertools.product(m['buttons'], repeat=p):
                L = 0
                for b in buttons:
                    L ^= b
                if L == lights:
                    found = p
                    break
            if found > -1:
                break
        assert found > -1
        tot += found

    print(tot)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
