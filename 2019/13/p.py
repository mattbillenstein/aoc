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
    prog = intcode(mem)

    g = SparseGrid([], {'.': 0, '#': 1, 'B': 2, 'P': 3, 'O': 4})

    while 1:
        try:
            x = next(prog)
            y = next(prog)
            tile = next(prog)
            g.set((x, y), tile)
        except StopIteration:
            break

    if DEBUG:
        g.print()

    cnt = sum(1 for _ in g if g.get(_) == 2)
    print(cnt)

def part2(mem):
    # set to play
    mem[0] = 2

    prog = intcode(mem)

    joystick = 0
    def gen():
        while (x := prog.send(joystick)) == 'INPUT':
            pass
        return x

    g = SparseGrid([], {'.': 0, '#': 1, 'B': 2, 'P': 3, 'O': 4})
    score = 0
    paddle = None
    ball = None
    x = None

    while 1:
        try:
            if x is None:
                x = next(prog)
            else:
                x = gen()
            y = gen()
            if x == -1 and y == 0:
                score = gen()
                continue

            tile = gen()
            if tile == 3:
                paddle = (x, y)
            elif tile == 4:
                ball = (x, y)

                # Simple enough to just follow the ball with the paddle...
                joystick = 0
                if paddle and paddle[0] > ball[0]:
                    joystick = -1
                elif paddle and paddle[0] < ball[0]:
                    joystick = 1

            g.set((x, y), tile)

            if DEBUG and tile in (3, 4):
                print()
                g.print()
                print('Score:', score)
        except StopIteration:
            break

    if DEBUG:
        print()
        g.print()

    print(score)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
