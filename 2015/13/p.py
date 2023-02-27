#!/usr/bin/env pypy3

import copy
import itertools
import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    happiness = defaultdict(dict)
    for line in lines:
        L = line.replace('.', '').split()
        n1 = L[0]
        n2 = L[-1]
        h = int(L[3])
        if L[2] == 'lose':
            h = -h
        happiness[n1][n2] = h
    return happiness

def part1(happiness):
    best_score = 0
    best_seating = None
    for tup in itertools.permutations(list(happiness), len(happiness)):
        score = 0
        for i in range(1, len(tup)-1, 1):
            n0, n1, n2 = tup[i-1:i+2]
            score += happiness[n1][n0]
            score += happiness[n1][n2]

        n0, n1, n2 = tup[-1], tup[0], tup[1]
        score += happiness[n1][n0]
        score += happiness[n1][n2]

        n0, n1, n2 = tup[-2], tup[-1], tup[0]
        score += happiness[n1][n0]
        score += happiness[n1][n2]

        if score > best_score:
            best_score = score
            best_seating = tup


    debug(best_seating)
    print(best_score)

def part2(happiness):
    # Add myself and redo it...
    for n, d in happiness.items():
        d['Matt'] = 0
    happiness['Matt'] = {_: 0 for _ in happiness}
    part1(happiness)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
