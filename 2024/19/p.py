#!/usr/bin/env pypy3

import sys
from functools import lru_cache

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    patts = lines[0].replace(',', '').split()
    designs = lines[2:]
    return (tuple(patts), tuple(designs))

def part(patts, designs):
    @lru_cache(maxsize=None)
    def possible(design):
        if not design:
            return 1
        tot = 0
        for patt in patts:
            if design.startswith(patt):
                tot += possible(design[len(patt):])
        return tot

    tot = poss = 0
    for design in designs:
        x = possible(design)
        if x:
            tot += x
            poss += 1

    if '1' in sys.argv:
        print(poss)

    if '2' in sys.argv:
        print(tot)

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
