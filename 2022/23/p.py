#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    elves = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                elves.add((x, y))

    return elves

def neighbors(x, y, dir=None):
    if dir == 'N':
        return [(_, y-1) for _ in range(x-1, x+1+1)]
    elif dir == 'S':
        return [(_, y+1) for _ in range(x-1, x+1+1)]
    elif dir == 'W':
        return [(x-1, _) for _ in range(y-1, y+1+1)]
    elif dir == 'E':
        return [(x+1, _) for _ in range(y-1, y+1+1)]
    return [(nx, ny) for ny in range(y-1, y+1+1) for nx in range(x-1, x+1+1) if (nx, ny) != (x, y)]

def new_position(x, y, dir):
    nx, ny = x, y
    if dir == 'N':
        ny -= 1
    elif dir == 'S':
        ny += 1
    if dir == 'W':
        nx -= 1
    elif dir == 'E':
        nx += 1
    return nx, ny

def box(elves):
    minx = min(_[0] for _ in elves)
    maxx = max(_[0] for _ in elves)
    miny = min(_[1] for _ in elves)
    maxy = max(_[1] for _ in elves)

    return (minx, maxx), (miny, maxy)

def print_elves(elves):
    xs, ys = box(elves)

    for y in range(ys[0], ys[1]+1):
        s = ''
        for x in range(xs[0], xs[1]+1):
            s += '#' if (x, y) in elves else '.'
        print(s)

def part1(elves):
    print_elves(elves)
    print()

    dirs = ['N', 'S', 'W', 'E']

    rnd = 0
    while 1:
        rnd += 1

        propose = defaultdict(list)
        for x, y in elves:
            if all(n not in elves for n in neighbors(x, y)):
                continue
        
            for dir in dirs:
                if all(n not in elves for n in neighbors(x, y, dir)):
                    nx, ny = new_position(x, y, dir)
                    propose[(nx, ny)].append((x, y))
                    break

        # now, move elves that were the only one to propose

        for new, L in propose.items():
            if len(L) == 1:
                old = L[0]
                elves.remove(old)
                elves.add(new)

        dirs = dirs[1:] + [dirs[0]]

        if rnd >= 10:
            break

    print_elves(elves)
    print()
    print(len(elves))

    xs, ys = box(elves)
    print(xs, ys)

    print((xs[1] - xs[0] + 1) * (ys[1] - ys[0] + 1) - len(elves))

def part2(elves):
    print(elves)

def main():
    elves = parse_input()
    if '1' in sys.argv:
        part1(elves)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
