#!/usr/bin/env pypy3

import itertools
import math
import random
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    bots = []
    for line in lines:
        for c in '<>,=':
            line = line.replace(c, ' ')
        L = line.split()
        x, y, z = [int(_) for _ in L[1:4]]
        r = int(L[-1])
        bots.append(((x, y, z), r))
    return bots

def manhattan_distance(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def count_in_range(pt, bots):
    return sum(1 for b, r in bots if manhattan_distance(pt, b) <= r)

def part1(bots):
    bots.sort(key=lambda x: x[1])

    b, r = bots[-1]

    cnt = 0
    for bot, r2 in bots:
        if manhattan_distance(b, bot) <= r:
            cnt += 1

    print(cnt)

def part2(bots):
    # Iteratively try to move in range of an out of range point keeping the
    # best point we've found along the way...
    #
    # This never exits, let it run and try what it outputs, should find a
    # solution in a few minutes...

    # Here are some of them with the same manhattan distance::
    # (54127929, 16826164, 30645449) 945 101599542
    # (54127928, 16826164, 30645448) 947 101599540 *
    # (54144077, 17007607, 30447855) 948 101599539
    # (54144079, 17007607, 30447854) 952 101599540 *
    # (54127927, 17023734, 30447877) 966 101599538
    # (54127928, 17023741, 30447871) 971 101599540 *
    # (54127928, 17023747, 30447866) 972 101599541
    # (54127929, 17023757, 30447857) 973 101599543
    # (54127928, 17023756, 30447856) 974 101599540 *
    # (54127928, 17023757, 30447855) 977 101599540 *
    # (54127928, 17023757, 30447854) 977 101599539

    start = time.time()

    origin = (0, 0, 0)

    # start at an average point among all the bots
    pt = (
        sum(b[0] for b, r in bots) // len(bots),
        sum(b[1] for b, r in bots) // len(bots),
        sum(b[2] for b, r in bots) // len(bots),
    )
    score = count_in_range(pt, bots)
    dist = manhattan_distance(origin, pt)

    print(pt, score, dist, time.time() - start)

    lastpt = None

    while 1:
        # if point changed, recompute list of out of range points
        if pt != lastpt:
            lastpt = pt
            L = [(r - manhattan_distance(pt, b), b, r) for b, r in bots]
            L = [tup for tup in L if tup[0] < 0]
            L.sort(reverse=True)

        # pick a random closer one
        d, b, r = random.choice(L)
        d = abs(d)

        # try random points on the surface
        bad = 0
        for i in range(1000):
            # randomly divide manhattan distance away among each axis
            dx = min(d, abs(pt[0]-b[0]))
            px = random.randrange(0, dx)

            dy = min(d-px, abs(pt[1]-b[1]))
            py = random.randrange(0, dy)

            pz = d - px - py

            if pt[0] > b[0]:
                px = -px
            if pt[1] > b[1]:
                py = -py
            if pt[2] > b[2]:
                pz = -pz

            npt = (pt[0] + px, pt[1] + py, pt[2] + pz)

            ndist = manhattan_distance(b, npt)
            if ndist > r:
                # d remainder overflowed pz, just throw in a random point
                step = max(i, 1)
                npt = (
                    random.randrange(pt[0] - step, pt[0] + step),
                    random.randrange(pt[1] - step, pt[1] + step),
                    random.randrange(pt[1] - step, pt[1] + step),
                )

            cnt = count_in_range(npt, bots)
            mdist = manhattan_distance(origin, npt)
            if cnt > score or (cnt == score and mdist < dist):
                score = cnt
                dist = mdist
                pt = npt

                print(pt, score, dist, time.time() - start)

                # point changed, recompute L
                break

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
