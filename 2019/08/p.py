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
    pixels = [int(_) for _ in lines[0]]
    return pixels

width = 25
height = 6

def part1(data):
    layers = len(data) // width // height
    i = 0
    d = defaultdict(lambda: defaultdict(int))
    for layer in range(layers):
        for y in range(height):
            for x in range(width):
                d[layer][data[i]] += 1
                i += 1

    L = list(d.values())
    L.sort(key=lambda x: x[0])

    print(L[0][1] * L[0][2])

def part2(data):
    layers = len(data) // width // height
    img = [[2 for w in range(width)] for h in range(height)]

    i = 0
    d = defaultdict(lambda: defaultdict(int))
    for layer in range(layers):
        for y in range(height):
            for x in range(width):
                if img[y][x] == 2:
                    img[y][x] = data[i]
                i += 1

    for row in img:
        print(''.join('#' if _ == 1 else ' ' for _ in row))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
