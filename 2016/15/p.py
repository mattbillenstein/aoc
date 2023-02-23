#!/usr/bin/env pypy3

import copy
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    discs = []
    for line in lines:
        for c in '#.=,':
            line = line.replace(c, ' ')
        L = line.split()
        disc = {
            'i': int(L[1]),
            'slots': int(L[3]),
            't': int(L[7]),
            'pos': int(L[12]),
        }
        discs.append(disc)
    return discs

def part1(discs):
    t = 0
    done = False
    while not done:
        t += 1
        done = True
        for disc in discs:
            disc['pos'] = (disc['pos'] + 1) % disc['slots']
            if (disc['pos'] + disc['i']) % disc['slots'] != 0:
                done = False

    print(t)

def part2(discs):
    disc = dict(discs[-1])
    disc['i'] += 1
    disc['slots'] = 11
    disc['pos'] = 0
    discs.append(disc)
    part1(discs)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
