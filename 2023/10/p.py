#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines, {'I': 1, 'O': 2, 'X': 3})

def fill(grid, pt):
    q = [pt]
    found = set()
    border = set()
    while q:
        pt = q.pop()
        found.add(pt)
        for npt in [grid.step(pt, _) for _ in '<>v^']:
            # found the edge, can just abort
            if npt is None:
                border.add(npt)
                continue

            if npt in found:
                continue

            c = grid.getc(npt)
            if c == '.':
                q.append(npt)
            else:
                border.add(npt)

    return found, border

def parts(grid):
    for pt in grid:
        if grid.getc(pt) == 'S':
            start = pt
            for dir in '<>^v':
                npt = grid.step(pt, dir)
                if npt and grid.getc(npt) in ('|', '-'):
                    sdir = dir
                    break
            break

    # trace to find the path
    path = set()

    # sets of empty spaces inside or outside the path, may swap later...
    ins = set()
    outs = set()

    dist = 0
    pt = start
    dir = sdir
    while 1:
        path.add(pt)
        dist += 1

        pt = grid.step(pt, dir)
        c = grid.getc(pt)
        if c == 'S':
            break

        inc, outc = '', ''
        if c  == '-':
            inc, outc = '^', 'v'
            if dir == '<':
                inc, outc = outc, inc
        elif c == '|':
            inc, outc = '>', '<'
            if dir == '^':
                inc, outc = outc, inc
        elif c == 'J':
            if dir == '>':
                dir = '^'
                outc = 'v>'
            else:
                assert dir == 'v'
                dir = '<'
                inc = 'v>'
        elif c == 'F':
            if dir == '^':
                dir = '>'
                inc = '<^'
            else:
                assert dir == '<'
                dir = 'v'
                outc = '<^'
        elif c == 'L':
            if dir == '<':
                dir = '^'
                inc = 'v<'
            else:
                assert dir == 'v'
                dir = '>'
                outc = 'v<'
        elif c == '7':
            if dir == '>':
                dir = 'v'
                inc = '^>'
            else:
                assert dir == '^'
                dir = '<'
                outc = '^>'

        for x in (inc, outc):
            for ndir in x:
                npt = grid.step(pt, ndir)
                if not npt:
                    continue
                nc = grid.getc(npt)
                if nc == '.':
                    if ndir in inc:
                        ins.add(npt)
                    else:
                        outs.add(npt)

    # part1, half of distance is the furthest away from start we can get...
    print(dist // 2)

    for pt in grid:
        if pt not in path:
            grid.setc(pt, '.')

    if DEBUG:
        grid.print()

    # trace again to collect fill points
    path = set()

    # sets of empty spaces inside or outside the path, may swap later...
    ins = set()
    outs = set()

    dist = 0
    pt = start
    dir = sdir
    while 1:
        path.add(pt)
        dist += 1

        pt = grid.step(pt, dir)
        c = grid.getc(pt)
        if c == 'S':
            break

        inc, outc = '', ''
        if c  == '-':
            inc, outc = '^', 'v'
            if dir == '<':
                inc, outc = outc, inc
        elif c == '|':
            inc, outc = '>', '<'
            if dir == '^':
                inc, outc = outc, inc
        elif c == 'J':
            if dir == '>':
                dir = '^'
                outc = 'v>'
            else:
                assert dir == 'v'
                dir = '<'
                inc = 'v>'
        elif c == 'F':
            if dir == '^':
                dir = '>'
                inc = '<^'
            else:
                assert dir == '<'
                dir = 'v'
                outc = '<^'
        elif c == 'L':
            if dir == '<':
                dir = '^'
                inc = 'v<'
            else:
                assert dir == 'v'
                dir = '>'
                outc = 'v<'
        elif c == '7':
            if dir == '>':
                dir = 'v'
                inc = '^>'
            else:
                assert dir == '^'
                dir = '<'
                outc = '^>'

        for x in (inc, outc):
            for ndir in x:
                npt = grid.step(pt, ndir)
                if not npt:
                    continue
                nc = grid.getc(npt)
                if nc == '.':
                    if ndir in inc:
                        ins.add(npt)
                    else:
                        outs.add(npt)

    foundins = set()
    borderins = set()
    for pt in ins:
        if pt in foundins:
            continue
        f, b = fill(grid, pt)
        foundins.update(f)
        borderins.update(b)

    foundouts = set()
    borderouts = set()
    for pt in outs:
        if pt in foundouts:
            continue
        f, b = fill(grid, pt)
        foundouts.update(f)
        borderouts.update(b)

    if None in borderins:
        borderins, borderouts = borderouts, borderins
        foundins, foundouts = foundouts, foundins

    if DEBUG:
        for pt in foundins:
            grid.setc(pt, 'X')

        print()
        grid.print()

        print(None in borderouts)
        print(None in borderins)
        print(len(foundouts))
    print(len(foundins))

def main():
    data = parse_input()
    parts(data)

if __name__ == '__main__':
    main()
