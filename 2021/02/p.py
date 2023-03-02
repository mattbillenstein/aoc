#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n').split() for _ in sys.stdin]
    return [(_[0], int(_[1])) for _ in lines]

def part1(data):
    x = y = 0
    for dir, dist in data:
        if dir == 'forward':
            x += dist
        elif dir == 'down':
            y += dist
        elif dir == 'up':
            y -= dist

    print(x*y)

def part2(data):
    x = y = aim = 0
    for dir, dist in data:
        if dir == 'forward':
            x += dist
            y += aim * dist
        elif dir == 'down':
            aim += dist
        elif dir == 'up':
            aim -= dist

    print(x*y)

def main(argv):
    data = parse_input()

    part1(data)
    part2(data)

if __name__ == '__main__':
    main(sys.argv)
