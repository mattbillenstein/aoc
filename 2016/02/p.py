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
    return [_.strip('\r\n') for _ in sys.stdin]

def part1(data):
    def getkey(key, dir):
        if dir == 'D' and key < 7:
            key += 3
        elif dir == 'U' and key > 3:
            key -= 3
        elif dir == 'L' and key not in (1, 4, 7):
            key -= 1
        elif dir == 'R' and key not in (3, 6, 9):
            key += 1
        return key

    s = ''
    key = 5
    for line in data:
        for dir in line:
            key = getkey(key, dir)
        s += str(key)
    print(s)

def part2(data):
    L = [
        [''] * 7,
        ['', '', '',   '1', '', '', ''],
        ['', '',  '2', '3', '4', '', ''],
        ['', '5', '6', '7', '8', '9', ''],
        ['', '',  'A', 'B', 'C', '', ''],
        ['', '', '',   'D', '', '', ''],
        [''] * 7,
    ]
    def getkey(pos, dir):
        x, y = pos
        nx, ny = x, y
        if dir == 'U':
            ny -= 1
        elif dir == 'D':
            ny += 1
        elif dir == 'L':
            nx -= 1
        elif dir == 'R':
            nx += 1

        if L[ny][nx]:
            return (nx, ny)
        return pos

    s = ''
    pos = (1, 3)
    for line in data:
        for dir in line:
            pos = getkey(pos, dir)
        s += L[pos[1]][pos[0]]
    print(s)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
