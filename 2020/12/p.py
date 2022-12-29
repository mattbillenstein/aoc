#!/usr/bin/env pypy3

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
    lines = [(_[0], int(_[1:])) for _ in lines]
    return lines

def part1(data):
    x, y = 0, 0
    dir = 'E'
    for cmd, dist in data:
        if cmd == 'L':
            # encode L as R so we only have to do the lookup table once...
            cmd = 'R'
            dist = 360 - dist

        if cmd == 'R':
            idx = dist // 90 - 1
            if dir == 'E':
                dir = 'SWN'[idx]
            elif dir == 'W':
                dir = 'NES'[idx]
            elif dir == 'N':
                dir = 'ESW'[idx]
            elif dir == 'S':
                dir = 'WNE'[idx]

        if cmd == 'F':
            # change forward to the current dir
            cmd = dir

        if cmd == 'E':
            x += dist
        elif cmd == 'W':
            x -= dist
        elif cmd == 'N':
            y += dist
        elif cmd == 'S':
            y -= dist

    debug(x, y)
    print(abs(y) + abs(x))

def part2(data):
    x, y = 0, 0
    wx, wy = 10, 1
    for cmd, dist in data:
        if cmd == 'L':
            cmd = 'R'
            dist = 360 - dist

        if cmd == 'R':
            # waypoint rotates around ship...
            dx = wx - x
            dy = wy - y

            debug(cmd, dist)
            debug(x, y, wx, wy)
            debug(dx, dy)

            if dist == 90:
                wx = x + dy
                wy = y - dx
            elif dist == 180:
                wx = x - dx
                wy = y - dy
            elif dist == 270:
                wx = x - dy
                wy = y + dx

            debug(x, y, wx, wy)
            debug()

        if cmd == 'F':
            # move to the waypoint dist times and move the waypoint as well...
            dx = wx - x
            dy = wy - y

            x  += dx * dist
            y  += dy * dist
            wx += dx * dist
            wy += dy * dist

        if cmd == 'E':
            wx += dist
        elif cmd == 'W':
            wx -= dist
        elif cmd == 'N':
            wy += dist
        elif cmd == 'S':
            wy -= dist

    debug(x, y)
    print(abs(y) + abs(x))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
