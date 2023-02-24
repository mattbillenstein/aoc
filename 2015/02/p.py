#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [[int(_) for _ in line.split('x')] for line in lines]

def part1(data):
    tot = 0
    for l, w, h in data:
        sides = [l*w, w*h, h*l]
        tot += sum(2*_ for _ in sides) + min(sides)
    print(tot)

def part2(data):
    tot = 0
    for l, w, h in data:
        sides = [2*l + 2*w, 2*w + 2*h, 2*h + 2*l]
        volume = l * w * h
        tot += min(sides) + volume
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
