#!/usr/bin/env pypy3

import random
import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    components = defaultdict(set)
    for line in lines:
        x, y = line.split(': ')
        for y in y.strip().split():
            components[x].add(y)
            components[y].add(x)
    return components

def compute_cut(a, b, comps):
    cut = 0
    for k in a:
        cut += sum(1 for _ in comps[k] if _ in b)
    return cut

def part1(comps):
    # random partition
    a = set()
    b = set()
    for k, v in comps.items():
        s = random.choice([a, b])
        s.add(k)

    # compute cut
    cut = compute_cut(a, b, comps)
    if DEBUG:
        print(a, b, cut)

    # Move the highest-cut item from one set to another - sets don't need to be
    # balanced, but guessing they'll be more or less balanced, so do a weighted
    # sample of the sets based on size
    while cut > 3:
        s = random.choices([a, b], weights=[len(a)/len(comps), len(b)/len(comps)])[0]
        t = a if s is b else b
        if len(s) == 1:
            s, t = t, s

        # Greedy algorithm - find the item that reduces the cut the most
        mx = [0, None]
        for k in s:
            in_t = sum(1 for _ in comps[k] if _ in t)
            in_s = len(comps[k]) - in_t
            diff = in_t - in_s
            if diff > mx[0]:
                mx[0] = diff
                mx[1] = k

        # but if we didn't find one, pick a random one - this will actually
        # increase teh cut
        diff, n = mx
        if not n:
            n = random.choice(tuple(s))
            in_t = sum(1 for _ in comps[n] if _ in t)
            in_s = len(comps[n]) - in_t
            diff = in_t - in_s

        # update
        t.add(n)
        s.remove(n)
        cut -= diff

        if DEBUG:
            assert compute_cut(a, b, comps) == cut, compute_cut(a, b, comps)

        if DEBUG:
            print(len(a), len(b), cut)

    print(len(a) * len(b))

def part2(data):
    # Click the red button!
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
