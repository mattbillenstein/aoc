#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [tuple(_.split('-')) for _ in lines]
    return (lines,)

def part(data):
    conns = defaultdict(set)
    for a, b in data:
        conns[a].add(b)
        conns[b].add(a)

    if '1' in sys.argv:
        x = set()
        for c1, s in conns.items():
            for c2 in s:
                for c3 in conns[c2]:
                    if c3 in s:
                        x.add(tuple(sorted([c1, c2, c3])))

        print(len([_ for _ in x if any(c[0] == 't' for c in _)]))

    if '2' in sys.argv:
        mx = set()
        for c, s in conns.items():
            # set for everything connected at c
            x = set(s)
            x.add(c)

            # remove anything in the set that's not connected to everything
            # else...
            for c2 in list(x):
                for c3 in list(x):
                    if c2 == c3:
                        continue
                    if c2 in x and c3 not in conns[c2]:
                        x.remove(c3)
                        break
            
            if len(x) > len(mx):
                mx = x

        print(','.join(sorted(mx)))

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
