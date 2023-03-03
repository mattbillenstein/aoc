#!/usr/bin/env pypy3

import random
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

def next_input(prog):
    s = ''
    while 1:
        try:
            o = next(prog)
        except StopIteration:
            break
        if o is None:
            continue
        if o == 'INPUT':
            break

        if o > 127:
            return o

        c = chr(o)
        if c == '\n':
            print(s)
            s = ''
        else:
            s += c

def part1(mem):
    # registers A-D, 4 steps ahead
    prog = intcode(mem)

    next_input(prog)

    inp = [
        # Jump if any hole ABC and not hole D
        'NOT A T',
        'NOT B J',
        'OR T J',   # A' or B'
        'NOT C T',
        'OR T J',   # A' or B' or C'
        'AND D J',
        'WALK\n',
    ]
    inp = '\n'.join(inp)

    for c in inp:
        prog.send(ord(c))

    dmg = next_input(prog)
    print(dmg)

def part2(mem):
    # we now have registers A-I, 9 steps ahead
    # mainly just trial and error - landing at the first spot after a hole
    # generally gives the most options...

    prog = intcode(mem)

    next_input(prog)

    inp = [
        # hole at C, land at D, H
        'NOT C J',
        'AND D J',
        'AND H J',

        # hole at B, land at D, H
        'NOT B T',
        'AND D T',
        'AND H T',

        'OR T J',

        # or, any hole at A...
        'NOT A T',

        'OR T J',

        'RUN\n',
    ]
    inp = '\n'.join(inp)

    for c in inp:
        prog.send(ord(c))

    dmg = next_input(prog)
    print(dmg)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
