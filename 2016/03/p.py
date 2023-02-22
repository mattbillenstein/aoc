#!/usr/bin/env pypy3

import copy
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [[int(_) for _ in line.split()] for line in lines]

def part1(data):
    for L in data:
        L.sort()
    print(sum(1 for _ in data if _[2] < _[0] + _[1]))

def part2(data):
    newdata = []
    for i in range(0, len(data), 3):
        for j in range(3):
            newdata.append([data[i][j], data[i+1][j], data[i+2][j]])

    data = newdata
    for L in data:
        L.sort()
    print(sum(1 for _ in data if _[2] < _[0] + _[1]))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
