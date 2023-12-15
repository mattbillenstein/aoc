#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    L = []
    for line in lines:
        x, y = line.split()
        Y = tuple([int(_) for _ in y.split(',')])
        L.append((x, Y))
    return L

def search(x, y, cache, in_run=False):
    key = (x, y, in_run)
    if key in cache:
        return cache[key]

    if len(y) == 1 and y[0] == 0:
        if '#' not in x:
            return 1
        else:
            return 0
    if not x:
        return 0

    tot = 0

    if x[0] == '?':
        # place #, decrement counter
        if y[0] > 0:
            tot += search(x[1:], (y[0]-1,) + y[1:], cache, True)

        if y[0] == 0:
            # place ., skip to next counter
            tot += search(x[1:], y[1:], cache, False)
        elif not in_run:
            # place ., repeat on current gap
            tot += search(x[1:], y, cache, False)
    elif x[0] == '.':
        if y[0] == 0:
            # found ., skip to next counter
            tot += search(x[1:], y[1:], cache, False)
        elif not in_run:
            # found ., repeat on current gap
            tot += search(x[1:], y, cache, False)
    elif x[0] == '#':
        if y[0] > 0:
            # place #, dec counter
            tot += search(x[1:], (y[0]-1,) + y[1:], cache, True)

    cache[key] = tot
    return tot

def part1(data):
    tot = 0
    for x, y in data:
        cache = {}
        c = search(x, y, cache)
        tot += c
    print(tot)

def part2(data):
    ndata = []
    for x, y in data:
        X = ''
        Y = tuple()
        for i in range(5):
            X += x + '?'
            Y += y
        X = X[:-1]

        ndata.append((X, Y))

    part1(ndata)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
