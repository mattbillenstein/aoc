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
    boxes = []
    bins = []

    for line in lines:
        if not line:
            continue
        if line.endswith(':'):
            box = []
            boxes.append(box)
        elif line[0] in '.#':
            box.append(line)
        else:
            assert ': ' in line
            size, counts = line.split(': ')
            size = tuple([int(_) for _ in size.split('x')])
            counts = [int(_) for _ in counts.split()]
            bins.append((size, counts))

    return (boxes, bins)

def part1(boxes, bins):
    # Rather cute, don't need to do any packing at all; just compute the area
    # needed and compare to the area available.
    #
    # Intuitively, with such large areas and so many boxes, you'd think you
    # could almost fill the entire bin full except for this piece with a hole
    # in it except near the edge; so, it's not completely surprising this works
    # I guess.

    box_areas = {}
    for i, b in enumerate(boxes):
        box_areas[i] = sum(_.count('#') for _ in b)

    debug(box_areas)

    # hole in this one that can't be reached...
    box_areas[1] += 1

    tot = 0
    for size, counts in bins:
        area = size[0] * size[1]
        needed = sum(box_areas[i] * c for i, c in enumerate(counts))
        if needed < area:
            tot += 1
        else:
            debug(size, counts, area, needed)

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)

if __name__ == '__main__':
    main()
