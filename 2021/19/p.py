#!/usr/bin/env pypy3

import math
import random
import sys
import time
from collections import defaultdict
from itertools import permutations
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    scanners = {}
    for line in lines:
        if not line:
            continue

        if ' scanner ' in line:
            num = int(line.split()[2])
            scanners[num] = beacons = []
        else:
            beacon = tuple([int(_) for _ in line.split(',')])
            beacons.append(beacon)

    for num, L in scanners.items():
        L.sort()

    return scanners

def adist(pt1, pt2):
    return (abs(pt1[0] - pt2[0]), abs(pt1[1] - pt2[1]), abs(pt1[2] - pt2[2]))

def dist(pt1, pt2):
    return (pt1[0] - pt2[0], pt1[1] - pt2[1], pt1[2] - pt2[2])

def swap(pt, map):
    return (pt[map[0]], pt[map[1]], pt[map[2]])

def flip(pt, map):
    return (pt[0] * map[0], pt[1] * map[1], pt[2] * map[2])

def translate_point(pt, swp, flp, offset=(0, 0, 0)):
    pt = swap(pt, swp)
    pt = flip(pt, flp)
    return (pt[0] + offset[0], pt[1] + offset[1], pt[2] + offset[2])

def reverse_translate_point(pt, swp, flp, offset=(0, 0, 0)):
    pt = (pt[0] - offset[0], pt[1] - offset[1], pt[2] - offset[2])
    pt = flip(pt, flp)
    return swap(pt, SWAPS[swp])

SWAPS = {
    # swap -> rswap
    (1, 0, 2): (1, 0, 2),
    (2, 1, 0): (2, 1, 0),
    (0, 2, 1): (0, 2, 1),

    # rotate -> rrotate
    (0, 1, 2): (0, 1, 2),
    (2, 0, 1): (1, 2, 0),
    (1, 2, 0): (2, 0, 1),
}

FLIPS = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            FLIPS.append((x, y, z))

def translate_reduce(scanners, translate):
    scanners = {k: set(v) for k, v in scanners.items()}

    # iteratively move beacons from one scanner to the next until just zero is
    # left...
    while sum(1 for v in scanners.values() if v) > 1:
        for num in list(scanners):
            if num == 0:
                continue

            translators = [(k, v) for k, v in translate.items() if k[0] == num]
            func = translate_point
            if not translators:
                # reverse into something else...
                translators = [((k[1], k[0]), v) for k, v in translate.items() if k[1] == num]
                func = reverse_translate_point

            # randomly pick a translator so we don't have to actually figure
            # out how to path from N to 0... This will eventually get us there.
            k, trans = random.choice(translators)
            nnum = k[1]

            for pt in scanners[num]:
                pt = func(pt, *trans)
                scanners[nnum].add(pt)
            scanners[num].clear()

    return scanners[0]

def run(scanners):
    # not sure what I'm doing, but try to fingerprint the beacons in each group
    # by computing their manhattan distance to their N closest neighbors -
    # perhaps that lets us match up some in some groups, then the distances to
    # those neighbors should give us an idea of orientation of each sensor...

    distances = defaultdict(list)
    for num, beacons in scanners.items():
        for b1, b2 in permutations(beacons, 2):
            # insert sorted so later matched points are ordered...
            tup = (b2, adist(b1, b2))
            distances[(b1, num)].append(tup)

    if DEBUG:
        print('DISTANCE')
        pprint(distances)
        print()

    matched = defaultdict(list)
    for k, L in distances.items():
        b1, num = k
        L.sort(key=lambda x: sum(x[1]))

        # now key by nearest two manhattan distances
        nk = tuple(sorted([tuple(sorted(L[0][1])), tuple(sorted(L[1][1]))]))
        matched[nk].append((num, b1, L[0][0], L[1][0]))

    if DEBUG:
        print('MATCHED')
        pprint(matched)
        print()

    translate = {}
    for k, L in matched.items():
        if len(L) > 1:
            debug(f'Relate: {[_[0] for _ in L]} {k}')
            debug(L)
            num, p1, p2, p3 = L[0]
            dist1 = dist(p1, p2)
            dist2 = dist(p1, p3)
            debug(num, dist1, dist2)
            for onum, op1, op2, op3 in L[1:]:
                odist1 = dist(op1, op2)
                odist2 = dist(op1, op3)
                debug(onum, odist1, odist2)

                # now figure out which swap/flip matches, compute offset, and
                # store those...
                for swp in SWAPS:
                    for flp in FLIPS:
                        if translate_point(odist1, swp, flp) == dist1 \
                            and translate_point(odist2, swp, flp) == dist2:

                            tp1 = translate_point(op1, swp, flp)
                            offset = (p1[0] - tp1[0], p1[1] - tp1[1], p1[2] - tp1[2])

                            assert translate_point(op1, swp, flp, offset) == p1
                            assert translate_point(op2, swp, flp, offset) == p2

                            assert reverse_translate_point(translate_point(op1, swp, flp, offset), swp, flp, offset) == op1
                            assert reverse_translate_point(translate_point(op2, swp, flp, offset), swp, flp, offset) == op2

                            assert (num, onum) not in translate or translate[(num, onum)] == (swp, flp, offset), ('Mismatch', translate[(num, onum)], (swp, flp, offset))
                            translate[(onum, num)] = (swp, flp, offset)
                            debug(f'Match {num} -> {onum}', swp, flp, offset)


    if DEBUG:
        print('TRANSLATE')
        pprint(translate)

    beacons = translate_reduce(scanners, translate)
    print(len(beacons))

    if DEBUG:
        for b in sorted(beacons):
            print(b)
        print()

    scanners = {k: [(0, 0, 0)] for k in scanners}
    scanners = translate_reduce(scanners, translate)

    # part2 - importantly, manhattan distance between _scanners_ - not
    # beacons...
    mdist = 0
    pts = None
    for b1, b2 in permutations(scanners, 2):
        d = sum(adist(b1, b2))
        if d > mdist:
            mdist = d
            pts = (b1, b2)

    debug(pts)
    print(mdist)

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
