#!/usr/bin/env pypy3

import random
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import SparseGrid
from intcode import intcode

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def part(mem):
    chars = {_: ord(_) for _ in '#<>v^'}
    chars['.'] = 0
    g = SparseGrid([], chars)

    prog = intcode(mem)
    x, y = 0, 0
    for v in prog:
        c = chr(v)
        if c == '\n':
            x = 0
            y += 1
            continue
            
        if c != '.':
            g.set((x, y), v)
        x += 1

    if DEBUG:
        print()
        g.print()

    intersections = []
    for pt in g:
        if all(g.get(g.step(pt, _)) == chars['#'] for _ in '<>v^'):
            intersections.append(pt)

    debug(intersections)
    print(sum(x*y for x, y in intersections))

    # wake up bot
    mem[0] = 2

    intersections = set(intersections)
    visited = set()

    cnt = 0
    for pt in g:
        v = g.get(pt, 0)
        c = chr(v)
        if c in '<>^v':
            pos = pt
        if c == '#':
            cnt += 1

    directions = []
    dir = chr(g.get(pos))

    debug(pos, cnt, dir)

    g2 = SparseGrid([], chars)

    # I think I need to consider turning at intersections here - can't find a
    # repeating set of sequences that covers the given path...

    # trace backwards from the bot location until we visit the entire path,
    # first compute a 90-degree turn, then step until we hit another corner -
    # repeat
    while len(visited) < cnt:
        # compute turn
        for ndir in '<>^v':
            pt = g.step(pos, ndir)
            if not pt in visited and g.get(pt):
                turn = {
                    '^': {'<': 'L', '>': 'R'},
                    '<': {'v': 'L', '^': 'R'},
                    'v': {'>': 'L', '<': 'R'},
                    '>': {'^': 'L', 'v': 'R'},
                }[dir][ndir]
                directions.append(turn)
                dir = ndir
                break

        steps = 0
        while 1:
            npos = g.step(pos, dir)
            if not g.get(npos):
                break
            pos = npos
            visited.add(pos)
            g2.set(pos, ord('#'))
            steps += 1

        directions.append(steps)

    print(directions)
    print(len(directions))

    if 0:
        # common steps are 4/8 and 6/12, break apart 8's and 12's
        ndirs = []
        for x in directions:
            if not isinstance(x, int):
                ndirs.append(x)
            elif x % 3 == 0:
                ndirs.extend([3] * (x // 3))
            elif x % 4 == 0:
                ndirs.extend([4] * (x // 4))
            else:
                assert 0

        directions = ndirs
        print(directions)
        print(len(directions))

    matches = defaultdict(set)
    for i in range(0, len(directions)):
#        if directions[i] not in ('L', 'R'):
#            continue
        for j in range(0, len(directions)):
            if i == j:
                continue

            k = 2
            while directions[i:i+k] == directions[j:j+k] and k < 20:
                i, j = min(i, j), max(i, j)
                d = tuple(directions[i:i+k])
                matches[d].add((i, j))

                k += 1

    for k, v in matches.items():
        print(k, v)
    print(len(matches))

    for a, b, c in itertools.combinations(list(matches), 3):
        # see if we can consume using just these components...
        L = []
        d = tuple(directions)
        found = True
        while d and found:
            found = False
            for tup in (a, b, c):
                if d[:len(tup)] == tup:
                    found = True
                    d = d[len(tup):]
                    L.append(tup)
                    break

        if not d:
            print('matched', a, b, c, L)
    
    if DEBUG:
        print()
        g2.print()

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
