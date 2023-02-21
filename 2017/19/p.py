#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part(data):
    chars = {' ': 0}
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for c in '|-+' + letters:
        chars[c] = ord(c)

    g = Grid(data, chars)
    if DEBUG:
        g.print()

    for x in g.xs:
        pt = (x, 0)
        if g.getc(pt) == '|':
            break

    dir = 'v'
    order = []
    steps = 0
    while 1:
        steps += 1
        debug(pt, dir)
        lastpt = pt
        pt = g.step(pt, dir)
        c = g.getc(pt)
        if c in letters:
            order.append(c)
        elif c == ' ':
            break
        elif c == '+':
            for npt in g.neighbors4(pt):
                if npt == lastpt:
                    continue
                x = g.getc(npt)
                if dir in '^v' and x == '-':
                    if npt[0] > pt[0]:
                        dir = '>'
                    else:
                        dir = '<'
                    break
                elif dir in '<>' and x == '|':
                    if npt[1] > pt[1]:
                        dir = 'v'
                    else:
                        dir = '^'
                    break

    print(''.join(order))
    print(steps)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
