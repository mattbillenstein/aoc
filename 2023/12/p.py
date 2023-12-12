#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    L = []
    for line in lines:
        x, y = line.split()
        Y = [int(_) for _ in y.split(',')]
        L.append((x, Y))
    return L

def search(x, y, cache, in_run=False, lvl='', current=''):
    key = (x, tuple(y))
    if key in cache:
        return cache[key]

    if DEBUG > 1:
        print(lvl + 'search', x, y, in_run, repr(current))

#    if current.endswith('..........'):
#        if DEBUG > 1:
#            print('abort')
#        return 0
#
#    if x.count('#') > sum(y):
#        print('ABORT')
#        return 0

    if len(y) == 1 and y[0] == 0:
        if '#' not in x:
            if DEBUG > 1:
                print(lvl + 'score')
            return 1
        else:
            return 0
    if not x:
        return 0

    tot = 0

    if x[0] == '?':
        # place #, decrement counter
        if y[0] > 0:
            y[0] -= 1
            tot += search(x[1:], y, cache, True, lvl + '  ', current + '#')
            y[0] += 1

        if y[0] == 0:
            # place ., skip to next counter
            tot += search(x[1:], y[1:], cache, False, lvl + '  ', current + '.')
        elif not in_run:
            # place ., repeat on current gap
            tot += search(x[1:], y, cache, False, lvl + '  ', current + '.')
    elif x[0] == '.':
        if y[0] == 0:
            # found ., skip to next counter
            tot += search(x[1:], y[1:], cache, False, lvl + '  ', current + x[0])
        elif not in_run:
            # found ., repeat on current gap
            tot += search(x[1:], y, cache, False, lvl + '  ', current + x[0])
    elif x[0] == '#':
        if y[0] > 0:
            # place #, dec counter
            y[0] -= 1
            tot += search(x[1:], y, cache, True, lvl + '  ', current + x[0])
            y[0] += 1

    cache[key] = tot
    return tot

def part1(data):
    tot = 0
    for x, y in data:
        c = search(x, y, {})
        tot += c
        debug(x, y, c)
    print(tot)

def part2(data):
    ndata = []
    for x, y in data:
        X = ''
        Y = []
        for i in range(5):
            X += x + '?'
            Y.extend(y)
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
