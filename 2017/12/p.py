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
    conns = {}
    for line in lines:
        line = line.replace(',', '')
        L = line.split()
        L.remove('<->')
        L = [int(_) for _ in L]
        conns[L[0]] = L[1:]
    return conns

def find(data, n, visited):
    visited.add(n)
    if n == 0 or 0 in data[n]:
        return True
    return any(find(data, _, visited) for _ in data[n] if _ not in visited)
    
def part(data):
    cnt = 0
    s = set(data[0])
    s.add(0)
    groups = [s]
    for n, L in data.items():
        s = set()
        if find(data, n, s):
            cnt += 1

        found = False
        for g in groups:
            if g.intersection(s):
                g.update(s)
                found = True
                break
        if not found:
            groups.append(s)

    print(cnt)
    print(len(groups))

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
