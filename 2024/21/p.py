#!/usr/bin/env pypy3

import sys
from functools import lru_cache

from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return (lines,)

def make_paths(cpt, npt, g):
    # only take L paths if they don't pass through the # in the grid
    if cpt == npt:
        return ['A']

    # this was trial/error from other ppl in the solutions thread - how can
    # this be derived?
    move_priority = '<^v>'

    dx = npt[0] - cpt[0]
    dy = npt[1] - cpt[1]
    cx = '>' if dx > 0 else '<'
    cy = 'v' if dy > 0 else '^'
    dx = abs(dx)
    dy = abs(dy)

    paths = []
    for path in set([cx * dx + cy * dy, cy * dy + cx * dx]):
        valid = True
        pt = cpt
        for dir in path:
            pt = g.step(pt, dir)
            if g.getc(pt) == '#':
                valid = False
                break
        if valid:
            paths.append(path + 'A')

    paths.sort(key=lambda x: [move_priority.index(_) for _ in x[:-1]])

    return [paths[0]]

def part(codes):
    # use small grids to generate paths
    dg = Grid(['#^A', '<v>'])
    ng = Grid(['789', '456', '123', '#0A'])

    # for each pair of points on each grid, generate the shortest path we can
    # take between them...
    paths = {}
    for g in (dg, ng):
        for pt1 in g:
            c1 = g.getc(pt1)
            if c1 == '#':
                continue
            for pt2 in g:
                c2 = g.getc(pt2)
                if c2 == '#':
                    continue
                paths[(c1, c2)] = make_paths(pt1, pt2, g)

    if DEBUG > 1:
        for k, v in sorted(paths.items()):
            print(k, v)
        return

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
            if len(s1) < best:
                best = len(s1)
                s = s1
        return s

    @lru_cache(maxsize=None)
    def compute_length(code, times):
        if 'A' in code[:-1]:
            return sum(compute_length(_, times) for _ in split(code))

        if times:
            return sum(compute_length(_, times-1) for _ in split(next_code(code)))
        else:
            return len(code)

    tot1 = tot2 = 0
    for code in codes:
        num = int(code.lstrip('A0').rstrip('A'))

        # compute numpad code
        ncode = next_code(code)

        if DEBUG:
            print(code, ncode, len(ncode))
            for i in range(2):
                ncode = next_code(ncode)
                print(code, ncode, len(ncode))
            print()

            n1 = len(ncode)
            n2 = 0
        else:
            n1 = compute_length(ncode, 2)
            n2 = compute_length(ncode, 25)
            # print(code, n, num)

        tot1 += num * n1
        tot2 += num * n2

    if '1' in sys.argv:
        print(tot1)
    if '2' in sys.argv:
        print(tot2)

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
