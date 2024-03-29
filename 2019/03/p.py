#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import SparseGrid, manhattan_distance

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [[(_[0], int(_[1:])) for _ in x.split(',')] for x in lines]
    return lines

def run(data):
    g = SparseGrid([], {'.': 0, '*': 1, 'X': 2})

    crosses = set()
    for i, wire in enumerate(data):
        pt = (0, 0)
        for dir, cnt in wire:
            for _ in range(cnt):
                pt = g.step(pt, dir)
                v = g.get(pt)

                if i == 0:
                    g.set(pt, 1)
                elif v:
                    g.set(pt, 2)
                    crosses.add(pt)

#    print(crosses)
    print(min(manhattan_distance((0, 0), pt) for pt in crosses))

    # Retrace recording crosses with how many steps it took to get there...
    steps = defaultdict(dict)

    for i, wire in enumerate(data):
        pt = (0, 0)
        step = 0
        for dir, cnt in wire:
            for _ in range(cnt):
                pt = g.step(pt, dir)
                step += 1
                if pt in crosses and i not in steps[pt]:
                    steps[pt][i] = step

    print(min(sum(_.values()) for _ in steps.values()))

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
