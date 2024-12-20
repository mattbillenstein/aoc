#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import Grid, manhattan_distance

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    g = Grid(lines, {c: i for i, c in enumerate('.#SE')})
    return (g,)

def part(g):
    # find start end and clear
    start = end = None
    for pt in g:
        c = g.getc(pt)
        if c == 'S':
            start = pt
            g.setc(pt, '.')
        elif c == 'E':
            end = pt
            g.setc(pt, '.')

    # trace the path with no skips
    path = set([start])
    pt = start
    while pt != end:
        for npt in g.neighbors4(pt):
            if g.getc(npt) == '.' and npt not in path:
                pt = npt
                path.add(npt)
                break

    path = tuple(path)
    assert path[0] == start
    assert path[-1] == end

    # lookup index of each point in path
    idxs = {pt: i for i, pt in enumerate(path)}

    save = 100
    # for the test input
    if len(path) < 1000:
        save = 50

    dists = []
    if '1' in sys.argv:
        dists.append(2)
    if '2' in sys.argv:
        dists.append(20)

    if not dists:
        return

    # for each point on path in front of us, if it's manhattan-distance is
    # <= cheat steps away, count it...
    cheats = defaultdict(int)
    tot = 0
    for i, pt in enumerate(path[:-1]):
        for npt in path[i+min(dists):]:
            md = manhattan_distance(pt, npt)
            for cheat in dists:
                if md <= cheat:
                    idx = idxs[npt]
                    new_len = len(path) - (idx - i) + md
                    saved = len(path) - new_len
                    if saved >= save:
                        cheats[cheat] += 1

    for k in sorted(cheats):
        print(cheats[k])

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
