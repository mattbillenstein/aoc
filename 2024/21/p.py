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
    # use small grids to generate paths
    dg = Grid(['#^A', '<v>'])
    ng = Grid(['789', '456', '123', '#0A'])

    # for each pair of points on each grid, generate a set of shortest paths we
    # can take between them...
    paths = defaultdict(set)
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
                    paths[(c1, c2)].add(path + 'A')

    #pprint(dict(paths))

    def generate(pos, code, ncode=''):
        # from starting position and code, generate possible next codes
        if not code:
            yield ncode
        else:
            for path in paths[(pos, code[0])]:
                for s in generate(code[0], code[1:], ncode + path):
                    yield s

    def split(code):
        # split a code on 'A' and return list of parts
        return [_ + 'A' for _ in code.split('A')[:-1]]

    @lru_cache(maxsize=None)
    def next_code(code):
        # given a code, generate the next code that will result in the shortest
        # descendant codes...

        # if we can split the code, do so and recurse
        if 'A' in code[:-1]:
            s = ''
            for p in split(code):
                s += next_code(p)
            return s

        # brute force find shortest code by inspecting several levels of
        # descendant codes...
        best = sys.maxsize
        for s1 in generate('A', code):
            for s2 in generate('A', s1):
                for s3 in generate('A', s2):
                    if len(s3) < best:
                        best = len(s3)
                        s = s1
        return s

    for k, L in paths.items():
        if len(L) > 1:
            mn = min(len(next_code(next_code(_))) for _ in L)
            #print(k, L)
            for x in list(L):
                nc = next_code(next_code(x))
                if len(nc) != mn:
                    L.remove(x)
                #print('  ', x, nc, len(nc))

    #pprint(dict(paths))
    #return

    @lru_cache(maxsize=None)
    def compute_length(code, times):
        #print(code, times)
        if 'A' in code[:-1]:
            return sum(compute_length(_, times) for _ in split(code))

        if times:
            return sum(compute_length(_, times-1) for _ in split(next_code(code)))
            #return compute_length(next_code(code), times-1)
        else:
            return len(code)

    tot = 0
    for code in codes:
        num = int(code.lstrip('A0').rstrip('A'))

        # compute numpad code
        ncode = next_code(code)

        if DEBUG:
            print(code, ncode, len(ncode))

            for i in range(2):
                ncode = next_code(ncode)

            n = len(ncode)
            print(code, ncode, n, num)
        else:
            n = compute_length(ncode, 2)  # fixme, 25
           # print(code, n, num)

        tot += num * n

    print(tot)

    # 277554934879758 too high times=25
    # 175396398527088 too low times=25
    # 110880490505014 too low times=24

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
