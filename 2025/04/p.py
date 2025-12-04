#!/usr/bin/env pypy3

import sys

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return Grid(lines)

def remove(g):
    L = []
    for pt in g:
        if g.getc(pt) == '@':
            if sum(1 if g.getc(_) == '@' else 0 for _ in g.neighbors8(pt)) < 4:
                L.append(pt)
    
    for pt in L:
        g.setc(pt, '.')

    return len(L)

def part1(g):
    print(remove(g))

def part2(g):
    tot = 0
    while x := remove(g):
        tot += x
    print(tot)

def main():
    g = parse_input()
    if '1' in sys.argv:
        part1(g.copy())
    if '2' in sys.argv:
        part2(g.copy())

if __name__ == '__main__':
    main()
