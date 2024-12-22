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
        #print('gen', repr(code), repr(ncode), pos, level)
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
        if 'A' in code[:-1]:
            s = ''
            for p in split(code):
                s += next_code(p)
            return s

        # take a code and generate its next two codes returning the next code
        # based on the shortest next next code...
        best = sys.maxsize
        for s1 in generate('A', code):
            for s2 in generate('A', s1):
                for s3 in generate('A', s2):
                    if len(s3) < best:
                        best = len(s3)
                        s = s1
        return s

    tot = 0
    for code in codes:
        ocode = code

        # compute numpad code
        ncode = next_code(code)

        print(code, ncode, len(ncode))

        if 0:
            if code == '029A':
                assert ncode == '<A^A>^^AvvvA', ncode

            code = ncode
            ncode = next_code(code)
            print(code, ncode, len(ncode))
            if code == '029A':
                assert ncode == 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A', ncode

            code = ncode
            ncode = next_code(code)
            print(code, ncode, len(ncode))
            d = {
                '029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
                '980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
                '179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
                '456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
                '379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
            }

            code = ocode
            n = len(ncode)

            if code in d:
                print(code)
                print(ncode, n)
                print(d[code], len(d[code]))

                # diff doesn't matter here if same length...
                #assert ncode == d[ocode]
                assert len(d[code]) == n

            print()

            continue

        if DEBUG:
            for i in range(2):
                ncode = next_code(ncode)

            n = len(ncode)
            num = int(''.join(_ for _ in code if _ != 'A'))
            print(code, ncode, n, num)
        else:
            pass
#           n = compute_length(ncode, 2)
            duh

        num *= n
        tot += num

    print(tot)
    return
    duh
    pprint(cache)

    for code in cache.values():
        val = get_next_code(code)

        print(code)
        parts = split(code)
        print(parts)
        val2 = ''
        for p in parts:
            s = get_next_code(p)
            print('  ', p, s)
            val2 += s

        print(code, val)
        print(code, val2)
        print()

    return

    def find_shortest(code):
        best = sys.maxsize
        L = []
        for s in generate('A', code):
            if len(s) <= best:
                best = len(s)
                yield s

    def take_shortest(codes):
        best = ''
        for code in codes:
            for nc in find_shortest(code):
                if not best or len(nc) < len(best):
                    best = code
        return best

    def find_shortest_length(code, times=1):
        if times > 1:
            tot = 0
            parts = [_ + 'A' for _ in code.split('A')]
            for p in parts:
                nc = take_shortest(find_shortest(p))
                print(' '*times, 'fsl p', p, nc, times)
                tot += find_shortest_length(nc, times-1)
        else:
            nc = take_shortest(find_shortest(code))
            print(' '*times, 'fsl code', code, nc, len(nc), times)
            tot = len(nc)
        print('fsl end', code, times, tot)
        print()
        return tot

    # for each code, take the shortest on the npad
    tot = 0
    for code in codes:
        # take npad code
        if 1:
            ncode = take_shortest(find_shortest(code))
            print(code, ncode, len(ncode))
            if code == '029A':
                assert ncode == '<A^A>^^AvvvA', ncode

            code = ncode
            ncode = take_shortest(find_shortest(code))
            print(code, ncode, len(ncode))
            if code == '029A':
                assert ncode == 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A', ncode

            code = ncode
            ncode = take_shortest(find_shortest(code))
            print(code, ncode, len(ncode))
            if code == '029A':
                assert ncode == '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A', ncode
            print()

            continue

        # find npad codes, take one that generates shortest dpad code
        best = take_shortest(find_shortest(code))
        print('best npad:', best)

        n = find_shortest_length(best, times=2)

        print(best, len(best), n)

        duh

        if code == '029A':
            assert n == 68, (code, dcode, n)
        elif code == '980A':
            assert n == 60, (code, dcode, n)
        elif code == '179A':
            assert n == 68, (code, dcode, n)
        elif code == '456A':
            assert n == 64, (code, dcode, n)
        elif code == '379A':
            assert n == 64, (code, dcode, n)


        num = int(''.join(_ for _ in code if _ != 'A'))
        print('final', code, dcode, n, num)
        num *= n
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
