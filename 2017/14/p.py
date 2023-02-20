#!/usr/bin/env pypy3

import itertools
import math
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
    return lines[0]

def knot_hash(data):
    def xor(L):
        x = L[0]
        for y in L[1:]:
            x ^= y
        return x

    data = [ord(_) for _ in data] + [17, 31, 73, 47, 23]
    nums = list(range(256))
    pos = skip = 0
    size = len(nums)
    for _ in range(64):
        for length in data:
            nums = nums * 2
            nums[pos:pos+length] = reversed(nums[pos:pos+length])
            nums[:pos] = nums[size:size+pos]
            nums = nums[:size]
            pos = (pos + length + skip) % size
            skip += 1

    L = [xor(nums[_:_+16]) for _ in range(0, len(nums), 16)]
    s = ''.join([f'{_:02x}' for _ in L])
    return s

def part1(s):
    cnt = 0
    for i in range(128):
        h = knot_hash(f'{s}-{i}')
        b = bin(int(h, 16))[2:].zfill(128)
        debug(i, h, b, len(b))
        cnt += b.count('1')

    print(cnt)

def neighbors(pt, pts):
    for npt in [(pt[0]-1, pt[1]), (pt[0]+1, pt[1]), (pt[0], pt[1]-1), (pt[0], pt[1]+1)]:
        if npt in pts:
            yield npt

def part2(s):
    pts = {}
    for y in range(128):
        h = knot_hash(f'{s}-{y}')
        b = bin(int(h, 16))[2:].zfill(128)
        for x, c in enumerate(b):
            if c == '1':
                pts[(x, y)] = None

    # set one point
    for pt in pts:
        pts[pt] = 1
        break

    # iterate points and set
    for pt, g in pts.items():
        # neighboring points in a group
        L = [pts[_] for _ in neighbors(pt, pts) if pts[_] is not None]
        if L:
            # set pt to the min group in neighbors
            if g is None:
                g = min(L)
                pts[pt] = g

            # merge groups by setting all other groups that connect through
            # this point to g
            other = [_ for _ in L if _ != g]
            for o in other:
                for npt in pts:
                    if pts[npt] == o:
                        pts[npt] = g
        else:
            if g is None:
                # create a new group
                pts[pt] = g = max([_ for _ in pts.values() if _ is not None]) + 1
            # set all neighbors to the new group - empty L means no neighbors
            # in a group...
            for npt in neighbors(pt, pts):
                pts[npt] = g

    print(len(set(pts.values())))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
