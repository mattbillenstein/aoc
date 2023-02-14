#!/usr/bin/env pypy3

import itertools
import math
import random
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

primes = [
#    10_000_019, 8_000_009, 7_000_003, 6_000_011, 5_000_011,
#    4_000_037, 3_000_017, 2_000_003,
    1_000_003, 
    900_001, 800_011, 600_011, 500_009, 300_007, 200_003, 100_003,
    50_021, 25_013, 10_007,
    5003, 2003, 1009, 503, 251, 101, 53, 23, 11, 5, 2, 1
]

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

def part1(bots):
    bots.sort(key=lambda x: x[1])

    b, r = bots[-1]

    cnt = 0
    for bot, r2 in bots:
        if manhattan_distance(b, bot) <= r:
            cnt += 1

    print(cnt)

def count_in_range(pt, bots):
    return sum(1 for b, r in bots if manhattan_distance(pt, b) <= r)

origin = (0, 0, 0)

def prime_search(pt, bots):
    score = count_in_range(pt, bots)
    dist = manhattan_distance(origin, pt)

    times = 5
    for step in primes:
        for x in range(-step * times, step * times, step):
            for y in range(-step * times, step * times, step):
                for z in range(-step * times, step * times, step):
                    npt = (pt[0] + x, pt[1] + y, pt[2] + z)

                    cnt = count_in_range(npt, bots)
                    if cnt >= score:
                        mdist = manhattan_distance(origin, npt)
                        if cnt > score or (cnt == score and mdist < dist):
                            score = cnt
                            dist = mdist
                            pt = npt

    print('prime', pt, score, dist, step)

    return pt, score, dist

def random_search(pt, bots, times=1_000_000):
    score = count_in_range(pt, bots)
    dist = manhattan_distance(origin, pt)

    pt = list(pt)

    step = 1024 * 1024
    while step > 8:
        for _ in range(times):
            npt = list(pt)

            while npt == pt:
                for i in range(3):
                    if random.random() < 0.5:
                        npt[i] += random.randrange(-step, step)

            cnt = count_in_range(npt, bots)
#            print('rnd', pt, npt, cnt)
            if cnt >= score:
                mdist = manhattan_distance(origin, npt)
                if cnt > score or (cnt == score and mdist < dist):
                    score = cnt
                    dist = mdist
                    pt = npt

        step //= 2

        print('rando', pt, score, dist, step)

    return pt, score, dist

def sequential_search(pt, bots):
    score = count_in_range(pt, bots)
    dist = manhattan_distance(origin, pt)

    n = 8
    for x in range(pt[0] - n, pt[0] + n + 1):
        for y in range(pt[1] - n, pt[1] + n + 1):
            for z in range(pt[2] - n, pt[2] + n + 1):
                npt = (x, y, z)

                cnt = count_in_range(npt, bots)
                if cnt >= score:
                    mdist = manhattan_distance(origin, npt)
                    if cnt > score or (cnt == score and mdist < dist):
                        score = cnt
                        dist = mdist
                        pt = npt

    print('seq  ', pt, score, dist)

    return pt, score, dist

def part2(bots):
    # Mostly random search, but we get a good start by walking primes and
    # keeping the best point we find...

    # a solution: [55223783, 15927903, 30447854] 952 101599540 0

    # start at an average point among all the bots
    pt = (
        sum(b[0] for b, r in bots) // len(bots),
        sum(b[1] for b, r in bots) // len(bots),
        sum(b[2] for b, r in bots) // len(bots),
    )
    score = count_in_range(pt, bots)
    dist = manhattan_distance(origin, pt)

    prime_done = set()
    seq_done = set()

    while 1:
        if pt not in prime_done:
            prime_done.add(pt)
            npt, nscore, ndist = prime_search(pt, bots)
            if nscore > score or (nscore == score and ndist < dist):
                pt = tuple(npt)
                score = nscore
                dist = ndist

        npt, nscore, ndist = random_search(pt, bots, 100_000)
        if nscore > score or (nscore == score and ndist < dist):
            pt = tuple(npt)
            score = nscore
            dist = ndist

        if pt not in seq_done:
            seq_done.add(pt)
            npt, nscore, ndist = sequential_search(pt, bots)
            if nscore > score or (nscore == score and ndist < dist):
                pt = tuple(npt)
                score = nscore
                dist = ndist

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
