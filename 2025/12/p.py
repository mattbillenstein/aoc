#!/usr/bin/env pypy3

import sys

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
    # This has a binomial sort of distribution - there are boxes that only need
    # 65-75% of available area consumed, and everything else is impossible.
    #
    # Intuitively, with such large areas and so many boxes, you'd think you
    # could almost fill the entire bin except perhaps near the edges - there
    # are some perfect tilings with one of each shape, so an actual approach
    # might be to compute those first (taking several hours) and then use those
    # perfect packings to tile the larger shape.

    box_areas = {}
    for i, b in enumerate(boxes):
        box_areas[i] = sum(_.count('#') for _ in b)

    debug(box_areas)

    tot = 0
    for size, counts in bins:
        area = size[0] * size[1]
        needed = sum(box_areas[i] * c for i, c in enumerate(counts))
        debug(f"{needed / area:.3f}", size, counts, area, needed)
        if needed < area:
            tot += 1

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)

if __name__ == '__main__':
    main()
