#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    L = [0] * len(data[0])
    for line in data:
        for i, v in enumerate(line):
            if v == '1':
                L[i] += 1

    gamma = ''.join(['1' if _ > len(data)//2 else '0' for _ in L])
    gamma = int(gamma, 2)
    epsilon = ''.join(['1' if _ < len(data)//2 else '0' for _ in L])
    epsilon = int(epsilon, 2)

    print(gamma * epsilon)

def part2(data):
    ox = list(data)

    i = 0
    while len(ox) > 1:
        ones = sum(int(_[i]) for _ in ox)
        zeros = len(ox) - ones
        keep = '1' if ones >= zeros else '0'
        ox = [_ for _ in ox if _[i] == keep]
        i += 1

    ox = int(ox[0], 2)

    co = list(data)

    i = 0
    while len(co) > 1:
        ones = sum(int(_[i]) for _ in co)
        zeros = len(co) - ones
        keep = '0' if zeros <= ones else '1'
        co = [_ for _ in co if _[i] == keep]
        i += 1

    co = int(co[0], 2)

    print(ox * co)

def main(argv):
    data = parse_input()

    part1(data)
    part2(data)

if __name__ == '__main__':
    main(sys.argv)
