#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [_.upper() for _ in lines[0].split(',')]

def step_hex(pt, dir):
    # https://www.redblobgames.com/grids/hexagons/
    #
    # using doubled-height horizontal layout - row values are doubled between
    # cells...

    nx, ny = pt
    if dir in ('N',):
        ny -= 2
    elif dir in ('S',):
        ny += 2
    elif dir in ('NW',):
        nx -= 1
        ny -= 1
    elif dir in ('NE',):
        nx += 1
        ny -= 1
    elif dir in ('SW',):
        nx -= 1
        ny += 1
    elif dir in ('SE',):
        nx += 1
        ny += 1
    else:
        assert 0, dir
    return nx, ny

def dist(pt):
    # we can move 2 N/S in a single step and then +/-1,+/-1 diagonally back to
    # 0, 0...
    return abs(abs(pt[0]) - abs(pt[1])) // 2 + min(abs(pt[0]), abs(pt[1]))

def part(data):
    pt = (0, 0)
    maxdist = 0
    for step in data:
        pt = step_hex(pt, step)
        d = dist(pt)
        if d > maxdist:
            maxdist = d

    print(dist(pt))
    print(maxdist)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
