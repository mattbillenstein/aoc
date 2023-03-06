#!/usr/bin/env pypy3

import sys

from grid import SparseGrid
from intcode import intcode

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def part1(mem):
    g = SparseGrid([], {'.': 0, '#': 1, 'O': 2})

    cnt = 0
    for x in range(50):
        for y in range(50):
            prog = intcode(mem)
            next(prog)
            prog.send(x)
            o = prog.send(y)

            if o:
                cnt += 1
                g.set((x, y), 1)

    if DEBUG:
        g.print()

    print(cnt)

def part2(mem):
    y = 1000

    while 1:
        y += 1

        # beam follows rough x=y diagonal
        x = y

        # find top right set point
        for step in (50, 25, 10, 1):
            v = 0
            while not v:
                x -= step
                prog = intcode(mem)
                next(prog)
                prog.send(x)
                v = prog.send(y)
                assert isinstance(v, int), v

            if step != 1:
                x += step

        # see if bottom left of box is also set - box is 100x100 inclusive, so
        # offset of 99 from found x/y
        nx = x - 99
        ny = y + 99
        prog = intcode(mem)
        next(prog)
        prog.send(nx)
        v = prog.send(ny)
        assert isinstance(v, int), v

        if v:
            break

    debug(x, y, nx, ny)

    print(nx * 10000 + y)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
