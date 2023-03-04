#!/usr/bin/env pypy3

import copy
import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    stacks = defaultdict(list)
    stacklines = []
    ops = []

    for line in lines:
        if not line:
            continue

        if line.startswith(' 1 '):
            stacklines.reverse()
            for i, c in enumerate(line.rstrip()):
                if c != ' ':
                    stacks[c] = [_[i] for _ in stacklines if _[i] != ' ']

        elif line.startswith('move '):
            _, cnt, _, s1, _, s2 = line.strip().split()
            cnt = int(cnt)
            ops.append((cnt, s1, s2))
        else:
            stacklines.append(line)

    return stacks, ops

def part(stacks, ops, part):

    for cnt, s1, s2 in ops:
        items = stacks[s1][-cnt:]
        del stacks[s1][-cnt:]

        if part == 1:
            items.reverse()

        stacks[s2].extend(items)

    if DEBUG:
        for k, L in stacks.items():
            print(k, L)

    print(''.join(_[-1] for _ in stacks.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part(*copy.deepcopy(data), 1)
    if '2' in sys.argv:
        part(*copy.deepcopy(data), 2)

if __name__ == '__main__':
    main()
