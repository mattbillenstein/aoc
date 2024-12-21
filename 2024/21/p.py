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

    maxlevel = 3

    def generate(code, pos='A', level=1):
        # generate all new codes from given code using paths
        s = pos + code
        L = []
        for i in range(len(s)-1):
            k, nk = s[i], s[i+1]
            L.append(paths[(k, nk)])

        for tup in itertools.product(*L):
            s = 'A'.join(tup) + 'A'
            if len(s) <= best[level]:
                best[level] = len(s)
                if level < maxlevel:
                    for x in generate(s, level=level+1):
                        yield x
                else:
                    yield s
                        
    tot = 0
    for code in codes:
        best = defaultdict(lambda: 10000000000000)
        sbest = ''
        for s in generate(code):
            if not sbest or len(s) < len(sbest):
                sbest = s
                print()
                print(code)
                print(s)

        num = int(''.join(_ for _ in code if _ != 'A'))
        print(code, sbest, len(sbest), num)
        num *= len(sbest)
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
