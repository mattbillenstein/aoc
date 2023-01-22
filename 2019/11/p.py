#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import SparseGrid
from intcode import intcode

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def part(mem, start=0):
    g = SparseGrid([])
    pt = (0, 0)
    g.set(pt, start)

    dir = '^'
    dirs = {
        # 0 is left, 1 right
        '^': {0: '<', 1: '>'},
        '<': {0: 'v', 1: '^'},
        'v': {0: '>', 1: '<'},
        '>': {0: '^', 1: 'v'},
    }

    prog = intcode(mem)

    painted = set()

    while 1:
        try:
            next(prog) # run up to yield...

            # feed value of current tile and read color to paint
            v = g.get(pt, 0)
            color = prog.send(v)

            # paint the grid and record the painted tile
            g.set(pt, color)
            painted.add(pt)

            # turn and step
            turn = next(prog)
            dir = dirs[dir][turn]
            pt = g.step(pt, dir)
        except StopIteration:
            break

    print()
    g.print()

    print(len(painted))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part(data)
    if '2' in sys.argv:
        part(data, 1)

if __name__ == '__main__':
    main()
