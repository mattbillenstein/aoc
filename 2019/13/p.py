#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
import threading
from collections import defaultdict
from pprint import pprint
from queue import Queue

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

def part1(mem):
    inp = Queue()
    out = Queue()
    prog = threading.Thread(target=intcode, args=(mem, inp, out), daemon=True)
    prog.start()

    g = SparseGrid([], {'.': 0, '#': 1, 'B': 2, 'P': 3, 'O': 4})

    while prog.is_alive():
        x = out.get()
        if x is None:
            break
        y = out.get()
        tile = out.get()
        g.set((x, y), tile)

    if DEBUG:
        g.print()

    cnt = sum(1 for _ in g if g.get(_) == 2)
    print(cnt)

    prog.join()

def part2(mem):
    # set to play
    mem[0] = 2

    inp = Queue()
    out = Queue()
    prog = threading.Thread(target=intcode, args=(mem, inp, out), daemon=True)
    prog.start()

    g = SparseGrid([], {'.': 0, '#': 1, 'B': 2, 'P': 3, 'O': 4})
    score = 0
    joystick = -1
    playing = False
    paddle = None
    ball = None

    while 1:
        x = out.get()
        if x is None:
            break
        y = out.get()
        if x == -1 and y == 0:
            score = out.get()
            playing = True
            continue

        tile = out.get()
        if tile == 3:
            paddle = (x, y)
        elif tile == 4:
            ball = (x, y)

            # after the game paints the ball, it reads input for the joystick
            # position... Simple enough to just follow the ball with the
            # paddle...
            joystick = 0
            if paddle and paddle[0] > ball[0]:
                joystick = -1
            elif paddle and paddle[0] < ball[0]:
                joystick = 1

            inp.put(joystick)

        g.set((x, y), tile)

        if DEBUG and tile in (3, 4):
            print()
            g.print()
            print('Score:', score)

    prog.join()

    if DEBUG:
        print()
        g.print()

    print('Score:', score)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
