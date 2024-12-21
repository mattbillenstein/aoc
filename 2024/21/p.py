#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from functools import lru_cache
from pprint import pprint

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return (lines,)

def canon(s):
    x = s.split('A')
    x = [''.join(sorted(list(_))) for _ in x]
    x = 'A'.join(x)
    return x

def find_paths(ckey, nkey, g):
    def find(path):
        pt, dir = path[-1]
        if g.getc(pt) == nkey:
            yield ''.join([_[1] for _ in path[1:]])

        visited = [_[0] for _ in path]
        for ndir in '<>v^':
            npt = g.step(pt, ndir)
            if npt and npt not in visited and g.getc(npt) != '#':
                for x in find(path + ((npt, ndir),)):
                    yield x

    for spt in g:
        if g.getc(spt) == ckey:
            break

    paths = []
    for path in find(((spt, None),)):
        paths.append(path)

    # filter down to all min paths of same length - I don't think there can be
    # a case where a longer path is desired?
    if paths:
        mn = min(len(_) for _ in paths)
        paths = [_ for _ in paths if len(_) == mn]

    return paths

def part1(codes):
    dg = Grid(['#^A', '<v>'])
    ng = Grid(['789', '456', '123', '#0A'])

    paths = defaultdict(list)
    for g in (dg, ng):
        for pt1 in g:
            c1 = g.getc(pt1)
            if c1 == '#':
                continue
            for pt2 in g:
                c2 = g.getc(pt2)
                if c2 == '#':
                    continue
                for path in find_paths(c1, c2, g):
                    paths[(c1, c2)].append(path)

    check = [
        '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
        'v<<A>>^A<A>AvA<^AA>A<vAAA>^A',
        '<A^A>^^AvvvA',
        '029A',
    ]

    def generate(code):
        # generate all new codes from given code using paths
        s = 'A' + code
        L = []
        for i in range(len(s)-1):
            k, nk = s[i], s[i+1]
            L.append(paths[(k, nk)])

        for tup in itertools.product(*L):
            yield 'A'.join(tup) + 'A'

    tot = 0
    for code in codes:
        best = ''
        for s1 in generate(code):
            for s2 in generate(s1):
                for s3 in generate(s2):
                    if not best or len(s3) < len(best):
                        best = s3
                        print()
                        print(code)
                        print(s1)
                        print(s2)
                        print(s3)

        num = int(''.join(_ for _ in code if _ != 'A'))
        print(code, best, len(best), num)
        num *= len(best)
        tot += num

    print(tot)

            
def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
